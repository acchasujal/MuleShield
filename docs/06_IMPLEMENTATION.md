# 06_IMPLEMENTATION.md — MuleShield AI: Implementation Specification

This document details the modular code structure, state context architecture, and React codebases deployed to implement the money-mule intelligence prototype.

---

## 1. Application Context State Structure

All global states reside in [`AppContext.tsx`](file:///d:/Projects/Muleshield/frontend-react/src/contexts/AppContext.tsx):
- `cases`: Array of active alert items.
- `selectedId`: Target account index currently under lookup.
- `analystDecisions`: Record mapping case accounts to investigator outcomes (`PENDING`, `APPROVED`, `ESCALATED`).
- `packageReady`: Tracks whether evidence packages are sealed.
- `unfoldProgress`: Controls simulation animation timelines per case.
- `offlineMode`: Simulates fallback data states when decoupled from the FastAPI backend.

---

## 2. Component Layout & Sizing

Every UI element is split into specialized sub-components under 200 lines to ensure codebase hygiene and maintainability:
- `components/layout/`: Sidebar and Topbar navigations.
- `components/ui/`: Standard StatCards, Highlights, and Toast banners.
- `components/cases/`: Case rows and queues.
- `components/investigation/`: Timeline trackers, DecisionSurfaces, CaseBriefs, and interactive SVG diagrams.
- `components/command-palette/`: Raycast-style search modals.

---

## 3. Custom React Hooks

- **`useCountUp`**: Evaluates smooth Quad-Ease countups to sync gauges and numeric score text.
- **`useCommandPalette`**: Attaches focus bounds, key hooks, and history lookups for modal panels.
- **`useUpload`**: Handles CSV multi-part file payloads and fallback routes.
