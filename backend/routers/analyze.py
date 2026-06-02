"""
MuleShield AI — Transaction Analysis Router
Exposes the /analyze endpoint for CSV parsing and fraud intelligence extraction.
"""

import asyncio
import hashlib
import json
import logging
import random
import traceback
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone

import pandas as pd
from fastapi import APIRouter, HTTPException, UploadFile, Request

from backend.explain import generate_explanation
from backend.fraud_detection import (
    detect_cycles, detect_layering, detect_structuring,
    detect_velocity, detect_anomaly, detect_dormant, ml_anomaly,
)
from backend.graph_builder import build_graph
from backend.risk_scoring import (
    calculate_composite_risk,
    assign_tier,
    calculate_transaction_score,
    align_lifecycle_stage,
)
from backend.xml_generator import generate_goaml_xml
from backend.utils import _validate_dataframe, lookup_account_features

# Logger setup
logger = logging.getLogger("muleshield.analyze")

# Shared thread pool for CPU-bound detection functions
_detection_pool = ThreadPoolExecutor(max_workers=4)

router = APIRouter(prefix="", tags=["Analysis"])


def get_fraud_paths(cycles: list) -> list[str]:
    return [" → ".join(c + [c[0]]) for c in cycles]


def generate_evidence_hash(alerts: list, transactions_dict: list) -> str:
    """
    Generates a deterministic SHA-256 hash of the complete evidence
    package. sort_keys=True ensures same input always produces same hash.
    If any alert or transaction is modified after this hash is generated,
    the hash will change — proving tampering occurred.
    """
    payload = {
        "alerts": alerts,
        "transactions": transactions_dict,
        "schema_version": "1.0",
    }
    data = json.dumps(payload, sort_keys=True, default=str)
    return hashlib.sha256(data.encode()).hexdigest()


