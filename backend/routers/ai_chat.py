"""
MuleShield AI — AI Assistant Router
Exposes /generate-str and /ask endpoints using NVIDIA NIM and Gemini models.
"""

import json
import logging
import random
from datetime import datetime, timezone

from fastapi import APIRouter
from pydantic import BaseModel

from backend.ai_service import (
    _slim_transactions,
    _cache_key,
    _generate_with_fallback,
    _str_cache,
    MAX_STR_TXN,
    MAX_ASK_TXN,
)


logger = logging.getLogger("muleshield.ai_chat")

router = APIRouter(prefix="", tags=["AI Assistant"])


class STRRequest(BaseModel):
    alerts: list
    transactions: list
    scenario_name: str


class AskRequest(BaseModel):
    question: str
    transactions: list


@router.post("/generate-str")
async def generate_str(body: STRRequest):
    """
    Generate a PMLA-compliant Suspicious Transaction Report.
    PRIMARY:  NVIDIA Llama-3.1-70b-instruct
    FALLBACK: Gemini 2.0 Flash
    Results are cached per unique payload hash.
    """
    case_id      = f"STR-{datetime.now(timezone.utc).strftime('%Y-%m-%d')}-{random.randint(1000, 9999)}"
    generated_at = datetime.now(timezone.utc).isoformat()

    # Check cache first (avoids re-calling AI for identical data)
    cache_payload = {
        "alerts": body.alerts,
        "transactions": body.transactions[:MAX_STR_TXN],
        "scenario": body.scenario_name,
    }
    ck = _cache_key(cache_payload)
    if ck in _str_cache:
        logger.info(f"STR cache hit for key {ck[:8]}…")
        cached = _str_cache[ck]
        # Refresh case_id and timestamp on cache hits to keep output unique
        cached.update({"case_id": case_id, "generated_at": generated_at})
        return cached

    # Slim down transactions to reduce token usage
    slim_txn = _slim_transactions(body.transactions, MAX_STR_TXN)

    # Compact but complete prompt
    prompt = f"""You are a senior AML compliance officer at a financial institution.
Generate a Suspicious Transaction Report (STR) per PMLA 2002 and RBI AML guidelines.

SCENARIO: {body.scenario_name}
CASE REFERENCE: {case_id}
FLAGGED ALERTS (summary):
{json.dumps(body.alerts[:10], separators=(',', ':'))}

KEY TRANSACTIONS ({len(slim_txn)} records):
{json.dumps(slim_txn, separators=(',', ':'))}

Write the STR with EXACTLY these sections (plain text, no markdown):
1. CASE REFERENCE
2. REPORTING ENTITY: MuleShield AI, AML Compliance Division
3. SUBJECT ACCOUNTS: IDs, names, suspicious totals
4. FRAUD PATTERN IDENTIFIED
5. TRANSACTION TIMELINE: chronological bullet points
6. REGULATORY BASIS: PMLA 2002 sections + RBI AML Master Circular clauses
7. RECOMMENDED ACTION: Account Freeze / FIU-IND goAML / Refer to ED / Enhanced Monitoring
8. RISK RATING: HIGH/MEDIUM/LOW + one-line justification
9. INVESTIGATING OFFICER: [To be assigned]
10. REPORT GENERATED: {generated_at}"""

    # Use fallback chain for STR (best structured long-form output)
    str_text, model_used = await _generate_with_fallback(
        prompt, max_tokens=1200, task_type="str"
    )

    result = {
        "str_content":  str_text,
        "case_id":      case_id,
        "generated_at": generated_at,
        "model_used":   model_used,
    }

    # Cache result so re-runs on same data skip API calls
    _str_cache[ck] = result
    logger.info(f"STR generated via {model_used} — cached key {ck[:8]}…")
    return result


@router.post("/ask")
async def ask(body: AskRequest):
    """
    Answer a natural-language question about transaction data.
    """
    slim_txn = _slim_transactions(body.transactions, MAX_ASK_TXN)

    prompt = f"""You are an AML investigator assistant for a financial intelligence platform.
Answer in 2-4 plain English sentences. Use account IDs and holder names when available.
Express amounts as \u20b9X lakh or \u20b9X crore. Never speculate beyond the data.

TRANSACTION DATA ({len(slim_txn)} records):
{json.dumps(slim_txn, separators=(',', ':'))}

QUESTION: {body.question}

Answer:"""

    # Use fallback chain for Q&A — fastest model for short factual responses
    answer, model_used = await _generate_with_fallback(
        prompt, max_tokens=300, task_type="ask"
    )
    logger.info(f"Ask answered via {model_used}")
    return {"answer": answer, "question": body.question, "model_used": model_used}
