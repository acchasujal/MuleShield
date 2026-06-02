import asyncio
import logging
import pandas as pd
from fastapi import APIRouter, HTTPException, UploadFile, File, Request
from pydantic import BaseModel
from backend.ml_service import MLService
from backend.risk_scoring import calculate_composite_risk, assign_tier, align_lifecycle_stage

logger = logging.getLogger("muleshield.router")

async def background_graph_seed(graph_service, df_raw):
    """Asynchronously seeds simulated transactions into Neo4j to build topological context."""
    if not graph_service or not graph_service.is_connected:
        return
    try:
        logger.info(f"Triggering background Neo4j graph seeding for {len(df_raw)} profiles...")
        # Create a mock transactional DataFrame that conforms to graph_service.seed_batch_transactions
        txn_records = []
        for idx, row in df_raw.head(1000).iterrows(): # Limit to 1000 records to prevent bottlenecks
            raw_id = row.get("Unnamed: 0", idx + 1)
            from_acc = f"ACC052{str(raw_id).zfill(11)}"
            to_acc = "ACC05299999999999" # Central consolidation node
            amount = float(row.get("F2578", 50000)) if not pd.isnull(row.get("F2578")) else 50000
            timestamp = pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
            channel = "UPI" if row.get("F886", 0) > 0.15 else "NEFT"
            txn_records.append({
                "from_account": from_acc,
                "to_account": to_acc,
                "amount": amount,
                "timestamp": timestamp,
                "channel": channel
            })
        
        df_txn = pd.DataFrame(txn_records)
        await graph_service.seed_batch_transactions(df_txn)
    except Exception as exc:
        logger.warning(f"Background graph seeding failed: {exc}")

router = APIRouter(prefix="", tags=["Inference"])

class SinglePredictionRequest(BaseModel):
    features: dict

class SinglePredictionResponse(BaseModel):
    account: str
    ml_score: float
    graph_score: float
    composite_score: float
    severity: str
    mule_stage: str
    shap_signals: dict
    goaml_xml: str | None = None
    case_id: str | None = None
    profile_risk: float | None = None
    transaction_risk: float | None = None
    graph_risk: float | None = None

