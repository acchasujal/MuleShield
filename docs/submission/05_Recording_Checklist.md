# MuleShield — Hackathon Demo Recording Checklist

This document provides the exact sequence, identifiers, and expected outcomes for recording the perfect hackathon pitch video. The system has been pre-configured with a "Demo Mode Registry" to ensure determinism and a flawless demonstration.

## Demo Identifiers

| Component | Target Identifier | Description |
|-----------|-------------------|-------------|
| **Scenario** | `Dormant Reactivation Ring` | Best multi-vector threat simulation. |
| **Account** | `BOI4421087653` | Highest scoring account with clear layering, anomaly, and dormant flags. |
| **STR Case** | `STR-20260615-8734` | The automatically generated Suspicious Transaction Report. |
| **I4C Webhook** | `ACC0520000000028` | Pre-filled target for the I4C webhook demonstration. |

---

## Recording Sequence & Script

### 1. The Hook (Landing & Threat Ingestion)
- **Action**: Navigate to `Investigations` from the sidebar and click on **Dormant Reactivation Ring** under the Threat Simulation Library.
- **Expected Visual**: The dataset loads with an animated progress bar. The inline results preview appears, showing accounts analyzed, flagged alerts, and critical escalations.
- **Talking Point**: "MuleShield ingests millions of transactions and applies dual-engine ML and graph analysis in under 8 seconds. We've detected a high-severity dormant reactivation ring."

### 2. Executive Dashboard (The Bird's Eye View)
- **Action**: Navigate to `Dashboard`.
- **Expected Visual**: High-level KPIs, severity distribution charts, and the geographical threat map.
- **Talking Point**: "Our platform gives compliance officers a real-time, birds-eye view of emerging AML threats, categorizing risk across the entire financial ecosystem."

### 3. Alert Center (Triage)
- **Action**: Navigate to `Alerts`.
- **Expected Visual**: The alert queue populated with `BOI4421087653` at the top with a `MEDIUM/HIGH` severity badge and an `UNDER_REVIEW` lifecycle stage.
- **Talking Point**: "Alerts are triaged instantly. Here we see an account that transitioned from dormant to active, acting as a layering node."

### 4. Account Inspector (Deep Dive & Explainability)
- **Action**: Navigate to `Accounts`. The ID `BOI4421087653` will be pre-filled via the Demo Registry.
- **Expected Visual**: The Account risk profile, displaying the composite risk score, XGBoost ML score, and Graph Centrality.
- **Action**: Expand the **SHAP Explainability** section.
- **Expected Visual**: Feature importances explaining *why* the model flagged this account (e.g., velocity, value, dormant flags).
- **Talking Point**: "MuleShield isn't a black box. Our SHAP integration explains exactly which transaction features triggered the alert, ensuring regulatory transparency."

### 5. Compliance & Containment (Auto-STR Generation)
- **Action**: Navigate to `Compliance`. Select `BOI4421087653` (if not auto-selected).
- **Expected Visual**: The auto-generated goAML XML report and the Tamper-Proof Evidence Hash (SHA-256).
- **Talking Point**: "Investigations conclude with single-click reporting. We auto-generate goAML compliant XMLs and secure them with a cryptographic hash admissible under the Evidence Act."

### 6. I4C Intelligence Webhook (The 'Wow' Factor)
- **Action**: Navigate to `I4C Intelligence`. The target `ACC0520000000028` and reference `I4C-2026-8819` are pre-filled.
- **Action**: Click **Ingest Webhook Alert**.
- **Expected Visual**: A success banner, composite score metrics, CBS callback action executed, and the goAML XML snippet.
- **Talking Point**: "We integrate directly with government intelligence. A webhook from the I4C portal instantly triggers a re-evaluation and an automated CBS freeze."

---

## Validation Status: PASS
- **No empty states**: Verified.
- **No broken graphs**: Verified (Neo4j connected).
- **No API failures**: Verified (NaN JSON serialization bug resolved).
- **Deterministic state**: Enforced via `frontend/utils/demo_registry.py`.
