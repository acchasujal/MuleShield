// ============================================================
// MuleShield — Topbar
// ============================================================

import { memo } from "react";
import { useLocation } from "react-router-dom";
import { Search, Terminal } from "lucide-react";

interface TopbarProps {
  query: string;
  onQueryChange: (q: string) => void;
  onOpenCommandPalette: () => void;
}

export const Topbar = memo(function Topbar({
  query,
  onQueryChange,
  onOpenCommandPalette,
}: TopbarProps) {
  const { pathname } = useLocation();
  const page = pathname.replace("/", "") || "cases";

  return (
    <header className="topbar" role="banner">
      <div className="topbar-breadcrumb" aria-label="Current location">
        <span className="topbar-breadcrumb-root">MuleShield</span>
        <span className="topbar-breadcrumb-sep" aria-hidden="true">/</span>
        <span className="topbar-breadcrumb-page">{page}</span>
      </div>

      <div className="topbar-actions">
        <button
          className="cmd-trigger-btn"
          onClick={onOpenCommandPalette}
          aria-label="Open command palette (Ctrl+K)"
          title="Ctrl+K"
        >
          <Terminal size={12} aria-hidden="true" />
          Command
          <kbd aria-hidden="true">⌃K</kbd>
        </button>

        <label className="search-field" aria-label="Search cases">
          <Search size={14} aria-hidden="true" />
          <input
            value={query}
            onChange={(e) => onQueryChange(e.target.value)}
            placeholder="Search cases..."
            aria-label="Filter cases by account, severity, or stage"
            type="search"
          />
        </label>

        <div
          className="avatar"
          role="img"
          aria-label="Analyst account: AR"
          title="Analyst workspace"
        >
          AR
        </div>
      </div>
    </header>
  );
});
