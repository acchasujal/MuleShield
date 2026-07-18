// ============================================================
// MuleShield — Case Utilities
// ============================================================

import { SIGNAL_NAMES } from "../constants";
import type { CaseItem, Severity } from "../types";

/**
 * Maps a Severity value to its CSS class name.
 */
export function severityClass(severity: Severity): string {
  return severity.toLowerCase();
}

/**
 * Converts a snake_case mule stage string into a human-readable label.
 * e.g. "BEING_FLUSHED" → "Being Flushed"
 */
export function labelStage(stage: string): string {
  return stage
    .replace(/_/g, " ")
    .replace(/\b\w/g, (m) => m.toUpperCase());
}

/**
 * Derives a Severity tier from a numeric risk score.
 */
export function tier(score: number): Severity {
  if (score >= 80) return "CRITICAL";
  if (score >= 60) return "HIGH";
  if (score >= 40) return "MEDIUM";
  return "LOW";
}

/**
 * Returns the top-3 SHAP signals for a case, sorted by absolute value.
 */
export function briefFor(
  item: CaseItem
): { key: string; text: string; val: number }[] {
  return Object.entries(item.shap_signals)
    .sort((a, b) => Math.abs(b[1]) - Math.abs(a[1]))
    .slice(0, 3)
    .map(([key, val]) => ({
      key,
      text: SIGNAL_NAMES[key] ?? `Elevated factor ${key}`,
      val,
    }));
}

/**
 * Maps a SHAP feature key to the risk dimension it belongs to.
 */
export function shapKeyToDimension(
  key: string
): "profile" | "transaction" | "network" {
  if (key === "F3889" || key === "F3891") return "profile";
  if (key === "F3908" || key === "F115" || key === "F886") return "transaction";
  return "network";
}

/**
 * Returns the recommendation text for a given severity.
 */
export function recommendationFor(severity: Severity): string {
  switch (severity) {
    case "LOW":
      return "No escalation recommended from current evidence.";
    case "MEDIUM":
      return "Monitor and enrich profile before escalation.";
    default:
      return "Immediate review and escalation under bank policy.";
  }
}
