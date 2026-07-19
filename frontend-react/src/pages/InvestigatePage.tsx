// ============================================================
// MuleShield — Investigate Page
// ============================================================

import { useCallback, useEffect, useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";
import { ArrowLeft, FileCheck2 } from "lucide-react";
import { useAppContext } from "../contexts/AppContext";
import { useCountUp } from "../hooks/useCountUp";
import { FALLBACK_CASES } from "../data/fallbackCases";
import { severityClass, formatAccount } from "../utils/caseUtils";
import { ScenarioSwitcher } from "../components/investigation/ScenarioSwitcher";
import { DecisionSurface } from "../components/investigation/DecisionSurface";
import { CaseBrief } from "../components/investigation/CaseBrief";
import { DecisionLedger } from "../components/investigation/DecisionLedger";
import { CaseRow } from "../components/cases/CaseRow";
import type { CaseItem, PrepareState } from "../types";

interface InvestigatePageProps {
  query: string;
}

export function InvestigatePage({ query }: InvestigatePageProps) {
  const navigate = useNavigate();
  const {
    cases,
    selectedCase,
    setSelectedId,
    analystDecisions,
    setAnalystDecision,
    packageReady,
    setPackageReady,
    unfoldProgress,
    setUnfoldProgress,
    notify,
    setCases,
  } = useAppContext();

  const item = selectedCase;
  const account = item.account;
  const progress = unfoldProgress[account] ?? 0;
  const pkgReady = packageReady[account] ?? false;
  const analystDecision = analystDecisions[account] ?? "PENDING";

  // ── Hover linkage ─────────────────────────────────────────
  const [hoveredDimension, setHoveredDimension] = useState<
    "profile" | "transaction" | "network" | null
  >(null);

  // ── Evidence prepare state ────────────────────────────────
  const [prepareState, setPrepareState] = useState<PrepareState>(
    pkgReady ? "ready" : "idle"
  );

  // Reset prepare state when case changes
  useEffect(() => {
    setPrepareState(pkgReady ? "ready" : "idle");
  }, [account, pkgReady]);

  const handlePrepare = useCallback(() => {
    if (prepareState !== "idle") return;
    setPrepareState("preparing");
    setTimeout(() => {
      setPrepareState("sealing");
      setTimeout(() => {
        setPrepareState("verified");
        setTimeout(() => {
          setPrepareState("ready");
          setPackageReady(account, true);
          notify("Evidence hash sealed and locked in Case Ledger.");
        }, 400);
      }, 400);
    }, 400);
  }, [prepareState, account, setPackageReady, notify]);

  const prepareLabel =
    prepareState === "idle"
      ? "Prepare Evidence"
      : prepareState === "preparing"
      ? "Reading Metadata..."
      : prepareState === "sealing"
      ? "Computing Cryptographic Seal..."
      : prepareState === "verified"
      ? "Verifying SHA-256 integrity..."
      : "Evidence Package Ready";

  // ── Auto unfold ───────────────────────────────────────────
  useEffect(() => {
    if (progress >= 3) return;
    const timer = setTimeout(() => {
      setUnfoldProgress(account, progress + 1);
    }, 1200);
    return () => clearTimeout(timer);
  }, [progress, account, setUnfoldProgress]);

  // ── Score target ──────────────────────────────────────────
  const targetScore = useMemo(() => {
    if (progress === 0) return Math.round(item.profile_risk * 0.4);
    if (progress === 1)
      return Math.round(item.profile_risk * 0.4 + item.transaction_risk * 0.4);
    return Math.round(item.risk_score);
  }, [progress, item]);

  const counterVal = useCountUp(targetScore);

  // ── Filtered sidebar list ─────────────────────────────────
  const filtered = useMemo(
    () =>
      cases.filter((c) =>
        `${c.account} ${c.severity} ${c.mule_stage} ${c.reasons.join(" ")}`
          .toLowerCase()
          .includes(query.toLowerCase())
      ),
    [cases, query]
  );

  const handleSelect = useCallback(
    (candidate: CaseItem) => {
      setSelectedId(candidate.account);
      setPackageReady(candidate.account, false);
    },
    [setSelectedId, setPackageReady]
  );

  const handleRunGuided = useCallback(() => {
    setCases(FALLBACK_CASES);
    setSelectedId(FALLBACK_CASES[0].account);
    setPackageReady(FALLBACK_CASES[0].account, false);
    setUnfoldProgress(FALLBACK_CASES[0].account, 0);
    notify("Guided investigation loaded.");
  }, [setCases, setSelectedId, setPackageReady, setUnfoldProgress, notify]);

  return (
    <>
      {/* Scenario switcher */}
      <ScenarioSwitcher
        cases={filtered}
        activeAccount={account}
        onSelect={handleSelect}
      />

      {/* Case header */}
      <div className="case-header">
        <div className="case-header-left">
          <button
            className="btn"
            onClick={() => navigate("/cases")}
            aria-label="Back to cases list"
          >
            <ArrowLeft size={15} aria-hidden="true" />
            Cases
          </button>
          <span className="font-mono text-sm text-muted" title={account}>{formatAccount(account)}</span>
          <div className={`status-badge severity-${severityClass(item.severity)}`}>
            <span className="status-dot" aria-hidden="true" />
            {item.severity}
          </div>
        </div>
        <button
          className="btn btn-primary"
          onClick={handlePrepare}
          disabled={prepareState !== "idle" && prepareState !== "ready"}
          aria-label={prepareLabel}
        >
          <FileCheck2 size={15} aria-hidden="true" />
          {prepareLabel}
        </button>
      </div>

      {/* Three-column grid */}
      <div className="grid grid-investigate">
        {/* Left: Case queue */}
        <section className="card" aria-label="Case queue sidebar">
          <div className="section-head">
            <h3>Case queue</h3>
            <span className="eyebrow">{filtered.length}</span>
          </div>
          <div className="case-list" role="list">
            {filtered.map((candidate) => (
              <CaseRow
                key={candidate.account}
                item={candidate}
                selected={candidate.account === account}
                onClick={() => handleSelect(candidate)}
                query={query}
                compact
              />
            ))}
          </div>
        </section>

        {/* Center: Decision surface */}
        <DecisionSurface
          item={item}
          counterVal={counterVal}
          unfoldProgress={progress}
          onSkipUnfold={() => setUnfoldProgress(account, 3)}
          hoveredDimension={hoveredDimension}
          analystDecision={analystDecision}
          onSetDecision={(d) => setAnalystDecision(account, d)}
          onNotify={notify}
        />

        {/* Right: Case brief */}
        <CaseBrief
          item={item}
          unfoldProgress={progress}
          onHoverDimension={setHoveredDimension}
        />
      </div>

      {/* Bottom: Decision ledger (appears at progress ≥ 3) */}
      {progress >= 3 && (
        <DecisionLedger
          item={item}
          packageReady={pkgReady}
          analystDecision={analystDecision}
        />
      )}
    </>
  );
}