@router.post("/analyze")
async def analyze(file: UploadFile, request: Request):
    """Upload a transaction CSV and receive fraud-risk analysis.

    Optimised pipeline:
      1. Graph-based signals (cycles, layering) run sequentially (need G)
      2. DataFrame-based signals run concurrently via thread pool
      3. All signals stored as sets for O(1) lookups
      4. Name lookup dict built once, shared across all explanations
    """
    try:
        df = pd.read_csv(file.file)
    except Exception as exc:
        raise HTTPException(400, detail=f"Could not parse CSV: {exc}")

    df = _validate_dataframe(df)

    try:
        # ── Phase 1: Build graph + graph-based signals ────────────────────
        loop = asyncio.get_event_loop()
        G = await loop.run_in_executor(_detection_pool, build_graph, df)
        cycles = await loop.run_in_executor(_detection_pool, detect_cycles, G)

        # ── Phase 2: Run independent detectors concurrently ───────────────
        layering_fut    = loop.run_in_executor(_detection_pool, detect_layering, G)
        structuring_fut = loop.run_in_executor(_detection_pool, detect_structuring, df)
        velocity_fut    = loop.run_in_executor(_detection_pool, detect_velocity, df)
        anomaly_fut     = loop.run_in_executor(_detection_pool, detect_anomaly, df)
        dormant_fut     = loop.run_in_executor(_detection_pool, detect_dormant, df)
        ml_anomaly_fut  = loop.run_in_executor(_detection_pool, ml_anomaly, df)

        (
            layering_paths, structuring_accs, velocity_accs,
            anomaly_accs, dormant_accs, ml_anomaly_accs,
        ) = await asyncio.gather(
            layering_fut, structuring_fut, velocity_fut,
            anomaly_fut, dormant_fut, ml_anomaly_fut,
        )

        # ── Phase 3: Build signals as SETS for O(1) lookup ────────────────
        signals = {
            "cycle":       set(n for c in cycles for n in c),
            "layering":    set(n for p in layering_paths for n in p),
            "structuring": set(structuring_accs),
            "velocity":    set(velocity_accs),
            "anomaly":     set(anomaly_accs),
            "dormant":     set(dormant_accs),
            "ml_anomaly":  set(ml_anomaly_accs),
        }

        # ── Phase 4: Pre-build name lookup (once, not per-account) ────────
        name_lookup = {}
        if "from_name" in df.columns:
            name_pairs = df[["from_account", "from_name"]].drop_duplicates("from_account")
            name_lookup = dict(zip(name_pairs["from_account"], name_pairs["from_name"]))

        # ── Phase 5: Score + explain each node ────────────────────────────
        results = []
        ml_service = getattr(request.app.state, "ml_service", None)
        graph_service = getattr(request.app.state, "graph_service", None)

        for node in G.nodes:
            raw_features = lookup_account_features(node)
            
            # Exec ML prediction
            if ml_service:
                pred = ml_service.predict_single(raw_features)
                ml_score = pred.get("ml_score", 0.50)
                mule_stage = pred.get("mule_stage", "LEGITIMATE")
                shap_signals = pred.get("shap_signals", {})
            else:
                ml_score = 0.50
                mule_stage = "LEGITIMATE"
                shap_signals = {}
                
            # Exec GDS centrality lookup
            graph_score = ml_score
            if graph_service and graph_service.is_connected:
                try:
                    centrality = await graph_service.get_centrality(node)
                    if centrality > 0.0:
                        graph_score = centrality
                except Exception as exc:
                    logger.warning(f"Neo4j GDS lookup failed in /analyze: {exc}")
                    
            # Reasons matched
            reasons = []
            for signal, accounts in signals.items():
                if node in accounts:
                    reasons.append(signal)

            txn_score = calculate_transaction_score(reasons)
            
            # Fused score (XGBoost baseline + dynamic NetworkX heuristics + centrality)
            composite_score = calculate_composite_risk(ml_score, graph_score, txn_score)
            severity = assign_tier(composite_score)
            mule_stage = align_lifecycle_stage(mule_stage, severity, txn_score)
            
            explanation = generate_explanation(
                node, df, signals, name_lookup=name_lookup
            )
            
            # Conditional STR & PostgreSQL Audit Logging
            goaml_xml = ""
            case_id = None
            evidence_hash = None
            
            if severity in ["MEDIUM", "HIGH", "CRITICAL"]:
                case_id = f"STR-{datetime.now(timezone.utc).strftime('%Y%m%d')}-{random.randint(1000, 9999)}"
                
                # Expose named SHAP-to-feature narratives for goAML (same as predict_single / predict_batch)
                explanations_list = []
                translation_map = {
                    "F670": "Prior regulatory watch-list flag active on account",
                    "F886": "Unusual rapid channel-switching behavior detected",
                    "F3908": "High velocity in/out ratio (funds passing through rapidly)",
                    "F115": "Elevated transaction ratio relative to customer history",
                    "F2082": "Complete absence of standard retail banking behavior",
                    "F3889": "Account is established dormant profile activated for laundering",
                    "F3891": "High-vulnerability demographic profile matched (student mule)"
                }
                for feature, shap_val in shap_signals.items():
                    desc = translation_map.get(feature, f"Elevated weight anomaly in feature {feature}")
                    explanations_list.append(f"{desc} (+{abs(int(shap_val * 100))} pts)")
                
                goaml_xml = generate_goaml_xml(
                    case_id=case_id,
                    account_no=node,
                    ml_score=ml_score,
                    graph_score=graph_score,
                    composite_score=composite_score,
                    severity=severity,
                    mule_stage=mule_stage,
                    explanations=explanations_list,
                    evidence=explanation["evidence"]
                )
                evidence_hash = hashlib.sha256(goaml_xml.encode()).hexdigest()
                
                # Asynchronously log postgres audit trail
                action = "AUTO_FREEZE" if severity == "CRITICAL" else "INVESTIGATOR_QUEUED"
                from backend.database import log_case_audit
                asyncio.create_task(log_case_audit(
                    case_id=case_id,
                    account_id=node,
                    event_type="RISK_FUSION",
                    ml_score=ml_score,
                    graph_score=graph_score,
                    composite_score=composite_score,
                    severity=severity,
                    mule_stage=mule_stage,
                    evidence_hash=evidence_hash,
                    action_taken=action
                ))
            
            results.append({
                "account": node,
                "risk_score": composite_score,
                "severity": severity,
                "reasons": reasons,
                "explanation": explanation["summary"],
                "evidence": explanation["evidence"],
                "mule_stage": mule_stage,
                "ml_score": round(ml_score * 100.0, 2),
                "graph_score": round(graph_score * 100.0, 2),
                "profile_risk": round(ml_score * 100.0, 2),
                "transaction_risk": round(txn_score, 2),
                "graph_risk": round(graph_score * 100.0, 2),
                "shap_signals": shap_signals,
                "goaml_xml": goaml_xml,
                "case_id": case_id,
                "evidence_hash": evidence_hash
            })

        fraud_paths = get_fraud_paths(cycles)

        # Sort alerts by risk score before hashing (deterministic order)
        sorted_alerts = sorted(results, key=lambda x: x["risk_score"], reverse=True)

        # Cryptographic seal over the complete evidence package
        evidence_hash   = generate_evidence_hash(sorted_alerts, df.to_dict("records"))
        hash_generated  = datetime.now(timezone.utc).isoformat()

        # Convert sets → lists for JSON serialisation in the response
        signals_serialisable = {k: sorted(v) for k, v in signals.items()}

        logger.info(
            f"Analysis complete — {len(results)} alerts, {len(cycles)} cycles, "
            f"evidence hash: {evidence_hash[:16]}…"
        )

        # Store in shared app state cache for absolute predict/single consistency
        request.app.state.analyze_results_cache = {res["account"]: res for res in results}

        return {
            "alerts":            sorted_alerts,
            "signals":           signals_serialisable,
            "fraud_paths":       fraud_paths,
            "evidence_hash":     evidence_hash,
            "hash_generated_at": hash_generated,
        }

    except HTTPException:
        raise
    except ValueError as exc:
        raise HTTPException(400, detail=str(exc))
    except Exception as exc:
        traceback.print_exc()
        raise HTTPException(500, detail=f"Analysis failed: {type(exc).__name__}: {exc}")
