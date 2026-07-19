// ============================================================
// MuleShield — Sidebar
// ============================================================

import { memo } from "react";
import { NavLink } from "react-router-dom";
import { ShieldCheck, RefreshCw } from "lucide-react";
import { NAV_ITEMS } from "../../constants";

interface SidebarProps {
  offlineMode: boolean;
  onReset: () => void;
}

export const Sidebar = memo(function Sidebar({
  offlineMode,
  onReset,
}: SidebarProps) {
  return (
    <aside className="sidebar" aria-label="Main navigation">
      {/* Brand */}
      <div className="brand">
        <div className="brand-mark" aria-hidden="true">M</div>
        <div>
          <div className="brand-name">MuleShield AI</div>
          <div className="brand-sub">Financial Trust Infra</div>
        </div>
      </div>

      {/* Navigation */}
      <nav aria-label="Workspace navigation">
        <p className="nav-section-label">Workspace</p>
        <ul className="nav" role="list">
          {NAV_ITEMS.map(({ label, path, icon: Icon }) => (
            <li key={path} role="listitem">
              <NavLink
                to={path}
                className={({ isActive }) =>
                  `nav-link${isActive ? " active" : ""}`
                }
                aria-label={label}
              >
                <Icon size={16} aria-hidden="true" />
                <span>{label}</span>
              </NavLink>
            </li>
          ))}
        </ul>
      </nav>

      {/* Footer */}
      <div className="sidebar-bottom">
        <div className="sidebar-status">
          <ShieldCheck size={15} color="var(--color-success)" aria-hidden="true" />
          <p className="sidebar-status-title">
            {offlineMode ? "Demo Mode Active" : "Operational Mode"}
          </p>
          <p className="sidebar-status-desc">
            {offlineMode
              ? "Resilient fallback fixture loaded without external APIs."
              : "Connected to MuleShield active server API."}
          </p>
        </div>
        <button
          className="reset-btn"
          onClick={onReset}
          aria-label="Reset presentation state"
        >
          <RefreshCw size={12} aria-hidden="true" />
          Reset Presentation
        </button>
      </div>
    </aside>
  );
});
