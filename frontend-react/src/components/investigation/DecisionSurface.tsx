// ============================================================
// MuleShield — DecisionSurface
// Central panel: animated score, contributor bars, recommendation,
// analyst decision capture, and timeline.
// ============================================================

import { memo } from "react";
import { AnimatePresence, motion } from "framer-motion";
import { recommendationFor, severityClass } from "../../utils/caseUtils";
import { InvestigationTimeline } from "./InvestigationTimeline";
import type { AnalystDecision, CaseItem } from "../../types";

interface DecisionSurfaceProps {
  item: CaseItem;
  counterVal: number;
  unfoldProgress: number;
  onSkipUnfold: () => void;
  hoveredDimension: "profile" | "transaction" | "network" | null;
  analystDecision: AnalystDecision;
  onSetDecision: (d: AnalystDecision) => void;
  onNotify: (msg: string) => void;
}

export const DecisionSurface = memo(function DecisionSurface({
  item,
  counterVal,
  unfoldProgress,
  onSkipUnfold,
  hoveredDimension,
  analystDecision,
  onSetDecision,
  onNotify,
}: DecisionSurfaceProps) {
  const unfoldStatus =
    unfoldProgress === 0
      ? "Assembling composite risk profile... [ML model active]"
      : unfoldProgress === 1
      ? "Correlating profile with transaction telemetry... [Dual engines active]"
      : "Risk fusion complete. Network evidence correlated.";

  return (
    <section className="card card-focal" aria-label="Decision surface">
      <div className="section-head">
        <div className="eyebrow">Decision surface</div>
        {unfoldProgress < 3 && (
          <button
            className="skip-btn"
            onClick={onSkipUnfold}
            aria-label="Skip investigation unfolding animation"
          >
            Skip Unfolding
          </button>
        )}
      </div>

      {/* Animated score */}
      <div className="score-wrap">
        <div
          className="score-number"
          aria-label={`Risk score: ${counterVal} out of 100`}
        >
          {counterVal}
          <span> / 100</span>
        </div>
        <div>
          <div
            className={`status-badge severity-${severityClass(item.severity)}`}
          >
            <span className="status-dot" aria-hidden="true" />
            {item.severity} risk
          </div>
          <p
            className="score-copy"
            style={{ marginTop: "var(--space-2)" }}
            aria-live="polite"
          >
            {unfoldStatus}
          </p>
        </div>
      </div>

      {/* Contributor bars */}
      <div className="bar-group" aria-label="Risk contributor scores">
        {unfoldProgress >= 0 && (
          <motion.div
            initial={{ opacity: 0, y: 4 }}
            animate={{ opacity: 1, y: 0 }}
            className={
              hoveredDimension === "profile" ? "highlighted-bar" : ""
            }
          >
            <div className="bar-head">
              <span>
                Profile behavior{" "}
                <span className="text-muted">· 40% weight</span>
              </span>
              <span className="font-mono">{item.profile_risk.toFixed(0)}</span>
            </div>
            <div
              className="bar-track"
              role="progressbar"
              aria-valuenow={item.profile_risk}
              aria-valuemin={0}
              aria-valuemax={100}
              aria-label="Profile risk"
            >
              <div
                className="bar-fill"
                style={{ width: `${item.profile_risk}%` }}
              />
            </div>
          </motion.div>
        )}

        {unfoldProgress >= 1 && (
          <motion.div
            initial={{ opacity: 0, y: 4 }}
            animate={{ opacity: 1, y: 0 }}
            className={
              hoveredDimension === "transaction" ? "highlighted-bar" : ""
            }
          >
            <div className="bar-head">
              <span>
                Transaction behavior{" "}
                <span className="text-muted">· 40% weight</span>
              </span>
              <span className="font-mono">
                {item.transaction_risk.toFixed(0)}
              </span>
            </div>
            <div
              className="bar-track"
              role="progressbar"
              aria-valuenow={item.transaction_risk}
              aria-valuemin={0}
              aria-valuemax={100}
              aria-label="Transaction risk"
            >
              <div
                className="bar-fill"
                style={{ width: `${item.transaction_risk}%` }}
              />
            </div>
          </motion.div>
        )}

        {unfoldProgress >= 2 && (
          <motion.div
            initial={{ opacity: 0, y: 4 }}
            animate={{ opacity: 1, y: 0 }}
            className={
              hoveredDimension === "network" ? "highlighted-bar" : ""
            }
          >
            <div className="bar-head">
              <span>
                Network context{" "}
                <span className="text-muted">· 20% weight</span>
              </span>
              <span className="font-mono">{item.graph_risk.toFixed(0)}</span>
            </div>
            <div
              className="bar-track"
              role="progressbar"
              aria-valuenow={item.graph_risk}
              aria-valuemin={0}
              aria-valuemax={100}
              aria-label="Network risk"
            >
              <div
                className="bar-fill"
                style={{ width: `${item.graph_risk}%` }}
              />
            </div>
          </motion.div>
        )}
      </div>

      {/* Recommendation + Analyst Decision */}
      <AnimatePresence>
        {unfoldProgress >= 3 && (
          <motion.div
            className="recommendation"
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.2 }}
          >
            <div className="eyebrow">Recommended next step</div>
            <strong>{recommendationFor(item.severity)}</strong>

            <div className="review-capture">
              <span className="text-muted text-xs">
                Confirm Analyst Decision:
              </span>
              <div
                style={{
                  display: "flex",
                  gap: "var(--space-2)",
                  marginTop: "var(--space-2)",
                  flexWrap: "wrap",
                }}
              >
                <button
                  className={`chip-btn${analystDecision === "APPROVED" ? " active" : ""}`}
                  onClick={() => {
                    onSetDecision("APPROVED");
                    onNotify("Marked as Approved.");
                  }}
                  aria-pressed={analystDecision === "APPROVED"}
                >
                  Approve AI recommendation
                </button>
                <button
                  className={`chip-btn${analystDecision === "ESCALATED" ? " active" : ""}`}
                  onClick={() => {
                    onSetDecision("ESCALATED");
                    onNotify("Escalated manually.");
                  }}
                  aria-pressed={analystDecision === "ESCALATED"}
                >
                  Escalate manually
                </button>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Timeline */}
      {unfoldProgress >= 3 && (
        <motion.div
          style={{ marginTop: "var(--space-7)" }}
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
        >
          <InvestigationTimeline
            currentStage={item.mule_stage}
            highlightedDimension={hoveredDimension}
            item={item}
          />
        </motion.div>
      )}
    </section>
  );
});
