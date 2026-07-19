# 04_UI_UX_GUIDE.md — MuleShield AI: UI/UX Guide

This document maps out the user experience flow, visual hierarchy, responsive layouts, and screen configurations for the financial trust infrastructure workspace.

---

## 1. Information Architecture & Navigation

The layout follows a persistent **2-Column Layout Engine**:
- **Sidebar (Left Rail)**: Handles workspace navigation (Cases queue, active Investigation Workspace, Sealed Evidence Packages, and Technical Methodology) and provides presentation reset actions.
- **Main Viewport (Right Area)**: Houses the active page layout. Includes a top-level breadcrumb tracker, global search, and command palette trigger button.

---

## 2. Page Hierarchy & Flows

### 1. Priority Cases Queue (`/cases`)
- **Visual Goal**: Analyst inbox model designed for institutional compliance environments.
- **Grid Layout**: Top statistical counters (StatCards) summarizing threat severity clusters, followed by the cases queue inbox.
- **Actions**: Triggers batch CSV ingestion, or initiates the main money-mule intelligence scenario walkthrough.

### 2. Investigation Workspace (`/investigate`)
- **Segmented Control**: Swaps active target accounts instantly using a unified control track.
- **Bento Layout**: 3-zone bento panel displaying:
  1. **Sidebar Queue**: Active cases matching search filters.
  2. **Decision Surface**: Core animated composite score, contribution breakdown bars, and lifecycle timeline.
  3. **Case Brief**: Mapped explainability attributions, active network links, and provenance drawer controls.

### 3. Sealed Handoff Center (`/evidence`)
- **Sealing Status**: Converts draft packages into cryptographically sealed STR profiles.
- **Report Template**: Rendered like formal paper document briefs (letterhead feel, plain serif fonts) for legal auditability.
- **Exports**: Trigger downloads of goAML XML files and case JSON logs.
