// ============================================================
// MuleShield — Application Constants
// ============================================================

import type { LucideIcon } from "lucide-react";
import {
  Activity,
  BarChart3,
  FileCheck2,
  GitBranch,
  Home,
  Sparkles,
  Waypoints,
} from "lucide-react";

import type { NavItem } from "../types";

// ---------------------------------------------------------------------------
// API
// ---------------------------------------------------------------------------
export const API_BASE_URL: string =
  (import.meta as unknown as { env: Record<string, string> }).env?.VITE_API_URL ??
  "http://127.0.0.1:8000";

// ---------------------------------------------------------------------------
// Navigation
// ---------------------------------------------------------------------------
export const NAV_ITEMS: NavItem[] = [
  { label: "Cases", path: "/cases", icon: Home },
  { label: "Investigate", path: "/investigate", icon: Sparkles },
  { label: "Evidence", path: "/evidence", icon: FileCheck2 },
  { label: "Methodology", path: "/methodology", icon: BarChart3 },
];

// ---------------------------------------------------------------------------
// Mule lifecycle stages (ordered)
// ---------------------------------------------------------------------------
export const MULE_STAGES = [
  "DORMANT",
  "ACTIVATION",
  "NEWLY_RECRUITED",
  "ACTIVE_MULE",
  "BEING_FLUSHED",
] as const;

// ---------------------------------------------------------------------------
// SHAP signal display names
// ---------------------------------------------------------------------------
export const SIGNAL_NAMES: Record<string, string> = {
  F670: "Prior regulatory watch-list signal",
  F886: "Unusual payment-channel switching",
  F3908: "High-velocity pass-through behavior",
  F115: "Elevated transaction frequency",
  F2082: "Normal retail activity is absent",
  F3889: "Dormant profile reactivated",
  F3891: "High-vulnerability profile signal",
};

// ---------------------------------------------------------------------------
// Methodology weights (used in WeightCard)
// ---------------------------------------------------------------------------
export const METHODOLOGY_WEIGHTS: Array<{
  value: string;
  label: string;
  text: string;
  icon: LucideIcon;
}> = [
  {
    value: "40%",
    label: "Profile behavior",
    text: "XGBoost profile inference and SHAP attribution.",
    icon: Activity,
  },
  {
    value: "40%",
    label: "Transaction behavior",
    text: "Velocity, layering, cycles, structuring, and anomaly signals.",
    icon: Waypoints,
  },
  {
    value: "20%",
    label: "Network context",
    text: "Graph relationship evidence when enrichment is available.",
    icon: GitBranch,
  },
];

// ---------------------------------------------------------------------------
// Animation durations (ms) — keep in sync with tokens.css
// ---------------------------------------------------------------------------
export const DURATION = {
  fast: 120,
  base: 180,
  slow: 280,
  unfold: 1200,
  toast: 2600,
  prepare: 400,
} as const;
