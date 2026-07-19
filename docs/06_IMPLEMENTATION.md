# MuleShield AI — Implementation Specification

This document details the modular code structure, React state management context architecture, and implementation details of the React web application.

---

## 1. Application Context State Structure

All global states reside in [`AppContext.tsx`](file:///d:/Projects/Muleshield/frontend-react/src/contexts/AppContext.tsx):
- `cases`: Array of active alert items.
- `selectedId`: Target account index currently under lookup.
- `analystDecisions`: Record mapping case accounts to investigator outcomes (`PENDING`, `APPROVED`, `ESCALATED`).
- `packageReady`: Tracks whether evidence packages are sealed.
- `unfoldProgress`: Controls simulation animation timelines per case.
- `offlineMode`: Simulates fallback data states when decoupled from FastAPI.

---

## 2. Component Layout & Sizing

Every UI element is split into specialized sub-components under 200 lines to ensure code quality:
- `components/layout/`: Sidebar and Topbar navigations.
- `components/ui/`: Standard StatCards, Highlights, and Toast banners.
- `components/cases/`: Case rows and tables.
- `components/investigation/`: Timeline trackers, DecisionSurfaces, and interactive SVG diagrams.
- `components/command-palette/`: Raycast-style modals.

---

## 3. Custom React Hooks

- **`useCountUp`**: Evaluates smooth Quad-Ease countups to sync gauges and numeric score text.
- **`useCommandPalette`**: Attaches focus bounds, key hooks, and history lookups for modal panels.
- **`useUpload`**: Handles CSV multi-part file payloads and fallback routes.
