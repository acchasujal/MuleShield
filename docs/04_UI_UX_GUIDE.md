# MuleShield AI — UI/UX Guide

This document maps out the user experience flow, visual hierarchy, responsive screen sizes, and layout configurations.

---

## 1. Information Architecture & Navigation

The layout follows a persistent **2-Column Layout Engine**:
- **Sidebar (Left Rail)**: Handles workspace navigation (Cases, Investigate, Evidence, Methodology) and provides presentation reset actions.
- **Main Viewport (Right Area)**: Houses the active workspace screen. Includes a top-level breadcrumb tracker and global search tool.

---

## 2. Page Hierarchy & Flows

### 1. Priority Cases Queue (`/cases`)
- **Visual Goal**: Analyst inbox model.
- **Grid Layout**: Top statistical counters (StatCards) summarizing threat severity clusters, followed by the cases queue.
- **Actions**: Triggers batch CSV ingestion, or initiates the main guided scenario walkthrough.

### 2. Guided Investigation Room (`/investigate`)
- **Segment Control**: Swaps active target accounts instantly.
- **Bento Workspace**: 3-zone bento panel displaying:
  1. **Sidebar Queue**: Active cases matching search filters.
  2. **Decision Center**: Core animated composited score, contribution breakdown bars, and lifecycle timeline.
  3. **Brief Inspector**: Mapped explainability attributions, active network links, and provenance drawer controls.

### 3. Sealed Handoff Center (`/evidence`)
- **Sealing Status**: Converts drafts into cryptographically sealed STR profiles.
- **Report Template**: Rendered like formal paper document briefs (letterhead feel, plain serif fonts).
- **Exports**: Trigger downloads of goAML XML files and case JSON logs.
