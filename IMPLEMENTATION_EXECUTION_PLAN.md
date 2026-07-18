# IMPLEMENTATION_EXECUTION_PLAN.md — MuleShield AI Redesign Blueprint

This document translates the **MuleShield AI — Implementation Master Plan** into a concrete, file-by-file engineering specification. It details exactly what changes, what remains untouched, the new UI/UX components to build, and the chronological execution plan to convert MuleShield from a collection of fraud widgets into a cohesive, high-credibility **AML Investigation Command Center**.

---

## 1. Executive Summary & Architectural Decisions

### Scope Matrix

| Metric / Dimension | Redesign Decision / Plan |
| :--- | :--- |
| **Backend Impact** | **0% Changes to Core Logic**. Core ML XGBoost, SHAP Explainer, Database Schema (PostgreSQL), Graph Degree Centrality (Neo4j), Score Fusion (40% profile, 40% transaction, 20% network), and goAML XML generator remain completely untouched. |
| **APIs Reused** | All existing REST endpoints: `POST /analyze`, `POST /predict/single`, `POST /ingest-i4c` (used as simulation trigger), and `GET /health` remain identical. |
| **Frontend Strategy** | **Maximize Streamlit + Inject Custom CSS**. Re-skin Streamlit using targeted HTML/CSS injection to bypass default aesthetics. Keep the layout simple, fast, and structured. |
| **Streamlit Pages Removed** | **5 Navigation Destinations Disappear**: "Model Analytics", "Dataset Intelligence", "System Health", "Alerts", and "Accounts" tabs are removed from the primary left-rail navigation. |
| **New Pages/Destinations** | **3 Navigation Items Lock**: **Overview** (Glanceable cases & KPIs), **Investigate** (Unified Case Workspace), and **Reports** (Compliance Package Hub). |
| **CSS Replacement** | Complete replacement of default colors and font styling. Injected stylesheet enforces `#0A0B0D` (background), `#141519` (cards), `#1B1D22` (interactive focus), Inter/Geist fonts, 16px border-radius, and the `#5B5FEF` accent. |

---

## 2. Codebase Impact & File-by-File Analysis

The table below catalogs every file in the repository and its designated action in this redesign phase:

