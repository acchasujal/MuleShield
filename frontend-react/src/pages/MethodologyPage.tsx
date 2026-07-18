// ============================================================
// MuleShield — Methodology Page
// ============================================================

import { Info } from "lucide-react";
import { METHODOLOGY_WEIGHTS } from "../constants";
import { WeightCard } from "../components/methodology/WeightCard";

export function MethodologyPage() {
  return (
    <>
      <div className="page-heading">
        <div>
          <div className="eyebrow">Methodology / Provenance</div>
          <h1>How the decision is formed.</h1>
          <p className="text-muted" style={{ marginTop: "var(--space-2)" }}>
            Technical context stays available without taking over the
            investigation.
          </p>
        </div>
        <div className="status-badge severity-low">
          <span className="status-dot" aria-hidden="true" />
          Backend unchanged
        </div>
      </div>

      {/* Weight cards */}
      <div className="grid grid-method">
        {METHODOLOGY_WEIGHTS.map((w) => (
          <WeightCard key={w.label} {...w} />
        ))}
      </div>

      {/* Decision boundary */}
      <div className="card" style={{ marginTop: "var(--space-4)" }}>
        <div className="eyebrow">Decision boundary</div>
        <h2 style={{ marginTop: "var(--space-2)" }}>
          Evidence before automation.
        </h2>
        <div className="callout">
          <div
            style={{
              display: "flex",
              alignItems: "flex-start",
              gap: "var(--space-3)",
            }}
          >
            <Info size={16} color="var(--color-accent-muted)" aria-hidden="true" />
            <p
              className="text-muted text-sm"
              style={{ lineHeight: "var(--leading-relaxed)" }}
            >
              MuleShield presents a risk recommendation and prepares evidence
              for investigator review. It does not automatically freeze an
              account or claim that a report has been submitted.
            </p>
          </div>
        </div>

        <div className="grid grid-2" style={{ marginTop: "var(--space-4)" }}>
          <div>
            <h3>Graceful degradation</h3>
            <p
              className="text-muted text-sm"
              style={{ lineHeight: "var(--leading-relaxed)", marginTop: "var(--space-2)" }}
            >
              If network enrichment is unavailable, profile and transaction
              evidence remain visible and the limitation is explicit.
            </p>
          </div>
          <div>
            <h3>Traceable narrative</h3>
            <p
              className="text-muted text-sm"
              style={{ lineHeight: "var(--leading-relaxed)", marginTop: "var(--space-2)" }}
            >
              Case briefs are generated from response fields and mapped feature
              labels, not an unconstrained chatbot.
            </p>
          </div>
        </div>
      </div>
    </>
  );
}
