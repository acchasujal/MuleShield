// ============================================================
// MuleShield — CaseBrief
// Right panel: explanation, SHAP signals, network diagram,
// and provenance drawer trigger.
// ============================================================

import { memo, useState } from "react";
import { motion } from "framer-motion";
import { Check, Eye } from "lucide-react";
import { briefFor, shapKeyToDimension } from "../../utils/caseUtils";
import { NetworkDiagram } from "./NetworkDiagram";
import { ProvenanceDrawer } from "./ProvenanceDrawer";
import type { CaseItem } from "../../types";

interface CaseBriefProps {
  item: CaseItem;
  unfoldProgress: number;
  onHoverDimension: (dim: "profile" | "transaction" | "network" | null) => void;
}

export const CaseBrief = memo(function CaseBrief({
  item,
  unfoldProgress,
  onHoverDimension,
}: CaseBriefProps) {
  const [isDrawerOpen, setIsDrawerOpen] = useState(false);
  const brief = briefFor(item);

  return (
    <section className="card" aria-label="Case brief">
      <div className="eyebrow">Case brief</div>
      <h2 style={{ marginTop: "var(--space-2)" }}>Why this case was flagged</h2>
      <p
        className="text-muted text-sm"
        style={{ lineHeight: "var(--leading-relaxed)", marginTop: "var(--space-3)" }}
      >
        {item.explanation}
      </p>

      {/* SHAP signal links */}
      <ul
        className="brief-list"
        aria-label="Key risk signals"
        role="list"
      >
        {brief.map(({ key, text }, idx) =>
          unfoldProgress >= idx ? (
            <motion.li
              key={key}
              className="brief-item linkable"
              role="listitem"
              initial={{ opacity: 0, x: -4 }}
              animate={{ opacity: 1, x: 0 }}
              onMouseEnter={() => onHoverDimension(shapKeyToDimension(key))}
              onMouseLeave={() => onHoverDimension(null)}
              tabIndex={0}
              onFocus={() => onHoverDimension(shapKeyToDimension(key))}
              onBlur={() => onHoverDimension(null)}
              aria-label={`Signal: ${text}`}
            >
              <Check size={15} aria-hidden="true" />
              <span>
                {text}{" "}
                <span className="link-arrow" aria-hidden="true">→</span>
              </span>
            </motion.li>
          ) : null
        )}
      </ul>

      {/* Network diagram */}
      {unfoldProgress >= 2 && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          style={{ marginTop: "var(--space-5)" }}
        >
          <div className="eyebrow" style={{ marginBottom: "var(--space-1)" }}>
            Network evidence
          </div>
          <NetworkDiagram
            subjectAccount={item.account}
            highlighted={false}
          />
        </motion.div>
      )}

      <button
        className="btn btn-ghost"
        style={{ marginTop: "var(--space-5)", width: "100%", justifyContent: "center" }}
        onClick={() => setIsDrawerOpen(true)}
        aria-label="View technical provenance for this case"
        aria-expanded={isDrawerOpen}
      >
        <Eye size={14} aria-hidden="true" />
        View Technical Provenance
      </button>

      <ProvenanceDrawer
        isOpen={isDrawerOpen}
        onClose={() => setIsDrawerOpen(false)}
        item={item}
      />
    </section>
  );
});
