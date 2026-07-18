// ============================================================
// MuleShield — Fallback Demo Data
// ============================================================
//
// Loaded when the backend is unavailable (offline / demo mode).
// Keep this data stable across resets — it is the ground truth
// for guided investigation demos.
// ============================================================

import type { CaseItem } from "../types";

export const FALLBACK_CASES: CaseItem[] = [
  {
    account: "ACC05200000000028",
    risk_score: 86,
    severity: "CRITICAL",
    mule_stage: "BEING_FLUSHED",
    profile_risk: 78,
    transaction_risk: 92,
    graph_risk: 65,
    case_id: "STR-20260719-0028",
    evidence_hash:
      "9e31f17b5d8ac4ab41c3a0e9d3f8c21a7a7d59efc26e4ddf0d11f4f2a6b7c2a1",
    reasons: ["Dormant reactivation", "Velocity spike", "Linked accounts"],
    explanation:
      "A dormant account reactivated and moved funds at high velocity through linked accounts. The pattern is consistent with an account being used as a pass-through node.",
    shap_signals: { F3889: 0.82, F3908: 0.74, F886: 0.51, F670: 0.28 },
    evidence: [
      {
        from_account: "ACC05200000000028",
        to_account: "ACC05299999999999",
        amount: 75000,
        timestamp: "2026-07-19 10:42:00",
        from_name: "Subject account",
        to_name: "Consolidation node",
        channel: "UPI",
      },
    ],
    goaml_xml:
      "<goAMLReport><caseId>STR-20260719-0028</caseId><account>ACC05200000000028</account><risk>86</risk><severity>CRITICAL</severity></goAMLReport>",
  },
  {
    account: "ACC05200000000142",
    risk_score: 74,
    severity: "HIGH",
    mule_stage: "ACTIVE_MULE",
    profile_risk: 71,
    transaction_risk: 79,
    graph_risk: 54,
    case_id: "STR-20260719-0142",
    evidence_hash: "5a7c8e9b1d4f6a2b8c0e7f3d9a1b5c6d",
    reasons: ["Circular routing", "High velocity"],
    explanation:
      "The account shows repeated high-velocity transfers and a circular routing pattern across related beneficiaries.",
    shap_signals: { F3908: 0.7, F115: 0.49, F886: 0.35 },
    evidence: [
      {
        from_account: "ACC05200000000142",
        to_account: "ACC05299999999980",
        amount: 42000,
        timestamp: "2026-07-19 09:18:00",
        channel: "IMPS",
      },
    ],
    goaml_xml:
      "<goAMLReport><caseId>STR-20260719-0142</caseId><account>ACC05200000000142</account><risk>74</risk><severity>HIGH</severity></goAMLReport>",
  },
  {
    account: "ACC05200000000199",
    risk_score: 52,
    severity: "MEDIUM",
    mule_stage: "NEWLY_RECRUITED",
    profile_risk: 54,
    transaction_risk: 58,
    graph_risk: 32,
    case_id: "STR-20260719-0199",
    evidence_hash: "7d2a9f4b6c1e8a3d",
    reasons: ["New account activity", "Unusual amount ratio"],
    explanation:
      "The account is newly active with transaction behavior that needs enrichment before escalation.",
    shap_signals: { F115: 0.41, F2082: 0.25 },
    evidence: [
      {
        from_account: "ACC05200000000199",
        to_account: "ACC05200000000011",
        amount: 18500,
        timestamp: "2026-07-19 08:03:00",
        channel: "NEFT",
      },
    ],
    goaml_xml:
      "<goAMLReport><caseId>STR-20260719-0199</caseId><account>ACC05200000000199</account><risk>52</risk><severity>MEDIUM</severity></goAMLReport>",
  },
  {
    account: "ACC05200000000013",
    risk_score: 16,
    severity: "LOW",
    mule_stage: "LEGITIMATE",
    profile_risk: 12,
    transaction_risk: 24,
    graph_risk: 8,
    case_id: "CASE-20260719-0013",
    evidence_hash: "8b7053c65586b6f8",
    reasons: ["Isolated anomaly"],
    explanation:
      "An isolated anomaly was detected, but current evidence does not support escalation.",
    shap_signals: { F3908: -0.19 },
    evidence: [],
    goaml_xml: "",
  },
];
