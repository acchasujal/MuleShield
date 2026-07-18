// ============================================================
// MuleShield — Cases Page
// ============================================================

import { useMemo } from "react";
import { useNavigate } from "react-router-dom";
import { Sparkles, Upload } from "lucide-react";
import { useAppContext } from "../contexts/AppContext";
import { useUpload } from "../hooks/useUpload";
import { FALLBACK_CASES } from "../data/fallbackCases";
import { StatCard } from "../components/ui/StatCard";
import { CaseRow } from "../components/cases/CaseRow";

interface CasesPageProps {
  query: string;
}

export function CasesPage({ query }: CasesPageProps) {
  const navigate = useNavigate();
  const {
    cases,
    setCases,
    setSelectedId,
    setPackageReady,
    setUnfoldProgress,
    notify,
  } = useAppContext();

  const filtered = useMemo(
    () =>
      cases.filter((item) =>
        `${item.account} ${item.severity} ${item.mule_stage} ${item.reasons.join(" ")}`
          .toLowerCase()
          .includes(query.toLowerCase())
      ),
    [cases, query]
  );

  const critical = filtered.filter((c) => c.severity === "CRITICAL").length;
  const high = filtered.filter((c) => c.severity === "HIGH").length;
  const review = filtered.filter((c) => c.severity !== "LOW").length;

  const runGuided = () => {
    setCases(FALLBACK_CASES);
    setSelectedId(FALLBACK_CASES[0].account);
    setPackageReady(FALLBACK_CASES[0].account, false);
    setUnfoldProgress(FALLBACK_CASES[0].account, 0);
    notify("Guided investigation loaded from mock provider.");
    navigate("/investigate");
  };

  const handleSelect = (account: string) => {
    setSelectedId(account);
    setPackageReady(account, false);
    navigate("/investigate");
  };

  const handleUploadSuccess = (
    incomingCases: typeof cases,
    firstId: string
  ) => {
    setCases(incomingCases);
    setSelectedId(firstId);
    navigate("/investigate");
  };

  const handleUpload = useUpload({
    onSuccess: handleUploadSuccess,
    onFallback: runGuided,
    notify,
  });

  return (
    <>
      {/* Page heading */}
      <div className="page-heading">
        <div>
          <div className="eyebrow">Cases / Priority queue</div>
          <h1>Good morning, Analyst.</h1>
          <p className="text-muted" style={{ marginTop: "var(--space-2)" }}>
            {filtered.length} signal{filtered.length !== 1 ? "s" : ""} need a
            defensible next move.
          </p>
        </div>
        <div className="page-heading-actions">
          <label className="btn" role="button" tabIndex={0}>
            <Upload size={15} aria-hidden="true" />
            Upload batch
            <input
              hidden
              type="file"
              accept=".csv"
              aria-label="Upload CSV batch file"
              onChange={(e) =>
                e.target.files?.[0] && handleUpload(e.target.files[0])
              }
            />
          </label>
          <button className="btn btn-primary" onClick={runGuided}>
            <Sparkles size={15} aria-hidden="true" />
            Run guided investigation
          </button>
        </div>
      </div>

      {/* Summary stats */}
      <div className="grid grid-4" style={{ marginBottom: "var(--space-5)" }}>
        <StatCard
          label="Critical cases"
          value={String(critical)}
          detail="Immediate review"
          severity="CRITICAL"
        />
        <StatCard
          label="High priority"
          value={String(high)}
          detail="Priority queue"
          severity="HIGH"
        />
        <StatCard
          label="Awaiting decision"
          value={String(review)}
          detail="Across current batch"
          severity="MEDIUM"
        />
        <StatCard
          label="Evidence sealed"
          value="12"
          detail="Review-ready packages"
          severity="LOW"
        />
      </div>

      {/* Two-column layout */}
      <div className="grid grid-2">
        {/* Case queue */}
        <section className="card" aria-label="Priority case queue">
          <div className="section-head">
            <div>
              <h2>Priority queue</h2>
              <div className="text-muted text-sm" style={{ marginTop: "var(--space-1)" }}>
                Ranked by composite risk and lifecycle urgency
              </div>
            </div>
            <span className="eyebrow">{filtered.length} cases</span>
          </div>
          <div className="case-list" role="list" aria-label="Case list">
            {filtered.length === 0 ? (
              <div className="empty-state">
                No cases match your search.
              </div>
            ) : (
              filtered.map((item, index) => (
                <CaseRow
                  key={item.account}
                  item={item}
                  selected={index === 0}
                  onClick={() => handleSelect(item.account)}
                  query={query}
                />
              ))
            )}
          </div>
        </section>

        {/* Guided investigation CTA */}
        <section className="card card-focal" aria-label="Guided investigation">
          <div className="eyebrow">Guided investigation</div>
          <h2 style={{ marginTop: "var(--space-3)" }}>
            Make the next decision visible.
          </h2>
          <p
            className="text-muted"
            style={{ lineHeight: "var(--leading-relaxed)", marginTop: "var(--space-3)" }}
          >
            Open a prepared scenario to see how MuleShield turns profile,
            transaction, and network signals into an explainable handoff.
          </p>
          <div className="callout">
            <div className="status-badge severity-critical">
              <span className="status-dot" aria-hidden="true" />
              Critical case ready
            </div>
            <p
              className="text-muted text-xs"
              style={{ marginTop: "var(--space-2)" }}
            >
              Dormant reactivation · velocity · linked accounts
            </p>
          </div>
          <button
            className="btn btn-primary"
            style={{ marginTop: "var(--space-6)" }}
            onClick={runGuided}
          >
            Open case workspace →
          </button>
        </section>
      </div>
    </>
  );
}
