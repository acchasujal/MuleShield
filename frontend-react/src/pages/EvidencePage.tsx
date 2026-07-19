// ============================================================
// MuleShield — Evidence Page
// ============================================================

import { useEffect, useState } from "react";
import { FileCheck2, FileText, ClipboardCheck, ShieldCheck } from "lucide-react";
import { useAppContext } from "../contexts/AppContext";
import { severityClass, labelStage, formatAccount } from "../utils/caseUtils";
import { downloadText } from "../utils/download";

export function EvidencePage() {
  const {
    cases,
    selectedCase,
    packageReady,
    setPackageReady,
    analystDecisions,
    notify,
  } = useAppContext();

  const item = selectedCase;
  const account = item.account;
  const pkgReady = packageReady[account] ?? false;
  const analystDecision = analystDecisions[account] ?? "PENDING";

  // Ledger stamp animation
  const [stampStage, setStampStage] = useState(0);
  useEffect(() => {
    setStampStage(0);
    const t1 = setTimeout(() => {
      setStampStage(1);
      const t2 = setTimeout(() => setStampStage(2), 250);
      return () => clearTimeout(t2);
    }, 250);
    return () => clearTimeout(t1);
  }, [account]);

  const handleSeal = () => {
    setPackageReady(account, true);
    notify("Evidence package successfully sealed.");
  };

  return (
    <>
      {/* Page heading */}
      <div className="page-heading">
        <div>
          <div className="eyebrow">Evidence / Handoff</div>
          <h1>Evidence packages.</h1>
          <p className="text-muted" style={{ marginTop: "var(--space-2)" }}>
            Make every recommendation reviewable and exportable.
          </p>
        </div>
        <button
          className="btn btn-primary"
          onClick={handleSeal}
          aria-label={pkgReady ? "Package already sealed" : "Seal evidence package"}
        >
          <FileCheck2 size={15} aria-hidden="true" />
          {pkgReady ? "Package Sealed" : "Seal selected package"}
        </button>
      </div>

      {/* Two-column grid */}
      <div className="grid grid-2">
        {/* Left: Package list + ledger */}
        <section className="card" aria-label="Evidence packages">
          <div className="section-head">
            <h2>Packages</h2>
            <span className="eyebrow">{cases.length} records</span>
          </div>

          <div className="case-list" role="list">
            {cases
              .filter((c) => c.severity !== "LOW")
              .map((candidate, index) => (
                <div
                  key={candidate.case_id}
                  className="case-row"
                  style={{ gridTemplateColumns: "1fr 72px" }}
                  role="listitem"
                  aria-label={`Case ${candidate.case_id}, ${candidate.severity}`}
                >
                  <div>
                    <div
                      className={`status-badge severity-${severityClass(candidate.severity)}`}
                    >
                      <span className="status-dot" aria-hidden="true" />
                      {candidate.severity}
                    </div>
                    <div className="case-account font-mono" style={{ marginTop: "var(--space-1)" }}>
                      {candidate.case_id}
                    </div>
                    <div className="case-signal">
                      {formatAccount(candidate.account)} ·{" "}
                      {index === 0 || pkgReady ? "Sealed" : "Draft"}
                    </div>
                  </div>
                  <div className="case-score">{Math.round(candidate.risk_score)}</div>
                </div>
              ))}
          </div>

          {/* Decision ledger */}
          <div className="callout" style={{ marginTop: "var(--space-5)" }}>
            <div className="eyebrow">Decision Ledger</div>
            <p
              className="text-muted text-sm"
              style={{ marginTop: "var(--space-2)", lineHeight: "var(--leading-relaxed)" }}
            >
              The ledger records the signal, recommendation, analyst review
              state, and integrity hash as one case event.
            </p>
            <div
              className="ledger-preview"
              role="log"
              aria-label="Case event ledger"
              aria-live="polite"
            >
              {stampStage >= 0 && (
                <div className="ledger-row">
                  <span className="stamp-chip">DETECTED</span>
                  <span className="text-muted text-xs font-mono">
                    19 Jul 2026 02:22 UTC
                  </span>
                </div>
              )}
              {stampStage >= 1 && (
                <div className="ledger-row">
                  <span className="stamp-chip">RECOMMENDED</span>
                  <span className="text-muted text-xs font-mono">
                    19 Jul 2026 02:23 UTC
                  </span>
                </div>
              )}
              {stampStage >= 2 && (
                <div className="ledger-row">
                  <span className="stamp-chip">
                    {pkgReady ? `SEALED (${analystDecision})` : "DRAFT"}
                  </span>
                  <span className="text-muted text-xs font-mono">
                    {pkgReady ? "19 Jul 2026 02:24 UTC" : "PENDING REVIEW"}
                  </span>
                </div>
              )}
            </div>
          </div>
        </section>

        {/* Right: Report preview */}
        <section className="card" aria-label="Report-ready package">
          <div className="eyebrow">Report-ready package</div>
          <h2 style={{ marginTop: "var(--space-2)" }} title={account}>Case {formatAccount(account)}</h2>

          <div className="report-preview" style={{ marginTop: "var(--space-5)" }}>
            <div className="eyebrow">MuleShield AI · Investigation report</div>
            <h2>Suspicious activity case brief</h2>

            <dl>
              {[
                ["Case reference", <span className="font-mono">{item.case_id}</span>],
                [
                  "Composite assessment",
                  `${Math.round(item.risk_score)} / 100 · ${item.severity}`,
                ],
                ["Lifecycle stage", labelStage(item.mule_stage)],
                ["Analyst Status", <strong>{analystDecision}</strong>],
              ].map(([label, value]) => (
                <div className="report-row" key={String(label)}>
                  <dt>{label}</dt>
                  <dd>{value}</dd>
                </div>
              ))}
            </dl>

            <div className="report-rule" />
            <p style={{ fontSize: "var(--text-base)", lineHeight: "var(--leading-relaxed)" }}>
              {item.explanation}
            </p>
            <div className="report-rule" />
            <p
              style={{
                fontSize: "var(--text-xs)",
                color: "#71727b",
                lineHeight: "var(--leading-relaxed)",
              }}
            >
              This package is prepared for investigator review and export. It
              does not execute automatic account freezing or regulatory
              submission.
            </p>
          </div>

          {/* Integrity hash */}
          <div
            className="hash-block"
            style={{ marginTop: "var(--space-4)" }}
            aria-label="Evidence integrity hash"
          >
            <ShieldCheck size={18} color="var(--color-success)" aria-hidden="true" />
            <div>
              <div
                className="eyebrow"
                style={{ color: "var(--color-success)" }}
              >
                Evidence integrity · {pkgReady ? "sealed" : "available"}
              </div>
              <code>{item.evidence_hash}</code>
            </div>
          </div>

          {/* Export actions */}
          <div
            style={{
              display: "flex",
              gap: "var(--space-2)",
              marginTop: "var(--space-4)",
              flexWrap: "wrap",
            }}
          >
            <button
              className="btn"
              onClick={() =>
                downloadText(
                  item.goaml_xml || `<case>${item.case_id}</case>`,
                  `${item.case_id}.xml`
                )
              }
              aria-label="Export case as goAML XML"
            >
              <FileText size={15} aria-hidden="true" />
              Export XML
            </button>
            <button
              className="btn btn-ghost"
              onClick={() =>
                downloadText(
                  JSON.stringify(item, null, 2),
                  `${item.case_id}.json`
                )
              }
              aria-label="Export case as JSON"
            >
              <ClipboardCheck size={15} aria-hidden="true" />
              Export case JSON
            </button>
          </div>
        </section>
      </div>
    </>
  );
}