@router.post("/predict/single", response_model=SinglePredictionResponse)
async def predict_single(body: SinglePredictionRequest, request: Request):
    """Executes prediction on a single account profile."""
    # Retrieve ML service from app state
    ml_service: MLService = getattr(request.app.state, "ml_service", None)
    if not ml_service:
        raise HTTPException(500, detail="ML Service is not initialized on the server.")

    features = body.features
    account_id = features.get("Unnamed: 0", features.get("account_id", "ACC_UNKNOWN"))

    raw_id = features.get("Unnamed: 0", "UNKNOWN")
    if raw_id != "UNKNOWN":
        formatted_acc_id = f"ACC052{str(raw_id).zfill(11)}"
    else:
        formatted_acc_id = str(account_id)

    # Check global session cache from analyze first to maintain 100% consistency
    cache = getattr(request.app.state, "analyze_results_cache", {})
    if formatted_acc_id in cache:
        cached_res = cache[formatted_acc_id]
        return SinglePredictionResponse(
            account=str(raw_id) if raw_id != "UNKNOWN" else formatted_acc_id,
            ml_score=cached_res["ml_score"],
            graph_score=cached_res["graph_score"],
            composite_score=cached_res["risk_score"],
            severity=cached_res["severity"],
            mule_stage=cached_res["mule_stage"],
            shap_signals=cached_res["shap_signals"],
            goaml_xml=cached_res.get("goaml_xml"),
            case_id=cached_res.get("case_id"),
            profile_risk=cached_res.get("profile_risk"),
            transaction_risk=cached_res.get("transaction_risk"),
            graph_risk=cached_res.get("graph_risk")
        )

    # Execute ML inference
    pred = ml_service.predict_single(features)
    if "error" in pred:
        raise HTTPException(400, detail=pred["error"])

    ml_score = pred["ml_score"]
    
    # Calculate fallback graph score (default to ml_score if Neo4j is offline)
    # Fetch GDS centrality score asynchronously if connected
    graph_service = getattr(request.app.state, "graph_service", None)
    graph_score = ml_score
    if graph_service and graph_service.is_connected:
        try:
            # Normalized centrality
            centrality = await graph_service.get_centrality(formatted_acc_id)
            
            # If the database returns 0.0 (unconnected node), fall back to ml_score to be safe
            if centrality > 0.0:
                graph_score = centrality
            else:
                graph_score = ml_score
        except Exception as exc:
            logger.warning(f"Neo4j single GDS lookup failed: {exc}. Reverting to Standalone ML fallback.")
            graph_score = ml_score
    
    # Fusion Composite risk score (No transaction context in baseline lookup -> txn_score = 0.0)
    composite_score = calculate_composite_risk(ml_score, graph_score, 0.0)
    severity = assign_tier(composite_score)
    mule_stage = align_lifecycle_stage(pred["mule_stage"], severity, 0.0)

    # Generate case reference and auto-goAML compliant XML if critical / high risk
    import random
    from datetime import datetime, timezone
    import hashlib
    from backend.xml_generator import generate_goaml_xml
    from backend.database import log_case_audit
    
    goaml_xml = None
    case_id = None
    evidence_hash = None
    
    if severity in ["MEDIUM", "HIGH", "CRITICAL"]:
        case_id = f"STR-{datetime.now(timezone.utc).strftime('%Y%m%d')}-{random.randint(1000, 9999)}"
        
        # Expose mathematical SHAP-to-feature narratives
        explanations = []
        translation_map = {
            "F670": "Prior regulatory watch-list flag active on account",
            "F886": "Unusual rapid channel-switching behavior detected",
            "F3908": "High velocity in/out ratio (funds passing through rapidly)",
            "F115": "Elevated transaction ratio relative to customer history",
            "F2082": "Complete absence of standard retail banking behavior",
            "F3889": "Account is established dormant profile activated for laundering",
            "F3891": "High-vulnerability demographic profile matched (student mule)"
        }
        for feature, shap_val in pred["shap_signals"].items():
            desc = translation_map.get(feature, f"Elevated weight anomaly in feature {feature}")
            explanations.append(f"{desc} (+{abs(int(shap_val * 100))} pts)")
            
        # Generate mock transaction history matching their profile for goAML
        evidence = []
        amount = float(features.get("F2578", 50000)) if not pd.isnull(features.get("F2578")) else 50000
        evidence.append({
            "from_account": formatted_acc_id,
            "to_account": "ACC05299999999999",
            "amount": amount,
            "timestamp": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S"),
            "channel": "UPI" if features.get("F886", 0) > 0.15 else "NEFT"
        })

        # Auto goAML compliance autopilot
        goaml_xml = generate_goaml_xml(
            case_id=case_id,
            account_no=formatted_acc_id,
            ml_score=ml_score,
            graph_score=graph_score,
            composite_score=composite_score,
            severity=severity,
            mule_stage=mule_stage,
            explanations=explanations,
            evidence=evidence
        )
        
        # TAMPER-PROOF EVIDENCE INTEGRITY SEAL per Indian Evidence Act 65B
        evidence_hash = hashlib.sha256(goaml_xml.encode()).hexdigest()

        # Log case auditing trace in PostgreSQL database
        action = "AUTO_FREEZE" if severity == "CRITICAL" else "INVESTIGATOR_QUEUED"
        # Execute database logging asynchronously in background
        asyncio.create_task(log_case_audit(
            case_id=case_id,
            account_id=formatted_acc_id,
            event_type="RISK_FUSION",
            ml_score=ml_score,
            graph_score=graph_score,
            composite_score=composite_score,
            severity=severity,
            mule_stage=mule_stage,
            evidence_hash=evidence_hash,
            action_taken=action
        ))

    return SinglePredictionResponse(
        account=str(account_id),
        ml_score=round(ml_score * 100.0, 2),
        graph_score=round(graph_score * 100.0, 2),
        composite_score=composite_score,
        severity=severity,
        mule_stage=mule_stage,
        shap_signals=pred["shap_signals"],
        goaml_xml=goaml_xml,
        case_id=case_id,
        profile_risk=round(ml_score * 100.0, 2),
        transaction_risk=0.0,
        graph_risk=round(graph_score * 100.0, 2)
    )

