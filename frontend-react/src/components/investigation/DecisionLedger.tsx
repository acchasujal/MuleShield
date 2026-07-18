// ============================================================
// MuleShield — DecisionLedger
// Bottom panel: chronological evidence chain.
// ============================================================

import { memo } from "react";
import { motion } from "framer-motion";
import type { AnalystDecision, CaseItem } from "../../types";

interface DecisionLedgerProps {
  item: CaseItem;
  packageReady: boolean;
  analystDecision: AnalystDecision;
}

const LEDGER_STEPS = [
  "Signal detected",
  "Evidence reviewed",
  "Recommendation recorded",
] as const;

export const DecisionLedger = memo(function DecisionLedger({
  item,
  packageReady,
  analystDecision,
}: DecisionLedgerProps) {
  const getDetail = (index: number): string => {
    if (index === 0) return item.reasons[0] ?? "Risk signal";
    if (index === 1) return "Profile and transaction context correlated";
    return packageReady
      ? `Decision finalized: ${analystDecision}`
      : "Awaiting investigator review";
  };

  return (
    <motion.section
      className="card"
      style={{ marginTop: "var(--space-4)" }}
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      aria-label="Evidence timeline"
    >
      <div className="section-head">
        <div>
          <div className="eyebrow">Evidence timeline</div>
          <h2 style={{ marginTop: "var(--space-2)" }}>
            From signal to accountable handoff
          </h2>
        </div>
        <span className="text-muted text-sm">
          {item.evidence.length} transaction record
          {item.evidence.length !== 1 ? "s" : ""}
        </span>
      </div>

      <div className="grid grid-3" style={{ gap: "var(--space-3)" }}>
        {LEDGER_STEPS.map((label, index) => (
          <div className="callout" key={label} style={{ marginTop: 0 }}>
            <div className="status-badge severity-low">
              <span className="status-dot" aria-hidden="true" />
              {index < 2 || packageReady ? "Complete" : "Ready"}
            </div>
            <div
              className="font-semibold text-sm"
              style={{ marginTop: "var(--space-2)" }}
            >
              {label}
            </div>
            <div
              className="text-muted text-xs"
              style={{ marginTop: "var(--space-1)" }}
            >
              {getDetail(index)}
            </div>
          </div>
        ))}
      </div>
    </motion.section>
  );
});
