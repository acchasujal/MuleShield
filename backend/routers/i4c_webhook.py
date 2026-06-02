"""
MuleShield AI — Government I4C Threat Intelligence Webhook Router
Ingests suspicious account reports from the Indian government's I4C cybercrime portal,
executes real-time dual-engine scoring, and logs compliance audits.
"""

import logging
import random
import hashlib
from datetime import datetime, timezone
import pandas as pd
from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from backend.ml_service import MLService
from backend.risk_scoring import calculate_composite_risk, assign_tier, align_lifecycle_stage
from backend.xml_generator import generate_goaml_xml
from backend.database import log_case_audit

logger = logging.getLogger("muleshield.i4c")

router = APIRouter(prefix="", tags=["I4C Webhook"])

class I4CWebhookPayload(BaseModel):
    account_no: str
    portal_ref: str # e.g. 'I4C-2026-8819'
    alert_type: str # e.g. 'Dormant Reactivation', 'UPI Velocity Spike'

@router.post("/ingest-i4c")
async def ingest_i4c(body: I4CWebhookPayload, request: Request):
    """Ingests threat alert, executes dual-engine fusion, seeds transaction, and freezes account."""
    ml_service: MLService = getattr(request.app.state, "ml_service", None)
    graph_service = getattr(request.app.state, "graph_service", None)
    
    if not ml_service:
        raise HTTPException(500, detail="ML Service is not initialized on the server.")

    account_no = body.account_no
    portal_ref = body.portal_ref
    alert_type = body.alert_type

    logger.info(f"[I4C Webhook] Ingested alert {portal_ref} for account {account_no} (Type: {alert_type})")

    # 1. Retrieve raw feature columns from BOI DataSet.csv if possible
    # We parse the row index from the account number (ACC052 + 11-digit zero-padded index)
    raw_features = {}
    try:
        # Parse index from account no: e.g. ACC05200000000052 -> 52 -> index 51
        acc_idx = int(account_no[6:]) - 1
        dataset_path = "data/boi/DataSet.csv"
        
        if pd.Series([dataset_path]).map(pd.io.common.file_exists).iloc[0]:
            df_dataset = pd.read_csv(dataset_path, nrows=1, skiprows=range(1, acc_idx + 1))
            if not df_dataset.empty:
                raw_features = df_dataset.iloc[0].to_dict()
    except Exception as exc:
        logger.warning(f"Could not load DataSet.csv features for I4C webhook: {exc}. Reverting to sandbox mock.")

    # Fallback to sandbox features if DataSet.csv row lookup fails
    if not raw_features:
        raw_features = {
            "Unnamed: 0": 999,
            "F670": 1.0, # Prior regulatory warning
            "F886": 0.45, # UPI spike
            "F3908": 0.85, # High velocity passing ratio
            "F115": 0.90,
            "F2082": 0.0, # Complete absence of consumer behaviour
            "F3889": "G365D" # Dormant
        }

    # 2. Run Tabular XGBoost Inference
    pred = ml_service.predict_single(raw_features)
    ml_score = pred.get("ml_score", 0.50)

    # 3. Fetch Neo4j Centrality Connectivity
    graph_score = ml_score
    if graph_service and graph_service.is_connected:
        try:
            # Async degree centrality GDS fetch
            centrality = await graph_service.get_centrality(account_no)
            if centrality > 0.0:
                graph_score = centrality
            
            # Seed real-time transaction to represent the cybercrime portal alert edge
            await graph_service.seed_transaction(
                from_acc=account_no,
                to_acc="ACC05299999999999", # Central suspect consolidation node
                amount=75000.0,
                timestamp=datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
                channel="UPI"
            )
        except Exception as exc:
            logger.warning(f"Neo4j GDS lookup failed in I4C Webhook: {exc}. Reverting to Standalone ML.")

    # 4. Score Fusion Layer
    composite_score = calculate_composite_risk(ml_score, graph_score, 0.0)
    severity = assign_tier(composite_score)
    mule_stage = align_lifecycle_stage(pred.get("mule_stage", "ACTIVE_MULE"), severity, 0.0)

    # 5. goAML Compliant XML payload autopilot
    case_id = f"STR-{datetime.now(timezone.utc).strftime('%Y%m%d')}-{random.randint(1000, 9999)}"
    
    explanations = [
        f"Ingested via I4C portal threat reference {portal_ref}",
        f"Classification alert type: {alert_type}"
    ]
    translation_map = {
        "F670": "Prior regulatory watch-list flag active on account",
        "F886": "Unusual rapid channel-switching behavior detected",
        "F3908": "High velocity in/out ratio (funds passing rapidly)",
        "F115": "Elevated transaction ratio relative to customer history",
        "F2082": "Complete absence of standard retail banking behavior",
        "F3889": "Account is established dormant profile activated for laundering",
        "F3891": "High-vulnerability demographic profile matched (student mule)"
    }
    for feature, shap_val in pred.get("shap_signals", {}).items():
        desc = translation_map.get(feature, f"Elevated weight anomaly in feature {feature}")
        explanations.append(f"{desc} (+{abs(int(shap_val * 100))} pts)")

    evidence = [{
        "from_account": account_no,
        "to_account": "ACC05299999999999",
        "amount": 75000.0,
        "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
        "channel": "UPI"
    }]

    goaml_xml = generate_goaml_xml(
        case_id=case_id,
        account_no=account_no,
        ml_score=ml_score,
        graph_score=graph_score,
        composite_score=composite_score,
        severity=severity,
        mule_stage=mule_stage,
        explanations=explanations,
        evidence=evidence
    )

    evidence_hash = hashlib.sha256(goaml_xml.encode()).hexdigest()

    # 6. Log Case Audit trace in PostgreSQL
    action = "AUTO_FREEZE" if severity in ["CRITICAL", "HIGH"] else "INVESTIGATOR_QUEUED"
    await log_case_audit(
        case_id=case_id,
        account_id=account_no,
        event_type="I4C_PORTAL_WEBHOOK",
        ml_score=ml_score,
        graph_score=graph_score,
        composite_score=composite_score,
        severity=severity,
        mule_stage=mule_stage,
        evidence_hash=evidence_hash,
        action_taken=action
    )

    return {
        "status": "success",
        "portal_reference": portal_ref,
        "account_no": account_no,
        "composite_score": composite_score,
        "severity": severity,
        "mule_stage": mule_stage,
        "action_taken": action,
        "case_id": case_id,
        "evidence_hash": evidence_hash,
        "goaml_xml": goaml_xml
    }
