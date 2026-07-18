// ============================================================
// MuleShield — API Service Layer
// ============================================================

import { API_BASE_URL } from "../constants";
import { tier } from "../utils/caseUtils";
import type { CaseItem, Severity } from "../types";

// ---------------------------------------------------------------------------
// Normalizer — maps raw API response shapes to the canonical CaseItem type
// ---------------------------------------------------------------------------

export function normalizeCase(raw: Record<string, unknown>): CaseItem {
  const score = Number(raw.risk_score ?? raw.composite_score ?? 0);
  return {
    account: String(raw.account ?? raw.account_no ?? "UNKNOWN"),
    risk_score: score,
    severity: (raw.severity ?? tier(score)) as Severity,
    mule_stage: String(raw.mule_stage ?? "LEGITIMATE"),
    profile_risk: Number(raw.profile_risk ?? raw.ml_score ?? 0),
    transaction_risk: Number(raw.transaction_risk ?? 0),
    graph_risk: Number(raw.graph_risk ?? raw.graph_score ?? 0),
    explanation: String(
      raw.explanation ?? "Risk assessment available for investigator review."
    ),
    shap_signals: (raw.shap_signals as Record<string, number>) ?? {},
    evidence_hash: String(raw.evidence_hash ?? "Not returned"),
    case_id: String(raw.case_id ?? `CASE-${Date.now()}`),
    goaml_xml: String(raw.goaml_xml ?? ""),
    evidence: (raw.evidence as CaseItem["evidence"]) ?? [],
    reasons: (raw.reasons as string[]) ?? [],
    scenario: String(raw.scenario ?? "Uploaded transaction batch"),
    institution: String(raw.institution ?? "Bank of India · Demonstration institution"),
    timeline: (raw.timeline as CaseItem["timeline"]) ?? [],
    network: (raw.network as CaseItem["network"]) ?? { nodes: [], edges: [] },
  };
}

// ---------------------------------------------------------------------------
// API calls
// ---------------------------------------------------------------------------

export interface UploadResult {
  cases: CaseItem[];
}

/**
 * Uploads a CSV batch file to the analysis endpoint.
 * Throws on network error or non-OK response.
 */
export async function uploadBatch(file: File): Promise<UploadResult> {
  const form = new FormData();
  form.append("file", file);

  const response = await fetch(`${API_BASE_URL}/analyze`, {
    method: "POST",
    body: form,
  });

  if (!response.ok) {
    throw new Error(`API error: ${response.status} ${response.statusText}`);
  }

  const data = (await response.json()) as { alerts?: Record<string, unknown>[] };
  const cases = (data.alerts ?? []).map(normalizeCase);
  return { cases };
}
