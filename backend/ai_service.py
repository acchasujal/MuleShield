"""
MuleShield AI — AI Service Component
Encapsulates NVIDIA NIM & Gemini Fallback clients and generation helpers.
"""

import asyncio
import hashlib
import json
import logging
import os
from dotenv import load_dotenv

# Initialize logging
logger = logging.getLogger("muleshield.ai_service")

# Load environment variables
load_dotenv()

GEMINI_KEY = os.getenv("GEMINI_API_KEY", "")
NVIDIA_KEY  = os.getenv("NVIDIA_API_KEY", "")

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
AI_TIMEOUT_SECS     = 45           # NVIDIA NIM can be slightly slower on cold start
MAX_STR_TXN         = 20           # transactions sent to /generate-str
MAX_ASK_TXN         = 10           # transactions sent to /ask (keep prompt small)
NVIDIA_STR_MODEL    = "meta/llama-3.1-70b-instruct"
NVIDIA_ASK_MODEL    = "meta/llama-3.1-8b-instruct"
GEMINI_MODEL        = "gemini-2.0-flash"

# ---------------------------------------------------------------------------
# Client Initializations
# ---------------------------------------------------------------------------
nvidia_client = None
if NVIDIA_KEY:
    try:
        from openai import OpenAI as _OpenAI
        nvidia_client = _OpenAI(
            base_url="https://integrate.api.nvidia.com/v1",
            api_key=NVIDIA_KEY,
        )
        logger.info("NVIDIA NIM client initialised (primary AI)")
    except ImportError:
        logger.warning("openai package not installed — NVIDIA client disabled")
else:
    logger.warning("NVIDIA_API_KEY not set — NVIDIA primary disabled")

gemini_client = None
if GEMINI_KEY:
    try:
        from google import genai
        gemini_client = genai.Client(api_key=GEMINI_KEY)
        logger.info(f"Gemini fallback initialised ({GEMINI_MODEL}, new google-genai SDK)")
    except Exception as exc:
        logger.warning(f"Gemini init failed: {exc}")
else:
    logger.warning("GEMINI_API_KEY not set — Gemini fallback disabled")

# ---------------------------------------------------------------------------
# STR Cache & Helpers
# ---------------------------------------------------------------------------
_str_cache: dict[str, dict] = {}


def _slim_transactions(transactions: list, limit: int) -> list:
    """
    Return at most `limit` transactions, keeping only the essential fields
    to minimise token usage sent to the AI.
    """
    keep = {"from_account", "to_account", "amount", "timestamp",
            "from_name", "to_name", "transaction_type", "channel"}
    slimmed = []
    for t in transactions[:limit]:
        slimmed.append({k: v for k, v in t.items() if k in keep})
    return slimmed


def _cache_key(payload: dict) -> str:
    raw = json.dumps(payload, sort_keys=True, default=str)
    return hashlib.sha256(raw.encode()).hexdigest()


async def _call_nvidia(prompt: str, model: str, max_tokens: int) -> str:
    """
    Call NVIDIA NIM API using the openai-compatible client.
    Single attempt with timeout — caller handles retry/fallback.
    Raises RuntimeError on any failure.
    """
    if not nvidia_client:
        raise RuntimeError("NVIDIA client not configured")

    logger.info(f"NVIDIA call → model={model} max_tokens={max_tokens}")
    loop = asyncio.get_event_loop()
    try:
        response = await asyncio.wait_for(
            loop.run_in_executor(
                None,
                lambda: nvidia_client.chat.completions.create(
                    model=model,
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=max_tokens,
                    temperature=0.3,
                    stream=False,
                ),
            ),
            timeout=AI_TIMEOUT_SECS,
        )
        text = response.choices[0].message.content.strip()
        if not text:
            raise RuntimeError("NVIDIA returned an empty response")
        logger.info(f"NVIDIA call succeeded ({model})")
        return text
    except asyncio.TimeoutError:
        raise RuntimeError(f"NVIDIA request timed out ({model})")
    except Exception as exc:
        raise RuntimeError(f"NVIDIA error ({model}): {exc}")


async def _call_gemini(prompt: str, max_tokens: int, retries: int = 2) -> str:
    """
    Call Gemini 2.0 Flash via the new google-genai SDK.
    Exponential backoff retry (fallback only).
    Raises RuntimeError after all retries exhausted.
    """
    if not gemini_client:
        raise RuntimeError("Gemini not configured")

    from google import genai
    last_err: Exception | None = None
    for attempt in range(1, retries + 1):
        try:
            logger.info(f"Gemini fallback attempt {attempt}/{retries} (max_tokens={max_tokens})")
            loop = asyncio.get_event_loop()
            response = await asyncio.wait_for(
                loop.run_in_executor(
                    None,
                    lambda: gemini_client.models.generate_content(
                        model=GEMINI_MODEL,
                        contents=prompt,
                        config=genai.types.GenerateContentConfig(
                            max_output_tokens=max_tokens,
                            temperature=0.3,
                        ),
                    ),
                ),
                timeout=AI_TIMEOUT_SECS,
            )
            text = response.text.strip()
            if not text:
                raise RuntimeError("Gemini returned an empty response")
            logger.info(f"Gemini fallback succeeded (attempt {attempt})")
            return text

        except asyncio.TimeoutError as exc:
            last_err = exc
            logger.warning(f"Gemini timeout on attempt {attempt}")
        except Exception as exc:
            last_err = exc
            logger.warning(f"Gemini error on attempt {attempt}: {exc}")

        if attempt < retries:
            wait = 2 ** attempt   # 2s, 4s
            logger.info(f"Retrying Gemini in {wait}s…")
            await asyncio.sleep(wait)

    raise RuntimeError(f"Gemini failed after {retries} attempts: {last_err}")


async def _generate_with_fallback(
    prompt: str,
    max_tokens: int,
    nvidia_model: str = NVIDIA_STR_MODEL,
) -> tuple[str, str]:
    """
    PRIMARY  → NVIDIA NIM (Llama 3.1)
    FALLBACK → Gemini 2.0 Flash
    Returns (response_text, model_label).
    Raises RuntimeError if both fail.
    """
    # Import here to avoid circular imports or fast fails on load
    from fastapi import HTTPException

    # --- Try NVIDIA first ---
    try:
        text = await _call_nvidia(prompt, nvidia_model, max_tokens)
        return text, nvidia_model
    except RuntimeError as nvidia_err:
        logger.error(f"NVIDIA failed: {nvidia_err} — falling back to Gemini…")

    # --- Gemini fallback ---
    try:
        text = await _call_gemini(prompt, max_tokens)
        return text, f"{GEMINI_MODEL} (fallback)"
    except RuntimeError as gemini_err:
        logger.error(f"Gemini fallback also failed: {gemini_err}")
        raise HTTPException(
            status_code=500,
            detail="AI service temporarily unavailable. Please try again.",
        )
