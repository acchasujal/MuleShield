// ============================================================
// MuleShield — Stat Card
// Used in the Cases page summary grid.
// ============================================================

import { memo } from "react";
import type { Severity } from "../../types";

interface StatCardProps {
  label: string;
  value: string;
  detail: string;
  severity: Severity | "low";
}

export const StatCard = memo(function StatCard({
  label,
  value,
  detail,
  severity,
}: StatCardProps) {
  return (
    <div className="card stat-card">
      <div className={`status-badge severity-${severity.toLowerCase()}`}>
        <span className="status-dot" aria-hidden="true" />
        {label}
      </div>
      <div className="stat-value" aria-label={`${value} ${label}`}>
        {value}
      </div>
      <div className="stat-label">{detail}</div>
    </div>
  );
});
