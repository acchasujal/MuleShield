// ============================================================
// MuleShield — App Context
//
// Holds all shared application state and business actions.
// Navigation is intentionally NOT here — pages own their routing.
// ============================================================

import React, {
  createContext,
  useCallback,
  useContext,
  useState,
  type ReactNode,
} from "react";

import { FALLBACK_CASES } from "../data/fallbackCases";
import type { AnalystDecision, CaseItem } from "../types";

// ---------------------------------------------------------------------------
// Context shape
// ---------------------------------------------------------------------------
interface AppContextValue {
  // Data
  cases: CaseItem[];
  setCases: (cases: CaseItem[]) => void;

  // Selection
  selectedId: string;
  setSelectedId: (id: string) => void;

  // Analyst decisions per case
  analystDecisions: Record<string, AnalystDecision>;
  setAnalystDecision: (caseId: string, decision: AnalystDecision) => void;

  // Evidence package state per case
  packageReady: Record<string, boolean>;
  setPackageReady: (caseId: string, ready: boolean) => void;

  // Investigation unfold progress per case
  unfoldProgress: Record<string, number>;
  setUnfoldProgress: (caseId: string, progress: number) => void;

  // Demo / connection mode
  offlineMode: boolean;
  setOfflineMode: (v: boolean) => void;

  // Derived
  selectedCase: CaseItem;

  // Actions
  notify: (message: string) => void;
  toast: string;
  resetDemo: () => void;
}

const AppContext = createContext<AppContextValue | null>(null);

// ---------------------------------------------------------------------------
// Provider
// ---------------------------------------------------------------------------
export function AppProvider({ children }: { children: ReactNode }) {
  const [cases, setCases] = useState<CaseItem[]>(FALLBACK_CASES);
  const [selectedId, setSelectedId] = useState(FALLBACK_CASES[0].account);
  const [analystDecisions, setAnalystDecisionsMap] = useState<
    Record<string, AnalystDecision>
  >({});
  const [packageReady, setPackageReadyMap] = useState<Record<string, boolean>>(
    {}
  );
  const [unfoldProgress, setUnfoldProgressMap] = useState<
    Record<string, number>
  >({});
  const [offlineMode, setOfflineMode] = useState(true);
  const [toast, setToast] = useState("");

  const selectedCase =
    cases.find((c) => c.account === selectedId) ?? cases[0];

  const notify = useCallback((message: string) => {
    setToast(message);
    window.setTimeout(() => setToast(""), 2600);
  }, []);

  const setAnalystDecision = useCallback(
    (caseId: string, decision: AnalystDecision) => {
      setAnalystDecisionsMap((prev) => ({ ...prev, [caseId]: decision }));
    },
    []
  );

  const setPackageReady = useCallback((caseId: string, ready: boolean) => {
    setPackageReadyMap((prev) => ({ ...prev, [caseId]: ready }));
  }, []);

  const setUnfoldProgress = useCallback(
    (caseId: string, progress: number) => {
      setUnfoldProgressMap((prev) => ({ ...prev, [caseId]: progress }));
    },
    []
  );

  const resetDemo = useCallback(() => {
    setCases(FALLBACK_CASES);
    setSelectedId(FALLBACK_CASES[0].account);
    setPackageReadyMap({});
    setUnfoldProgressMap({});
    setAnalystDecisionsMap({});
    notify("Demo state successfully reset.");
  }, [notify]);

  return (
    <AppContext.Provider
      value={{
        cases,
        setCases,
        selectedId,
        setSelectedId,
        analystDecisions,
        setAnalystDecision,
        packageReady,
        setPackageReady,
        unfoldProgress,
        setUnfoldProgress,
        offlineMode,
        setOfflineMode,
        selectedCase,
        notify,
        toast,
        resetDemo,
      }}
    >
      {children}
    </AppContext.Provider>
  );
}

// ---------------------------------------------------------------------------
// Consumer hook
// ---------------------------------------------------------------------------
export function useAppContext(): AppContextValue {
  const ctx = useContext(AppContext);
  if (!ctx) {
    throw new Error("useAppContext must be used within <AppProvider>");
  }
  return ctx;
}
