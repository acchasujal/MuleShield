// ============================================================
// MuleShield — App Shell
//
// Root component: ~80 lines.
// Assembles layout, command palette, and routing.
// All business logic lives in pages, components, hooks, and context.
// ============================================================

import { useState, useCallback, useMemo } from "react";
import { useNavigate } from "react-router-dom";
import {
  Activity,
  BarChart3,
  FileCheck2,
  Home,
  RefreshCw,
  Sparkles,
} from "lucide-react";

import { useAppContext } from "./contexts/AppContext";
import { useCommandPalette } from "./hooks/useCommandPalette";
import type { Command } from "./hooks/useCommandPalette";
import { FALLBACK_CASES } from "./data/fallbackCases";

import { Sidebar } from "./components/layout/Sidebar";
import { Topbar } from "./components/layout/Topbar";
import { Toast } from "./components/ui/Toast";
import { CommandPalette } from "./components/command-palette/CommandPalette";
import { AppRouter } from "./app/Router";

export default function App() {
  const navigate = useNavigate();
  const {
    setCases,
    setSelectedId,
    setPackageReady,
    setUnfoldProgress,
    resetDemo,
    offlineMode,
    setOfflineMode,
    notify,
    toast,
  } = useAppContext();

  const [query, setQuery] = useState("");

  // ── Guided investigation ──────────────────────────────────
  const runGuided = useCallback(() => {
    setCases(FALLBACK_CASES);
    setSelectedId(FALLBACK_CASES[0].account);
    setPackageReady(FALLBACK_CASES[0].account, false);
    setUnfoldProgress(FALLBACK_CASES[0].account, 0);
    notify("Guided investigation loaded from mock provider.");
    navigate("/investigate");
  }, [setCases, setSelectedId, setPackageReady, setUnfoldProgress, notify, navigate]);

  // ── Command list ──────────────────────────────────────────
  const commands = useMemo<Command[]>(
    () => [
      {
        id: "guided",
        label: "Run Guided Investigation Scenario",
        category: "Demo",
        icon: Sparkles,
        shortcut: ["G"],
        action: runGuided,
      },
      {
        id: "reset",
        label: "Reset Presentation State",
        category: "Demo",
        icon: RefreshCw,
        shortcut: ["R"],
        action: () => {
          resetDemo();
        },
      },
      {
        id: "toggle-mode",
        label: `Toggle Connection Mode (${offlineMode ? "Simulated Offline" : "Live Web"})`,
        category: "Demo",
        icon: Activity,
        shortcut: ["O"],
        action: () => {
          setOfflineMode(!offlineMode);
          notify(
            `Connection mode: ${!offlineMode ? "Simulated Offline" : "Live Web"}`
          );
        },
      },
      {
        id: "nav-cases",
        label: "Navigate to Cases Queue",
        category: "Navigation",
        icon: Home,
        shortcut: ["1"],
        action: () => navigate("/cases"),
      },
      {
        id: "nav-investigate",
        label: "Navigate to Investigation Workspace",
        category: "Navigation",
        icon: Sparkles,
        shortcut: ["2"],
        action: () => navigate("/investigate"),
      },
      {
        id: "nav-evidence",
        label: "Navigate to Sealed Evidence Packages",
        category: "Navigation",
        icon: FileCheck2,
        shortcut: ["3"],
        action: () => navigate("/evidence"),
      },
      {
        id: "nav-methodology",
        label: "Navigate to Technical Methodology",
        category: "Navigation",
        icon: BarChart3,
        shortcut: ["4"],
        action: () => navigate("/methodology"),
      },
    ],
    [
      runGuided,
      resetDemo,
      offlineMode,
      setOfflineMode,
      notify,
      navigate,
    ]
  );

  // ── Command palette ───────────────────────────────────────
  const palette = useCommandPalette(commands);

  return (
    <div className="app">
      <Sidebar offlineMode={offlineMode} onReset={resetDemo} />

      <main className="main" id="main-content">
        <Topbar
          query={query}
          onQueryChange={setQuery}
          onOpenCommandPalette={palette.open}
        />
        <div className="content">
          <AppRouter query={query} />
        </div>
      </main>

      {/* Command Palette */}
      <CommandPalette
        isOpen={palette.isOpen}
        onClose={palette.close}
        query={palette.query}
        onQueryChange={palette.setQuery}
        filteredCommands={palette.filtered}
        allCommands={commands}
        focusedIndex={palette.focusedIndex}
        setFocusedIndex={palette.setFocusedIndex}
        onExecute={palette.execute}
        recentIds={palette.recentIds}
        onKeyDown={palette.handleKeyDown}
        searchRef={palette.searchRef}
      />

      {/* Toast */}
      <Toast message={toast} />
    </div>
  );
}
