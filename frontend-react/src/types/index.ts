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

export interface TimelineEvent {
  timestamp: string;
  label: string;
  detail: string;
  risk_delta: number;
  kind: "signal" | "transaction" | "network" | "decision";
}

export interface NetworkNode {
  id: string;
  label: string;
  role: string;
  risk: "subject" | "linked" | "sink" | "legitimate";
}

export interface NetworkEdge {
  from: string;
  to: string;
  amount: number;
  channel: string;
  direction: "inbound" | "outbound";
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
  scenario: string;
  institution: string;
  timeline: TimelineEvent[];
  network: { nodes: NetworkNode[]; edges: NetworkEdge[] };
}

export interface NavItem {
  label: string;
  path: string;
  icon: LucideIcon;
}
