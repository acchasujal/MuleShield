// ============================================================
// MuleShield — ScenarioSwitcher
// Quick-switch chips between cases in Investigation view.
// ============================================================

import { memo } from "react";
import type { CaseItem } from "../../types";

interface ScenarioSwitcherProps {
  cases: CaseItem[];
  activeAccount: string;
  onSelect: (item: CaseItem) => void;
}

export const ScenarioSwitcher = memo(function ScenarioSwitcher({
  cases,
  activeAccount,
  onSelect,
}: ScenarioSwitcherProps) {
  return (
    <div
      className="scenario-switcher"
      role="group"
      aria-label="Quick scenario switch"
    >
      <span className="text-muted text-xs">Quick Scenarios:</span>
      {cases.map((c) => (
        <button
          key={c.account}
          className={`scenario-chip${c.account === activeAccount ? " active" : ""}`}
          onClick={() => onSelect(c)}
          aria-pressed={c.account === activeAccount}
          aria-label={`Switch to case ${c.account}, ${c.severity}`}
        >
          {c.account.slice(-4)} ({c.severity})
        </button>
      ))}
    </div>
  );
});
