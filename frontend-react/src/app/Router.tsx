// ============================================================
// MuleShield — App Router
// Proper <Routes> based routing with 404 redirect.
// ============================================================

import { Navigate, Route, Routes } from "react-router-dom";
import { CasesPage } from "../pages/CasesPage";
import { InvestigatePage } from "../pages/InvestigatePage";
import { EvidencePage } from "../pages/EvidencePage";
import { MethodologyPage } from "../pages/MethodologyPage";

interface AppRouterProps {
  query: string;
}

export function AppRouter({ query }: AppRouterProps) {
  return (
    <Routes>
      <Route path="/" element={<Navigate to="/cases" replace />} />
      <Route path="/cases" element={<CasesPage query={query} />} />
      <Route path="/investigate" element={<InvestigatePage query={query} />} />
      <Route path="/evidence" element={<EvidencePage />} />
      <Route path="/methodology" element={<MethodologyPage />} />
      {/* Catch-all: redirect unknown paths to cases */}
      <Route path="*" element={<Navigate to="/cases" replace />} />
    </Routes>
  );
}