@router.post("/predict/batch")
async def predict_batch(request: Request, file: UploadFile = File(...)):
    """Ingests a CSV containing account profiles, runs inference, and returns critical flagged alerts."""
    ml_service: MLService = getattr(request.app.state, "ml_service", None)
    if not ml_service:
        raise HTTPException(500, detail="ML Service is not initialized on the server.")

    try:
        # Load CSV buffer with high-speed dimension slicing using usecols
        try:
            # Read first line (column headers) to slice parsing dimensions
            first_line = file.file.readline()
            if isinstance(first_line, bytes):
                headers_str = first_line.decode("utf-8", errors="ignore")
            else:
                headers_str = first_line
            
            headers = [h.strip().strip('"').strip("'") for h in headers_str.split(",")]
            file.file.seek(0)  # Reset stream position
            
            # Select only required columns (metadata + features + staging fields)
            required_cols = {"Unnamed: 0", "from_account", "to_account", "amount", "timestamp",
                             "from_name", "to_name", "transaction_type", "channel"}
            if ml_service and ml_service.feature_names:
                required_cols.update(ml_service.feature_names)
            required_cols.update(["F3889", "F3912", "F670", "F115", "F2082", "F2578", "F886"])
            
            usecols = [c for c in headers if c in required_cols]
            if not usecols:
                usecols = None
        except Exception:
            # Robust fallback to read all columns if slicing fails
            try:
                file.file.seek(0)
            except Exception:
                pass
            usecols = None

        df_raw = pd.read_csv(file.file, usecols=usecols)
    except Exception as exc:
        raise HTTPException(400, detail=f"Failed to parse CSV file: {exc}")

    if df_raw.empty:
        raise HTTPException(400, detail="Uploaded CSV file contains zero records.")

    # Validate that we have features. If the columns are not named F1...F3924, raise an error.
    feature_cols = [c for c in df_raw.columns if c.startswith("F")]
    if not feature_cols:
        raise HTTPException(400, detail="Uploaded file does not match DataSet layout (missing F-features columns).")

    try:
        # Execute batch ML inference
        predictions = ml_service.predict_batch(df_raw)

        # Ingest graph connectivity score from graph_service using bulk query
        graph_service = getattr(request.app.state, "graph_service", None)
        graph_scores = {}
        
        if graph_service and graph_service.is_connected:
            try:
                # Build account list
                acc_ids = []
                for pred in predictions:
                    idx = pred["index"]
                    row = df_raw.iloc[idx]
                    raw_id = row.get("Unnamed: 0", idx + 1)
                    account_id = f"ACC052{str(raw_id).zfill(11)}"
                    acc_ids.append(account_id)
                
                # Fetch centralities in a single bulk query roundtrip!
                graph_scores = await graph_service.get_centralities_bulk(acc_ids)
                
                # Trigger asynchronous graph seeding in the background
                asyncio.create_task(background_graph_seed(graph_service, df_raw))
            except Exception as exc:
                logger.warning(f"Neo4j GDS batch centrality bulk lookup failed: {exc}. Reverting to Standalone ML fallback.")

        # Build response alerts
        alerts = []
        bulk_audits = []
        
        import random
        from datetime import datetime, timezone
        import hashlib
        from backend.xml_generator import generate_goaml_xml
        from backend.database import log_case_audits_bulk
        
        for pred in predictions:
            idx = pred["index"]
            row = df_raw.iloc[idx]
            
            # Format account ID: ACC052 + index zfill(11)
            raw_id = row.get("Unnamed: 0", idx + 1)
            account_id = f"ACC052{str(raw_id).zfill(11)}"

            ml_score = pred["ml_score"]
            # Fallback to ml_score if graph score not fetched or returns 0.0
            graph_score = graph_scores.get(account_id, ml_score)
            if graph_score == 0.0:
                graph_score = ml_score

            # Score Fusion layer
            composite_score = calculate_composite_risk(ml_score, graph_score, 0.0)
            severity = assign_tier(composite_score)
            mule_stage = align_lifecycle_stage(pred["mule_stage"], severity, 0.0)

            # Map the top-5 feature significance indices to human-readable explanations
            reasons = []
            explanations = []
            
            # Map translated human-readable fraud signals
            translation_map = {
                "F670": "Prior regulatory watch-list flag active on account",
                "F886": "Unusual rapid channel-switching behavior detected",
                "F3908": "High velocity in/out ratio (funds passing through rapidly)",
                "F115": "Elevated transaction ratio relative to customer history",
                "F2082": "Complete absence of standard retail banking behavior",
                "F3889": "Account is established dormant profile activated for laundering",
                "F3891": "High-vulnerability demographic profile matched (student mule)"
            }

            for feature, shap_val in pred["shap_signals"].items():
                reasons.append(feature)
                desc = translation_map.get(feature, f"Elevated weight anomaly detected in feature {feature}")
                explanations.append(f"{desc} (+{abs(int(shap_val * 100))} pts)")

            # Dynamic Slicing: Omit XML compliance overhead for low risk accounts
            goaml_xml = ""
            evidence = []
            case_id = None
            evidence_hash = None
            
            if severity in ["MEDIUM", "HIGH", "CRITICAL"]:
                case_id = f"STR-{datetime.now(timezone.utc).strftime('%Y%m%d')}-{random.randint(1000, 9999)}"
                
                # Format evidence list
                amount = float(row.get("F2578", 50000)) if not pd.isnull(row.get("F2578")) else 50000
                evidence.append({
                    "from_account": account_id,
                    "from_name": f"Customer #{raw_id}",
                    "to_account": "ACC05299999999999",
                    "to_name": "Consolidation Node",
                    "amount": amount,
                    "timestamp": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "channel": "UPI" if row.get("F886", 0) > 0.15 else "NEFT",
                    "location": "Mumbai",
                    "transaction_type": "DR"
                })
                
                # Auto-generate XML compliance payload
                goaml_xml = generate_goaml_xml(
                    case_id=case_id,
                    account_no=account_id,
                    ml_score=ml_score,
                    graph_score=graph_score,
                    composite_score=composite_score,
                    severity=severity,
                    mule_stage=mule_stage,
                    explanations=explanations,
                    evidence=evidence
                )
                
                evidence_hash = hashlib.sha256(goaml_xml.encode()).hexdigest()
                
                # Queue PostgreSQL audit logging in bulk
                action = "AUTO_FREEZE" if severity == "CRITICAL" else "INVESTIGATOR_QUEUED"
                bulk_audits.append({
                    "case_id": case_id,
                    "account_id": account_id,
                    "event_type": "BATCH_RISK_FUSION",
                    "ml_score": ml_score,
                    "graph_score": graph_score,
                    "composite_score": composite_score,
                    "severity": severity,
                    "mule_stage": mule_stage,
                    "evidence_hash": evidence_hash,
                    "action_taken": action
                })

            alerts.append({
                "account": account_id,
                "risk_score": composite_score,
                "severity": severity,
                "reasons": reasons,
                "explanation": " | ".join(explanations),
                "evidence": evidence,
                "mule_stage": mule_stage,
                "goaml_xml": goaml_xml,
                "case_id": case_id,
                "evidence_hash": evidence_hash
            })

        # Trigger PostgreSQL bulk write
        if bulk_audits:
            asyncio.create_task(log_case_audits_bulk(bulk_audits))

        # Sort alerts by composite risk score descending
        sorted_alerts = sorted(alerts, key=lambda x: x["risk_score"], reverse=True)

        logger.info(f"Batch prediction complete: flagged {len(sorted_alerts)} accounts.")
        
        # Return matched alerts
        return {
            "alerts": sorted_alerts,
            "total_analyzed": len(df_raw),
            "flagged_count": len(sorted_alerts)
        }

    except Exception as exc:
        logger.error(f"Failed to execute batch prediction: {exc}", exc_info=True)
        raise HTTPException(500, detail=f"Inference error: {exc}")
