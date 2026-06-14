"""
MuleShield AI — AI Service Component
Encapsulates Groq, NVIDIA NIM, OpenRouter & Gemini Fallback clients and generation helpers.
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

GROQ_KEY       = os.getenv("GROQ_API_KEY", "")
NVIDIA_KEY     = os.getenv("NVIDIA_API_KEY", "")
OPENROUTER_KEY = os.getenv("OPENROUTER_API_KEY", "")
GEMINI_KEY     = os.getenv("GEMINI_API_KEY", "")

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
AI_TIMEOUT_SECS     = 45           # API calls can be slightly slower on cold start
MAX_STR_TXN         = 20           # transactions sent to /generate-str
MAX_ASK_TXN         = 10           # transactions sent to /ask (keep prompt small)

# Best models per provider checked from API listings
GROQ_STR_MODEL         = "llama-3.3-70b-versatile"
GROQ_ASK_MODEL         = "llama-3.1-8b-instant"

NVIDIA_STR_MODEL       = "meta/llama-3.3-70b-instruct"
NVIDIA_ASK_MODEL       = "meta/llama-3.1-8b-instruct"

OPENROUTER_STR_MODEL   = "meta-llama/llama-3.3-70b-instruct:free"
OPENROUTER_ASK_MODEL   = "meta-llama/llama-3.3-70b-instruct:free"

GEMINI_MODEL           = "gemini-2.0-flash"

# ---------------------------------------------------------------------------
# Client Initializations
# ---------------------------------------------------------------------------
groq_client = None
if GROQ_KEY:
    try:
        from openai import OpenAI as _OpenAI
        groq_client = _OpenAI(
            base_url="https://api.groq.com/openai/v1",
            api_key=GROQ_KEY,
        )
        logger.info("Groq client initialised (Primary AI)")
    except ImportError:
        logger.warning("openai package not installed — Groq client disabled")
else:
    logger.warning("GROQ_API_KEY not set — Groq primary disabled")

nvidia_client = None
if NVIDIA_KEY:
    try:
        from openai import OpenAI as _OpenAI
        nvidia_client = _OpenAI(
            base_url="https://integrate.api.nvidia.com/v1",
            api_key=NVIDIA_KEY,
        )
        logger.info("NVIDIA NIM client initialised (Secondary AI)")
    except ImportError:
        logger.warning("openai package not installed — NVIDIA client disabled")
else:
    logger.warning("NVIDIA_API_KEY not set — NVIDIA secondary disabled")

openrouter_client = None
if OPENROUTER_KEY:
    try:
        from openai import OpenAI as _OpenAI
        openrouter_client = _OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=OPENROUTER_KEY,
        )
        logger.info("OpenRouter client initialised (Tertiary AI)")
    except ImportError:
        logger.warning("openai package not installed — OpenRouter client disabled")
else:
    logger.warning("OPENROUTER_API_KEY not set — OpenRouter tertiary disabled")

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


async def _call_openai_compatible(client, model: str, prompt: str, max_tokens: int, provider_name: str) -> str:
    """
    Call an OpenAI-compatible API using the provided client.
    """
    if not client:
        raise RuntimeError(f"{provider_name} client not configured")

    logger.info(f"{provider_name} call → model={model} max_tokens={max_tokens}")
    loop = asyncio.get_event_loop()
    try:
        response = await asyncio.wait_for(
            loop.run_in_executor(
                None,
                lambda: client.chat.completions.create(
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
            raise RuntimeError(f"{provider_name} returned an empty response")
        logger.info(f"{provider_name} call succeeded ({model})")
        return text
    except asyncio.TimeoutError:
        raise RuntimeError(f"{provider_name} request timed out ({model})")
    except Exception as exc:
        raise RuntimeError(f"{provider_name} error ({model}): {exc}")


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
    task_type: str = "str",
) -> tuple[str, str]:
    """
    Try AI services in order:
    1. Groq
    2. NVIDIA NIM
    3. OpenRouter
    4. Gemini
    Returns (response_text, model_label).
    Raises HTTPException if all fail.
    """
    from fastapi import HTTPException

    # Determine models based on task type
    if task_type == "str":
        groq_model = GROQ_STR_MODEL
        nvidia_model = NVIDIA_STR_MODEL
        openrouter_model = OPENROUTER_STR_MODEL
    else:
        groq_model = GROQ_ASK_MODEL
        nvidia_model = NVIDIA_ASK_MODEL
        openrouter_model = OPENROUTER_ASK_MODEL

    # --- 1. Groq (Primary) ---
    try:
        text = await _call_openai_compatible(groq_client, groq_model, prompt, max_tokens, "Groq")
        return text, f"Groq ({groq_model})"
    except Exception as err:
        logger.warning(f"Groq failed: {err} — trying NVIDIA NIM...")

    # --- 2. NVIDIA NIM (Secondary) ---
    try:
        text = await _call_openai_compatible(nvidia_client, nvidia_model, prompt, max_tokens, "NVIDIA")
        return text, f"NVIDIA ({nvidia_model})"
    except Exception as err:
        logger.warning(f"NVIDIA failed: {err} — trying OpenRouter...")

    # --- 3. OpenRouter (Tertiary) ---
    try:
        text = await _call_openai_compatible(openrouter_client, openrouter_model, prompt, max_tokens, "OpenRouter")
        return text, f"OpenRouter ({openrouter_model})"
    except Exception as err:
        logger.warning(f"OpenRouter failed: {err} — trying Gemini...")

    # --- 4. Gemini (Fallback) ---
    try:
        text = await _call_gemini(prompt, max_tokens)
        return text, f"Gemini ({GEMINI_MODEL} fallback)"
    except Exception as err:
        logger.error(f"Gemini fallback also failed: {err}")
        raise HTTPException(
            status_code=500,
            detail="AI service temporarily unavailable. Please try again.",
        )
