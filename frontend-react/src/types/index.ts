// ============================================================
// MuleShield — Shared Type Definitions
// ============================================================

import type { LucideIcon } from "lucide-react";

export type { LucideIcon };

export type Severity = "CRITICAL" | "HIGH" | "MEDIUM" | "LOW";

export type AnalystDecision = "PENDING" | "APPROVED" | "ESCALATED";

export type MuleStage =
  | "DORMANT"
  | "ACTIVATION"
  | "NEWLY_RECRUITED"
  | "ACTIVE_MULE"
  | "BEING_FLUSHED"
  | "LEGITIMATE";

export type PrepareState = "idle" | "preparing" | "sealing" | "verified" | "ready";

export interface Evidence {
  from_account: string;
  to_account: string;
  amount: number;
  timestamp: string;
  from_name?: string;
  to_name?: string;
  channel?: string;
}

export interface CaseItem {
  account: string;
  risk_score: number;
  severity: Severity;
  mule_stage: MuleStage | string;
  profile_risk: number;
  transaction_risk: number;
  graph_risk: number;
  explanation: string;
  shap_signals: Record<string, number>;
  evidence_hash: string;
  case_id: string;
  goaml_xml: string;
  evidence: Evidence[];
  reasons: string[];
}

export interface NavItem {
  label: string;
  path: string;
  icon: LucideIcon;
}
