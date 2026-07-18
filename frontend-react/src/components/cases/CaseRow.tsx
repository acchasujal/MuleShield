// ============================================================
// MuleShield — Case Row
// Reusable case list item used in Cases page and Investigation sidebar.
// ============================================================

import { memo } from "react";
import { labelStage, severityClass } from "../../utils/caseUtils";
import { Highlight } from "../ui/Highlight";
import type { CaseItem } from "../../types";

interface CaseRowProps {
  item: CaseItem;
  selected?: boolean;
  onClick: () => void;
  query?: string;
  /** When true, shows a compact 1-column layout (used in investigation sidebar) */
  compact?: boolean;
}

export const CaseRow = memo(function CaseRow({
  item,
  selected = false,
  onClick,
  query = "",
  compact = false,
}: CaseRowProps) {
  return (
    <button
      className={`case-row${selected ? " selected" : ""}${compact ? " case-row-compact" : ""}`}
      onClick={onClick}
      aria-pressed={selected}
      aria-label={`Case ${item.account}, ${item.severity} severity, score ${Math.round(item.risk_score)}`}
      style={compact ? { gridTemplateColumns: "1fr" } : undefined}
    >
      <div>
        <div className={`status-badge severity-${severityClass(item.severity)}`}>
          <span className="status-dot" aria-hidden="true" />
          {item.severity}
        </div>
        <div
          className="text-muted text-xs"
          style={{ marginTop: "var(--space-1)" }}
        >
          {labelStage(item.mule_stage)}
        </div>
      </div>

      <div>
        <div className="case-account font-mono">
          <Highlight text={item.account} query={query} />
        </div>
        <div className="case-signal">
          <Highlight text={item.reasons.join(" · ")} query={query} />
        </div>
      </div>

      {!compact && (
        <div className="case-score" aria-hidden="true">
          {Math.round(item.risk_score)}
          <span className="text-muted text-xs"> /100</span>
        </div>
      )}

      {compact && (
        <div
          style={{
            display: "flex",
            justifyContent: "space-between",
            marginTop: "var(--space-1)",
          }}
        >
          <span className="case-account font-mono text-xs">
            <Highlight text={item.account} query={query} />
          </span>
          <strong className="font-mono text-sm">
            {Math.round(item.risk_score)}
          </strong>
        </div>
      )}
    </button>
  );
});
