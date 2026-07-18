# AI_CONTEXT.md — For Future Claude/Cursor Coding Sessions

> Read this file first before writing any code. It is the operational briefing; `PROJECT_CONTEXT.md` is the vision doc, `BUILD_GUIDE.md` is the architecture/roadmap doc, `DESIGN_SYSTEM.md` is the visual spec, `PECHACKS_STRATEGY.md` is the hackathon-fit doc. This file exists so you don't have to re-derive state from scratch.

---

## 1. Current Project State

`[FACT]` MuleShield AI's backend (FastAPI + XGBoost/SHAP + Neo4j + PostgreSQL + goAML XML generation) is **fully built and functional**. The active work is a **frontend/UI redesign only**, targeting submission to PEC Hacks 4.0 (Aug 29-30, 2026) with ~2 days of implementation time remaining as of this doc's writing.

## 2. Completed Features `[FACT]`

- Composite risk fusion engine (`backend/ml/score_fusion.py`) — 0.40/0.40/0.20 weighting across ML/Transaction/Graph scores.
- XGBoost classifier + SHAP explainability (`backend/ml/predictor.py`, `shap_engine.py`).
- Neo4j graph degree-centrality scoring with graceful offline degradation (`backend/graph_service.py`).
- PostgreSQL audit logging with SHA-256 evidence hashing (`backend/database.py`).
- goAML-compliant XML report generation (`backend/xml_generator.py`).
- Mule lifecycle staging engine (DORMANT → ACTIVATION → NEWLY_RECRUITED → ACTIVE_MULE → BEING_FLUSHED) (`backend/ml/lifecycle_engine.py`).
- I4C government webhook ingestion simulation (`routers/i4c_webhook.py`).
- Existing Streamlit frontend (functional but needs the redesign described in `DESIGN_SYSTEM.md` / `BUILD_GUIDE.md`).

## 3. Pending Features (this sprint) `[RECOMMENDATION — not yet built]`

Ranked list lives in `BUILD_GUIDE.md` §4. Priority order for implementation:
1. CSS/typography/theme overhaul of existing Streamlit app
2. Dashboard restructure into 3-zone bento layout (merge Account Inspector + Alert Center)
3. SHAP → plain-English card redesign
4. Composite score reveal animation
5. Static React/Tailwind landing page (separate build, see §5 below)
6. goAML reveal + hash animation
7. Graph viz restyle + cached/static fallback
8. Micro-interactions, loading/empty states

## 4. Important Design Decisions `[DECISION — locked]`

- **No backend logic changes.** The fusion formula, ML pipeline, and API contracts are frozen for this sprint — see `[CONSTRAINT]` in `BUILD_GUIDE.md` §2.
- **Dark-mode-first, Minimal Enterprise + Soft Glass** visual language — full token spec in `DESIGN_SYSTEM.md`. Do not introduce colors/fonts/radii outside that spec.
- **Neo4j is NOT part of the default live demo path.** Default demo must work fully offline (cached data + ML score only). Live graph DB is a secondary "explore" tab only, per `BUILD_GUIDE.md` §3.
- **No new ML models.** All "AI investigation" output is a re-presentation of existing SHAP/fusion/lifecycle data as plain-English text — not new inference. Do not add new model training code this sprint.

## 5. Architecture Decisions

- Frontend split: existing Streamlit app gets a heavy CSS-injected re-skin (working product, connects to live backend); a **separate static React/Tailwind landing page** is built independently and used only as the demo's first-impression asset, not wired to the live backend. Do not attempt to merge these into one codebase under the 2-day constraint — keep them as two separate deliverables shown sequentially in the demo.
- Component hierarchy target: see `DESIGN_SYSTEM.md` §20.

## 6. Files That Matter

`[FACT]`
- `backend/ml/score_fusion.py` — the core scoring logic, treat as read-only this sprint.
- `backend/ml/lifecycle_engine.py` — stage transition rules, source for the "AI Investigation Timeline" UI feature.
- `OPERATIONS.md` §3.3 — the F670/F886/etc. → plain-English signal dictionary; wire this through every UI surface, not just the SHAP panel.
- `frontend/app.py` — primary file being redesigned this sprint.
- `frontend/components/graph_view.py` — graph viz restyle target (colors/labels only, no logic changes).

## 7. Things to Never Change (this sprint)

- The 0.40/0.40/0.20 fusion weighting.
- The severity threshold tiers (CRITICAL≥80, HIGH 60-79, MEDIUM 40-59, LOW<40).
- The 122-feature validated index (`final_metadata.json`) — never add/omit columns dynamically, per `OPERATIONS.md` §2.2.
- Product branding: always "MuleShield AI", target institution "Bank of India"/"BOI" — never "FundTrace" or "Union Bank" (legacy names, already purged once, do not reintroduce).

## 8. Known Bugs / Unresolved Issues `[FLAG — not a UI task, but must be resolved before pitch]`

- **Validation metric credibility risk**: `VALIDATION_REPORT.md` §4.4 reports ROC-AUC = 1.000000 and PR-AUC = 1.000000 on a validation split containing only 16 positive samples. This is a leakage/overfitting red flag that must be re-audited (beyond the already-excluded F3912 feature) or reframed honestly in pitch material. This is a data-science task, not a frontend task — flag it, don't silently fix it by changing UI copy.
- **Unresolved prior "overclaiming incident"**: referenced by the user in an earlier session but never specified. Do not fabricate what it was or claim it's resolved — surface this as an open question if it comes up.

## 9. Technical Constraints

- 2-day implementation window (as of this doc).
- Native Streamlit cannot achieve true Stripe/Linear visual parity — see §5 split-build decision.
- Hackathon wifi/infra reliability for live Docker + Neo4j + PostgreSQL is unverified — offline fallback is mandatory, not optional.

## 10. Future Improvements `[IDEA — do not build now]`

- RBI regulatory sandbox pilot integration.
- Real-time streaming ingestion (currently batch CSV only).
- Multi-tenant bank deployment.
- Risk heatmap widget, interactive fraud-journey scrubber (cut first if time runs short — see `DESIGN_SYSTEM.md` §23).

## 11. Current Priorities (in order)

1. Resolve/re-audit the validation-metric leakage risk (blocking, not cosmetic).
2. CSS/theme overhaul of existing Streamlit app.
3. Dashboard restructure + SHAP card redesign.
4. Static landing page build.
5. Demo rehearsal with offline fallback path.
6. PPT build from real screenshots.

## 12. Developer Notes

- Every UI change should be checked against `DESIGN_SYSTEM.md` before merging — one consistent design language across landing, dashboard, and PPT is a bigger judge-perception lever than any single feature.
- When in doubt between adding a feature and polishing an existing one, polish — see `BUILD_GUIDE.md` §7 priority matrix.
- Verify PEC Hacks judge panel and track brief details on pechacks.org before finalizing pitch language — the version in `PECHACKS_STRATEGY.md` is marked unverified this session.