| Current File | Component / Area | Action | Redesign Reason & Action | Est. Work |
| :--- | :--- | :--- | :--- | :--- |
| [frontend/app.py](file:///d:/Projects/Muleshield/frontend/app.py) | Router & Entry Point | **Modify** | Collapse left rail to 3 destinations; inject the new design system CSS; remove the moving government cyber threat ticker; wire clean state routing. | 3 hours |
| [frontend/components/sidebar.py](file:///d:/Projects/Muleshield/frontend/components/sidebar.py) | Navigation Panel | **Modify** | Remove 6/9 options. Keep only Overview, Investigate, and Reports. Clean up side controls and remove cluttered status checkers. | 1.5 hours |
| [frontend/components/executive_dashboard.py](file:///d:/Projects/Muleshield/frontend/components/executive_dashboard.py) | Overview Page | **Modify** | Rework layout into a clean Bento Grid layout (3 KPIs + 1 queue card + 1 core preview card). Strip high-contrast colored cards. | 2 hours |
| [frontend/components/alert_center.py](file:///d:/Projects/Muleshield/frontend/components/alert_center.py) | Queue View | **Delete / Merge** | Merge functionality (alert queue and filtering) into the left column of the new Investigate page. Delete the separate component. | 1.5 hours |
| [frontend/components/account_inspector.py](file:///d:/Projects/Muleshield/frontend/components/account_inspector.py) | Core Analysis Panel | **Replace** | Replaced by `investigation_workspace.py`. Layout shifts from complex multi-expander widgets to a clean, cohesive 3-column workspace. | 4 hours |
| [frontend/components/compliance_panel.py](file:///d:/Projects/Muleshield/frontend/components/compliance_panel.py) | Reports Page | **Modify** | Redesign layout to present the goAML XML report in a physical "document preview" style letterhead card. Render SHA-256 seal. | 2.5 hours |
| [frontend/components/graph_view.py](file:///d:/Projects/Muleshield/frontend/components/graph_view.py) | Network Inspector | **Modify** | Embed inside a collapsed drawer or tab. Add a clean, static, pre-rendered backup layout if Neo4j is offline or slow. | 2 hours |
| [frontend/components/lifecycle_view.py](file:///d:/Projects/Muleshield/frontend/components/lifecycle_view.py) | Lifecycle State | **Modify** | Convert from descriptive texts into a horizontal 5-stage track component with the current stage highlighted in accent/risk color. | 1.5 hours |
| [frontend/components/hero.py](file:///d:/Projects/Muleshield/frontend/components/hero.py) | Welcome Screen | **Replace** | Simplify Streamlit welcome to a 1-click "Run Guided Investigation" option. (A static premium React/Tailwind landing page will be built in parallel). | 2 hours |
| [frontend/components/kpi_cards.py](file:///d:/Projects/Muleshield/frontend/components/kpi_cards.py) | Metric Displays | **Modify** | Redesign utilizing tabular numbers, dark slate backgrounds, and simple 1-color indicators. | 1 hour |
| [frontend/components/charts.py](file:///d:/Projects/Muleshield/frontend/components/charts.py) | Graphics/Bars | **Modify** | Restrain color schemes to monochrome or single-accent colors (no rainbow bars or duplicate KPI rings). | 1 hour |
| [frontend/utils/constants.py](file:///d:/Projects/Muleshield/frontend/utils/constants.py) | Shared Values | **Modify** | Remove emojis from labels (e.g. "🛡️ MuleShield" -> "MuleShield"). Ensure severe thresholds reflect 40/40/20 fusion logic. | 0.5 hours |
| [frontend/utils/demo_registry.py](file:///d:/Projects/Muleshield/frontend/utils/demo_registry.py) | Offline Fixtures | **Keep** | Retain static fallbacks for offline demo resilience. | None |
| [backend/*](file:///d:/Projects/Muleshield/backend) | Entire Backend | **Keep** | **Do Not Modify**. Keep all Python code in `backend/` completely untouched (XGBoost model, graph algorithms, DB operations). | None |

---

## 3. Feature-by-Feature Design Specifications

For every recommended feature from the implementation master plan, we outline the engineering specifics below:

### 1. CSS Stylesheet & Typography Overhaul
*   **Current Implementation:** Inline Streamlit styled components, mixed colors (`#1e293b`, default red/green badges).
*   **Problems:** Default Streamlit chrome, borders, rounded radii, and margins conflict with a premium, linear B2B aesthetic.
*   **Files Involved:** `frontend/app.py`
*   **Components Involved:** Shell, Layout, Global styling tags.
*   **Impact:** Frontend-only.
*   **Est. Effort:** 2.5 hours.
*   **Dependencies:** None.
*   **Risk Level:** Low.
*   **Priority:** P0.
*   **Acceptance Criteria:**
    *   No standard Streamlit orange headers or sidebar widgets visible.
    *   Background is fixed to `#0A0B0D`. Cards use `#141519`.
    *   All body and label typography defaults to Inter/Geist. Large metrics use tabular numbers.
*   **Testing Checklist:**
    *   [ ] Open app in chrome devtools, verify no font-family fallback to Arial.
    *   [ ] Verify card borders use a uniform `#1B1D22` outline.

### 2. Collapsed Three-Tab Left Navigation
*   **Current Implementation:** `frontend/components/sidebar.py` uses a list of 9 radio destinations.
*   **Problems:** Cluttered and scattered interface. Judges lose focus navigating between model analytics, system health, and datasets.
*   **Files Involved:** `frontend/components/sidebar.py`, `frontend/app.py`
*   **Components Involved:** Sidebar navigation pane.
*   **Impact:** Frontend navigation logic.
*   **Est. Effort:** 1.5 hours.
*   **Dependencies:** CSS Stylesheet.
*   **Risk Level:** Low.
*   **Priority:** P0.
*   **Acceptance Criteria:**
    *   Exactly 3 tabs exist: Overview, Investigate, Reports.
    *   The live threat ticker and health-checking buttons are removed from the sidebar.
*   **Testing Checklist:**
    *   [ ] Click each of the 3 tabs and ensure pages render instantly.
    *   [ ] Confirm no remaining sidebar links reference deleted tabs.

### 3. Unified Investigate Workspace
*   **Current Implementation:** Separated into Alert Center (queue) and Account Inspector (details) requiring page jumps.
*   **Problems:** Users lose context. Investigating an account requires copy-pasting IDs between sidebar text inputs and views.
*   **Files Involved:** `frontend/app.py`, `frontend/components/account_inspector.py`, `frontend/components/alert_center.py`
*   **Components Involved:** Left column (cases queue), Middle column (Risk card + lifecycle), Right column (SHAP explanation).
*   **Impact:** High. Re-arranges the core interactive layer of the app.
*   **Est. Effort:** 4.5 hours.
*   **Dependencies:** CSS/Radii tokens.
*   **Risk Level:** Medium.
*   **Priority:** P0.
*   **Acceptance Criteria:**
    *   Single-screen workspace layout with 3 vertical zones.
    *   Selecting an account in the left queue populates details in the center and right columns without a full reload.
*   **Testing Checklist:**
    *   [ ] Select "Dormant Reactivation Ring" scenario; verify all 3 columns update dynamically.
    *   [ ] Inspect spacing between columns (must align to a strict 16px grid).

### 4. Fused Risk Decision Card
*   **Current Implementation:** Multiple raw score metrics, inconsistent 70/30 vs 40/40/20 fusion formula labels.
*   **Problems:** Confuses viewers. Dilutes the central value of composite risk scoring.
*   **Files Involved:** `frontend/components/account_inspector.py` (or new workspace file)
*   **Components Involved:** Decision widget card.
*   **Impact:** Medium.
*   **Est. Effort:** 2 hours.
*   **Dependencies:** Unified Investigate Workspace.
*   **Risk Level:** Low.
*   **Priority:** P0.
*   **Acceptance Criteria:**
    *   One large, prominent composite risk score indicator (e.g. `86/100`).
    *   Exactly three small horizontal bar charts showing contributors: Profile (40%), Transaction (40%), and Network (20%).
*   **Testing Checklist:**
    *   [ ] Confirm calculated contribution ratios strictly match the backend API response.
    *   [ ] Validate background color uses a soft glass border treatment with high contrast.

### 5. Plain-English SHAP Case Brief
*   **Current Implementation:** Renders raw machine learning features (e.g. `F670`, `F886`) directly to the user.
*   **Problems:** Incomprehensible to compliance investigators. Looks like a raw debugging view.
*   **Files Involved:** `frontend/components/account_inspector.py`
*   **Components Involved:** SHAP explanation drawer/card.
*   **Impact:** Medium.
*   **Est. Effort:** 2 hours.
*   **Dependencies:** None.
*   **Risk Level:** Low.
*   **Priority:** P1.
*   **Acceptance Criteria:**
    *   Raw features translated into 3 clean, human-readable bullet points (e.g. "Dormant account reactivated", "High transfer speed").
    *   Raw debugging codes hidden behind a small progressive disclosure "Technical factor details" expander.
*   **Testing Checklist:**
    *   [ ] Load fallback dataset. Verify no raw column names are visible in the default view.
    *   [ ] Expand "Technical factor details" and verify correct SHAP values render inside.

### 6. Sealed Reports & goAML Preview
*   **Current Implementation:** Raw text area dumping XML outputs in a gray code editor block.
*   **Problems:** Looks unfinished. Does not present goAML as a premium compliance handoff package.
*   **Files Involved:** `frontend/components/compliance_panel.py`
*   **Components Involved:** Compliance report renderer.
*   **Impact:** Medium.
*   **Est. Effort:** 2.5 hours.
*   **Dependencies:** Reports navigation tab.
*   **Risk Level:** Low.
*   **Priority:** P0.
*   **Acceptance Criteria:**
    *   goAML XML report previewed inside a physical "paper-like" card component with formal borders.
    *   The SHA-256 evidence integrity hash clearly displayed underneath the document.
*   **Testing Checklist:**
    *   [ ] Click "Download goAML XML Report" button; verify correct XML schema outputs.
    *   [ ] Validate SHA-256 matches values logged in backend databases.

### 7. Static Premium React/Tailwind Landing Page
*   **Current Implementation:** Basic Streamlit markdown splash.
*   **Problems:** Streamlit's loading delay and lack of custom interactive layouts yield a poor first impression.
*   **Files Involved:** Created as a standalone index page.
*   **Components Involved:** Landing Hero Section, problem statistics panel, trust footer.
*   **Impact:** High first impression lift.
*   **Est. Effort:** 6 hours.
*   **Dependencies:** Design System.
*   **Risk Level:** Medium.
*   **Priority:** P1.
*   **Acceptance Criteria:**
    *   Interactive static page that introduces the product concept and features a single "Run Guided Investigation" call-to-action button that routes directly to the working Streamlit workspace.
*   **Testing Checklist:**
    *   [ ] Load landing page; check mobile layout responsiveness.
    *   [ ] Confirm clicking the CTA redirects to the Streamlit app seamlessly.

---

## 4. UI Layout Specs per Screen

### Overview Page
*   **Current UI:** Grid of charts, multiple navigation items, and performance health bars.
*   **New Layout:** Bento grid layout containing:
    *   **KPI Row:** 3 cards displaying Total Flags, Actioned Cases, and Average Resolution Time.
    *   **Case Queue Grid:** A compact table displaying active critical cases.
    *   **Active Preview Card:** Details of the selected high-risk account.
*   **Aesthetics:** Tabular fonts, `#141519` card container surfaces, minimal gray borders, and one pulse color dot on critical items.

### Investigate Workspace
*   **Current UI:** Separated tabs for search and results.
*   **New Layout:** Three-column layout:
    1.  **Left Column (30%):** Alert and scenario list.
    2.  **Center Column (45%):** Decision ledger with score gauge, lifecycle track, and action suggestions.
    3.  **Right Column (25%):** Case brief with 3 plain-text reasons, technical explainers, and link network fallback.
*   **Interactions:** Hover effects on case lists, skeleton shimmer loaders during analysis.

### Reports Workspace
*   **Current UI:** Raw JSON and XML downloads.
*   **New Layout:** 
    *   Left-aligned letterhead card displaying document name, generated date, and metadata.
    *   Right-aligned download options, SHA-256 seal container, and transaction ledger.
*   **Typography:** Strict sans-serif font rendering to mirror official AML submissions.

---

## 5. Streamlit Optimization & CSS Injection Strategy

Because the backend remains untouched, our Streamlit rendering must be highly optimized:
1.  **Centralized Stylesheet:** Write a `style.css` file containing all layout resets and class modifiers. Inject this file at the start of `app.py`:
    ```python
    with open("frontend/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    ```
2.  **Custom Component Minimization:** Use default widgets (`st.dataframe`, `st.button`, `st.radio`) but format them using injected class overrides.
3.  **Preventing Double Render:** Force-cache data inputs to avoid multiple database calls when switching workspaces.

---

## 6. Implementation Milestones

### Milestone 0: Preparation (Hours 0 - 3)
*   **Tasks:** Sweep all text files and UI code to remove overclaims (e.g. change "auto-freeze" to "recommended hold"). Audit validation metrics. Set up `style.css`.
*   **Expected Output:** Credibility statements locked, design token definitions ready in code.

### Milestone 1: Navigation Refactor (Hours 3 - 6)
*   **Tasks:** Collapse sidebar navigation in `sidebar.py`. Redefine active routes in `app.py` for Overview, Investigate, and Reports. Remove system health buttons.
*   **Expected Output:** Sidebar rendered with exactly 3 items; router cleanly switches pages.

### Milestone 2: Investigate Layout (Hours 6 - 12)
*   **Tasks:** Build the 3-column investigate workspace in `account_inspector.py`. Load selected accounts via columns. Setup fallback data bindings.
*   **Expected Output:** Interactive investigation table updating cases dynamically.

### Milestone 3: Risk Fusion (Hours 12 - 16)
*   **Tasks:** Implement the 3-bar contribution widget under the composite score. Connect metrics directly to FastAPI response payloads.
*   **Expected Output:** Unified risk card displaying a score gauge and Profile/Transaction/Network bars.

### Milestone 4: Case Briefs (Hours 16 - 20)
*   **Tasks:** Translate SHAP features to human-readable bullets. Add the expander for raw feature matrices.
*   **Expected Output:** SHAP explainer cards showing plain-text reasons.

### Milestone 5: Reports Page (Hours 20 - 24)
*   **Tasks:** Redesign `compliance_panel.py`. Construct the document letterhead display. Render the SHA-256 seal block.
*   **Expected Output:** Premium XML export screen.

### Milestone 6: Landing Page (Hours 24 - 36)
*   **Tasks:** Create a standalone React/Tailwind landing hero. Connect CTA button to Streamlit workspace.
*   **Expected Output:** High-conversion static asset ready to present.

### Milestone 7: Polish & Validation (Hours 36 - 48)
*   **Tasks:** Verify offline resiliency (run workspace without database/Neo4j). Refine styling margins. Conduct full run-through rehearsals.
*   **Expected Output:** Redesigned, functional, offline-capable application.
