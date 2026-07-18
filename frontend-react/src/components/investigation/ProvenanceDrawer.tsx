// ============================================================
// MuleShield — ProvenanceDrawer
// Sliding side panel showing SHAP values, weights, diagnostics.
// ============================================================

import { memo } from "react";
import { AnimatePresence, motion } from "framer-motion";
import { X } from "lucide-react";
import { SIGNAL_NAMES } from "../../constants";
import type { CaseItem } from "../../types";

interface ProvenanceDrawerProps {
  isOpen: boolean;
  onClose: () => void;
  item: CaseItem;
}

export const ProvenanceDrawer = memo(function ProvenanceDrawer({
  isOpen,
  onClose,
  item,
}: ProvenanceDrawerProps) {
  return (
    <AnimatePresence>
      {isOpen && (
        <>
          {/* Backdrop */}
          <motion.div
            className="drawer-overlay"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.2 }}
            onClick={onClose}
            aria-hidden="true"
          />

          {/* Panel */}
          <motion.div
            role="dialog"
            aria-modal="true"
            aria-label="Technical provenance panel"
            className="drawer-panel"
            initial={{ x: "100%" }}
            animate={{ x: 0 }}
            exit={{ x: "100%" }}
            transition={{ type: "tween", duration: 0.25, ease: [0.16, 1, 0.3, 1] }}
          >
            <div className="drawer-header">
              <h3>Technical Provenance</h3>
              <button
                className="close-btn"
                onClick={onClose}
                aria-label="Close provenance panel"
              >
                <X size={16} aria-hidden="true" />
              </button>
            </div>

            <div className="drawer-body">
              {/* Risk weights */}
              <div className="drawer-section">
                <h4>Fused Risk Contributors (40/40/20)</h4>
                <dl style={{ marginTop: "var(--space-3)" }}>
                  {[
                    ["Profile Weight", "40%"],
                    ["Transaction Weight", "40%"],
                    ["Graph Weight", "20%"],
                  ].map(([label, value]) => (
                    <div className="factor-row" key={label}>
                      <dt className="text-muted">{label}</dt>
                      <dd className="font-semibold">{value}</dd>
                    </div>
                  ))}
                </dl>
              </div>

              {/* SHAP values */}
              <div className="drawer-section">
                <h4>Feature Explainer Weights (SHAP)</h4>
                <dl style={{ marginTop: "var(--space-3)" }}>
                  {Object.entries(item.shap_signals).map(([key, value]) => (
                    <div className="factor-row" key={key}>
                      <dt className="text-muted">
                        {SIGNAL_NAMES[key] ?? key}
                      </dt>
                      <dd className="font-mono text-sm">
                        {Number(value).toFixed(2)}
                      </dd>
                    </div>
                  ))}
                </dl>
              </div>

              {/* Diagnostics */}
              <div className="drawer-section">
                <h4>Diagnostics &amp; Fallbacks</h4>
                <p
                  className="text-muted text-sm"
                  style={{ lineHeight: "var(--leading-relaxed)", marginTop: "var(--space-2)" }}
                >
                  Platform running under STANDALONE ML MODE. Graph relationship
                  outputs are mapped from static topology files because Neo4j is
                  offline.
                </p>
              </div>
            </div>
          </motion.div>
        </>
      )}
    </AnimatePresence>
  );
});
