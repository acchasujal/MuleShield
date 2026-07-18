# MuleShield AI — Implementation Master Plan

## Executive decision

**Do not build another fraud dashboard.** Reframe MuleShield as an **AML Investigation Command Center**: a bank investigator uploads or opens a flagged transaction batch, understands the risk in seconds, takes a defensible action, and receives a regulator-ready evidence package.

The product promise is not “AI detects fraud.” It is:

> **MuleShield turns a suspicious-money trail into a reviewable, explainable, and report-ready case before the funds are dispersed.**

This is a much stronger PEC Hacks FinTech submission because it directly answers the official brief—“Reimagine money, banking, and financial access. Build the infrastructure for the next billion users”—with trust infrastructure for the payment layer, rather than another consumer payments app or isolated ML demo. PEC Hacks 4.0 is a 36-hour in-person event; the public site lists FinTech among its domains and the exact “next billion users” brief. [PEC Hacks official site](https://pechacks.org/)

**The strategic move for the remaining two days:** make one exceptional end-to-end investigation feel real, calm, and credible. Reuse the working backend, APIs, XGBoost/SHAP pipeline, Neo4j path, PostgreSQL audit log, XML generator, lifecycle engine, and fallback fixtures. Do not add a model, database, integration, new dashboard, or generic chatbot.

---

## 1. Evidence base and working assumptions

This plan is based on a full review of `docs/DOCS-V2/*.md`, an inspection of the current Streamlit entry point and supplied dashboard screenshot, and independent web research. Statements below are deliberately separated into verified capability, design recommendation, and pitch-safe claim.

### What is verified in the repository

- FastAPI exposes analysis, single-account prediction, and simulated I4C-ingestion paths.
- Risk is fused using **40% profile/ML, 40% transaction, 20% graph**. Severity is CRITICAL ≥80, HIGH 60–79, MEDIUM 40–59, LOW <40.
- XGBoost inference, SHAP attribution, rule/transaction analysis, graph scoring with offline degradation, lifecycle staging, audit hashing, and goAML XML generation already exist.
- The Streamlit product has fallback data, so a demo can succeed without live Neo4j or PostgreSQL.
- The current UI has at least nine top-level destinations: Dashboard, Investigations, Alerts, Accounts, Model Analytics, Compliance, I4C Intelligence, Dataset Intelligence, and System Health.

### Important credibility constraints

- The reported ROC-AUC and PR-AUC of 1.0 are based on a split with only 16 positive validation samples. Treat this as an unresolved audit risk, never as a hero metric.
- Current copy includes claims that must be removed or qualified unless demonstrated live: “live” government ticker, automatic CBS freeze, I4C scale/latency numbers, 72-hour-to-4-second reduction, “admissible” evidence, model-improvement claims, and 99.8%/100% readiness claims.
- There is a current inconsistency: the product documentation locks a 40/40/20 fusion formula while an existing UI roadmap describes 70/30. The UI, pitch, and source of truth must only show 40/40/20.
- Do not imply that a generated XML report is submitted to FIU-IND, that MuleShield freezes accounts, or that an I4C integration is live. It is a **review recommendation / simulated ingestion / report-ready export** unless a live integration can be proven.

### External research implications

- PEC Hacks’ official public brief validates the FinTech choice, the “next billion users” framing, the Aug 29–30 2026 schedule, and its 36-hour offline format. The public site does not publish a judge rubric; do not invent one. [Official event and FinTech domain](https://pechacks.org/)
- Devfolio confirms a student-led, impact-oriented event with mentorship and a 2–5 member team format; it does not supply a scoring rubric. [PEC Hacks on Devfolio](https://pec-hacks.devfolio.co/)
- The relevant 2026 product pattern is **confidence over complexity**: a single decisive default view, progressive disclosure, and AI that explains/prioritizes instead of creating another control surface. [SaaS UI patterns](https://www.saasui.design/blog/7-saas-ui-design-trends-2026)
- In regulated fintech, UX must simplify a decision without hiding evidence, uncertainty, or auditability. That is why MuleShield should use a focused case workspace—not a dense, KPI-heavy analytics wall. [Fintech SaaS UX analysis](https://wsa.design/news/fintech-saas-design-how-to-turn-product-complexity-into-clear-ux)

---

## 2. Critical review of the existing project

### What judges will love

1. **A complete chain, not a classifier.** Most hackathon fraud projects stop at a score. MuleShield can show detection → explanation → lifecycle context → compliance artifact → tamper-evident audit trail.
2. **Practical resilience.** Graceful ML-only operation when graph/database infrastructure is unavailable is excellent engineering judgment for an on-premise banking context and protects the live demo.
3. **Technically legible depth.** XGBoost, SHAP, graph analysis, FastAPI, Neo4j, PostgreSQL, and cryptographic evidence are substantial—but should be revealed after value, not dumped up front.
4. **A real domain wedge.** Money-mule networks are a sharper, less crowded FinTech angle than budgeting, payments, or generic “fraud AI.”
5. **Lifecycle framing.** “Before funds are flushed” is a memorable operational story that makes a risk score actionable.

### What judges may dislike today

1. **It currently looks like several projects stitched together.** Nine navigation items, KPI panels, model analytics, system-health pages, data intelligence, and the I4C simulator compete with the actual investigation task.
2. **The dashboard communicates monitoring, not resolution.** A compliance officer’s first question is “what needs my action and why?” Current top-level metrics do not answer it.
3. **The visual system is close but not coherent.** Existing rounded cards, mixed saturated borders, a dense left rail, Streamlit chrome, a 6px radius, and an animated bottom ticker conflict with the proposed minimal enterprise system.
4. **The ticker actively weakens trust.** It is visually noisy, uses unverifiable “LIVE” language, and advertises jargon/claims the product should not need to defend.
5. **The narrative overclaims.** “Auto-freeze,” “inter-agency SLA,” “government telemetry,” and absolute performance/readiness claims invite technical interrogation and can collapse trust in a two-minute demo.
6. **Data/ML detail appears too early.** Raw feature codes, model analytics, dataset statistics, and infrastructure health are useful backup evidence—not the core product journey.

### Missed opportunity

MuleShield already has the ingredients for a rare hackathon moment: a **case handoff** that says, “Here is the account, here is why it is risky, here is where the money moved, here is the recommended action, and here is the compliance package.” The redesign should build that moment, not add more charts.

---

## 3. Product vision and positioning

### Recommended product category

**MuleShield AI — Financial Trust Infrastructure for AML Operations**

Subhead: **Detect mule networks early. Give investigators a defensible next move.**

Supporting one-liner: *An explainable investigation workspace that fuses behavioral, transactional, and network signals into a report-ready AML case.*

### Language to use

- “Investigation workspace,” “risk recommendation,” “evidence package,” “review-ready,” “report-ready,” “offline-resilient.”
- “Designed for bank AML and fraud-operations teams.”
- “Built to protect the payment rails used by the next billion digital users.”

### Language to avoid

- “Autopilot” as the core promise (suggests unsupervised high-stakes action).
- “Auto-freeze,” “court-admissible,” “FIU submission,” “live I4C feed,” “real-time” unless the exact condition is demonstrated.
- “100%,” “guaranteed,” “prevent,” “eliminate,” and unsupported time/money savings.
- “AI chatbot” or “ML dashboard.” Neither distinguishes the product.

### The mental model

```
Suspicious activity
       ↓
MuleShield creates a case
       ↓
Investigator sees the evidence and recommended action
       ↓
Investigator reviews / escalates
       ↓
MuleShield prepares the audit and reporting evidence
```

This is an operational system, not an analytics destination.

---

## 4. Feature audit: cut complexity without cutting proof

| Existing capability / surface | Decision | How it should appear in the submitted product | Why |
|---|---|---|---|
| CSV batch analysis | **KEEP + REDESIGN** | Primary “Start investigation” action; include one preloaded demo scenario | It proves a working workflow and supports the demo |
| Composite risk fusion | **KEEP + SIMPLIFY** | One focal risk card with three labeled contributors: Profile, Transaction, Network | This is the core differentiator; never duplicate the score in multiple graphs |
| SHAP explanations | **KEEP + REDESIGN** | “Why MuleShield flagged this” with 3 plain-language evidence bullets and “View technical factors” disclosure | Makes AI defensible rather than decorative |
| Lifecycle staging | **KEEP + MERGE** | A small “Mule lifecycle” state in the case card, paired with recommended urgency | Strong story, but should not become a separate taxonomy lesson |
| Neo4j / graph visual | **KEEP + DEMOTE** | Collapsed “Network evidence” panel with cached static fallback | Useful corroboration; risky as the first demo interaction |
| goAML XML | **KEEP + ELEVATE** | The final case-handoff card: “Report-ready package” with preview, download, and hash | The least common / most pitchable differentiator |
| SHA-256 audit evidence | **KEEP + ELEVATE** | One compact “Evidence integrity” row in the report card | Builds enterprise trust without a cryptography lecture |
| PostgreSQL audit log | **KEEP + HIDE** | Proof point in “Case activity” / technical appendix | It is implementation proof, not a primary screen |
| I4C webhook simulator | **SIMPLIFY + POSTPONE** | Keep only as an optional “simulated threat-intel event” demo trigger; no live ticker | A demo enhancer, not a credible public live-feed claim |
| Alert Center + Account Inspector | **MERGE** | One Investigate workspace: queue at left, selected case at center, explanation at right | Removes page transitions and preserves context |
| Executive dashboard / KPI strip | **SIMPLIFY** | Overview shows only 3–4 action-linked facts; do not lead the demo here | Avoid fake operational analytics and decorative cards |
| Model Analytics | **POSTPONE / HIDE** | One “Methodology” drawer or appendix screenshot | Technical judges can ask; everyone else should not have to navigate it |
| Dataset Intelligence | **REMOVE FROM NAV** | Technical appendix only | Raw features and synthetic demographic claims harm focus and can invite data-ethics questions |
| System Health | **REMOVE FROM NAV** | Hidden support route / preflight checklist only | Infrastructure status is not product value |
| Animated government ticker | **REMOVE** | Nothing replaces it | It undermines calm, credibility, and accessible reading |
| Generic AI chat | **POSTPONE** | Do not show in default path | It adds risk of hallucination and does not improve the core decision |
| Risk heatmap / timeline scrubber | **POSTPONE** | Build only after all P0 items, if at all | Nice visuals cannot compensate for a weak first workflow |

---

## 5. Target UX: one case, one decision, one handoff

### The default journey (three clicks after opening)

1. **Landing / start** — Judge sees the product promise and chooses **Run guided investigation**.
2. **Investigate** — A prepared “Dormant account reactivated” scenario is ready; click **Analyze case**. CSV upload is adjacent but secondary.
3. **Decision** — Fusion reveal completes, a selected high-risk case opens, and the investigator sees evidence plus the appropriate recommended action.
4. **Handoff** — Click **Prepare report package**. Show goAML preview, evidence hash, and a clear “Ready for investigator review/export” status.

This keeps the demo under 100 seconds without pretending that a financial institution should automatically freeze someone’s account.

### Information architecture

Use only three left-rail destinations:

| Navigation | Job to be done | Default content |
|---|---|---|
| Overview | “What needs attention?” | Three action-linked metrics, active case queue, one selected critical case |
| Investigate | “Why is this account risky and what should I do?” | Unified case workspace |
| Reports | “What evidence can I hand off?” | Generated report packages and evidence integrity |

“Overview” must link directly into the selected case. It is not an executive analytics museum.

### Investigate workspace layout

```
┌──────────────────────────────────────────────────────────────────────┐
│ Case: ACC…0028   CRITICAL • ACTIVE MULE        [Prepare report]       │
├───────────────┬───────────────────────────────────┬──────────────────┤
│ Case queue    │ Risk decision                      │ Why flagged      │
│               │  86 / 100  Critical                │ • Dormant acct   │
│ 4 cases       │  Profile  • Transaction • Network  │   reactivated    │
│ selected case │  Recommended: Hold & review        │ • High velocity  │
│ others muted  │  Lifecycle: Being flushed          │ • Linked accounts│
│               │  [View network evidence]           │ [Technical detail]│
└───────────────┴───────────────────────────────────┴──────────────────┘
```

### Decision language

Show a recommendation, owner, and reason—not an unsupported action:

- **CRITICAL:** “Immediate review recommended — escalate under bank policy.”
- **HIGH:** “Priority review recommended — prepare STR evidence.”
- **MEDIUM:** “Monitor and enrich — review on next transaction event.”
- **LOW:** “No escalation recommended from current evidence.”

---

## 6. UI redesign strategy

### Visual direction

Adopt the existing locked “Minimal Enterprise + Soft Glass” direction, but execute it consistently.

- `#0A0B0D` page background; `#141519` cards; `#1B1D22` raised state.
- Inter or Geist, with tabular numerals for scores, amounts, and timestamps.
- 8px spatial grid; 16px cards; 8px controls; 24px card padding; 1280px content max width.
- One indigo interaction accent (`#5B5FEF`); risk colors only communicate risk state, never decoration.
- Lucide line icons only. Remove emojis, decorative dots, rainbow chart palettes, and moving tickers.

### Hierarchy rules

1. Put the selected case and recommended decision in the top-left quadrant.
2. Treat the composite score as the only hero number in the workspace.
3. Write a human outcome before showing a model input: “Dormant account reactivated and moved funds through linked accounts,” not “F670 + F886.”
4. Put raw data, model factors, XML, and graph mechanics behind progressive disclosure.
5. Use empty space deliberately. One important card should look important because surrounding UI is quiet.

### Cards, tables, graphs

- **Cards:** use one standard treatment. The fusion card alone receives the restrained glass/glow treatment.
- **Charts:** remove any chart that does not change the next action. One small contributor bar or segmented score is enough.
- **Tables:** use a compact case queue with risk badge, account suffix, lifecycle state, and one-line signal. Reserve raw transaction rows for an expander.
- **Network:** render a stable cached view with 3–6 highlighted linked nodes and a caption explaining the relationship. Never open with an unreadable force graph.
- **goAML:** style it as a document preview, not a code block. The XML download is evidence, while the visible “report package summary” carries the story.

### Motion and interactions

- Fusion score assembles once in 1–1.5 seconds with the contributor bars; no artificial loading beyond the actual request.
- Cards fade/slide up 8px, 50ms stagger; hover lifts 2px over 150–200ms.
- Critical badge has a subtle pulse only while it is the active case.
- “Prepare report package” produces a purposeful staged transition: report prepared → hash sealed → ready for review/export.
- No page transitions, particles, bouncing, automatic carousels, spinning “AI” ornaments, or attention-seeking background animation.

### Accessibility and demo reliability

- Never encode severity by color alone; include label and icon/text.
- Maintain readable contrast and a minimum 14px body type.
- Do not depend on hover to communicate evidence.
- Preload an offline scenario and cache all critical response payloads. A network graph or database failure must show “Network enrichment unavailable — decision generated from profile and transaction evidence,” not an error stack.

---

## 7. Feasible innovation opportunities

These are product re-presentations of existing outputs, not new backend work.

| Innovation | Existing source | Why it improves the pitch | Cost / risk |
|---|---|---|---|
| **Case Brief**: a 3-sentence plain-language narrative | SHAP + lifecycle + fusion result | Makes explainability immediately understandable | Low; template-based, must label as generated summary |
| **Decision Ledger**: “Signal → recommendation → evidence package” | Existing score, audit hash, XML | Turns technical plumbing into a defensible operating model | Low |
| **Resilience state**: “Network-enriched” or “ML + transaction fallback” | Graph-service fallback state | Demonstrates mature failure handling rather than hiding it | Low |
| **Guided demo mode** with one deterministic scenario | Existing data/fallback registry | Guarantees narrative and removes file-selection awkwardness | Low |
| **Lifecycle trace**: five-state horizontal track with current state highlighted | Lifecycle engine | Makes “before funds are flushed” visible | Low |

Do not build a conversational agent, real-time stream, live regulatory integration, custom graph model, risk heatmap, multi-tenant admin suite, payments rails, or new bank dashboard. Those create surface area without strengthening the judged moment.

---

## 8. Technical architecture decision

**Keep the architecture unchanged.** It is already more than sufficient for a polished submission.

```
Streamlit investigation workspace
          ↓ REST
FastAPI orchestration
 ├─ XGBoost + SHAP (core explanation)
 ├─ transaction heuristics (behavioral evidence)
 ├─ Neo4j / cached graph (optional enrichment)
 ├─ lifecycle engine (urgency context)
 └─ PostgreSQL/file audit + goAML XML + SHA-256 (case handoff)
```

### Frontend implementation boundaries

- Refactor rendering and CSS only; preserve API shapes and scoring code.
- Reuse the existing fallback registry as an explicit **Demo Mode** data provider.
- Normalize all displayed fusion copy to 40/40/20 and risk thresholds to the documented source of truth.
- Pass graph availability/fallback status to the UI if available; otherwise expose a conservative static “network evidence not loaded” state.
- Build a separate static React/Tailwind landing page only after the Streamlit case workflow works and is visually validated. It must be a first-impression asset, never a second app that judges need to operate.

### Pre-demo engineering checklist

1. Run the prepared scenario with backend online, then with the database/graph path unavailable.
2. Confirm the same selected account, risk level, SHAP reasons, lifecycle stage, report preview, and hash appear every time.
3. Search visible UI strings for `live`, `auto-freeze`, `8 sec`, `4 sec`, `99.8`, `100%`, `I4C`, `admissible`, and `70/30`; remove or qualify unsupported uses.
4. Hide stack traces, missing-resource errors, and Streamlit development chrome from the recording/presentation view.
5. Capture real screenshots only after this checklist passes.

---

## 9. Execution roadmap (48 hours)

### Phase 0 — credibility gate (first 90 minutes; blocking)

| Task | Owner | Effort | Dependency | Impact |
|---|---:|---:|---|---|
| Freeze approved pitch vocabulary and remove contradictory/unsupported visible claims | Product + frontend | 45m | None | Very high |
| Audit 1.0 validation claim; prepare an honest one-sentence response | ML owner | 45m | Validation artifacts | Very high |
| Choose and lock one deterministic critical scenario | Full team | 15m | Fallback data | Very high |

**Done when:** every team member can say what is simulated, what is offline-capable, and what MuleShield does not claim to automate.

### Phase 1 — make the case workflow work (hours 1.5–10; P0)

| Task | Effort | Dependency | Acceptance criterion |
|---|---:|---|---|
| Collapse navigation to Overview / Investigate / Reports | 1h | Existing router | No other screens visible in default product |
| Remove ticker, emojis, mixed color treatments, and redundant top chrome | 1h | CSS | Screenshot reads calm and deliberate |
| Build unified Investigate layout and selected-case state | 3h | Existing alert/account payloads | Queue, decision, explanation visible without page jump |
| Re-render fusion card, lifecycle state, and recommendation wording | 2h | Analysis response | Exactly one prominent risk score; all values match backend |
| Re-render SHAP as three plain-English facts plus technical disclosure | 1.5h | Existing mapping | No raw feature code in default view |
| Make offline demo scenario a first-class button | 1.5h | Fallback files | Works with network/DB unavailable |

**Cut order if behind:** polish on Overview first, never Investigate.

### Phase 2 — make the handoff memorable (hours 10–17; P0/P1)

| Task | Effort | Dependency | Acceptance criterion |
|---|---:|---|---|
| Build report-ready package preview with goAML, hash, and review/export status | 2.5h | XML/hash output | One click clearly ends the investigation |
| Add static/cached network evidence panel with fallback wording | 1.5h | Existing graph fixture | No live Neo4j required |
| Add restrained score/report motion and loading/skeleton states | 2h | Stable layout | Motion supports comprehension, not decoration |
| Visual QA at 1440px and demo laptop resolution | 1h | All above | No overflow, contrast, or awkward Streamlit artifacts |

**Cut order if behind:** graph interactivity first, report preview never.

### Phase 3 — first impression and proof (hours 17–27; P1)

| Task | Effort | Dependency | Acceptance criterion |
|---|---:|---|---|
| Static landing page: hero, problem, 3-step method, trust footer | 4–6h | Product copy | Opens with the same promise as the app |
| Capture screenshots / record the offline fallback walkthrough | 1.5h | Stable demo | Assets show actual product, not mock claims |
| Build concise deck with visual continuity | 3h | Screenshots | Product looks like one designed system |

### Phase 4 — rehearsal, reliability, and reserve (hours 27–48; P0)

| Task | Effort | Acceptance criterion |
|---|---:|---|
| Three timed offline-path rehearsals | 2h | A different team member can run it in <2 minutes |
| Failure drill: backend slow/offline, Neo4j offline, graph unavailable | 2h | Graceful, truthful fallback at each point |
| Fix only bugs that affect story, legibility, or reliability | 5h | No scope expansion |
| Pitch/Q&A rehearsal and deck refinement | 3h | Claims stay defensible under questions |
| Reserve | 9h | Protects the submission from late breakage |

### Non-negotiable priority order

1. Claim audit and validation framing
2. Working offline case workflow
3. Report/evidence handoff
4. Visual coherence
5. Landing page and deck
6. Optional graph polish / micro-interactions

---

## 10. Perfect live demo: 100 seconds

**Precondition:** app is open at the landing or Guided Demo state; fallback scenario is already available; do not rely on Docker, Neo4j, external APIs, Wi-Fi, or manual CSV hunting.

| Time | Screen / click | What the presenter says | What the judge should conclude |
|---:|---|---|---|
| 0–10s | Landing | “As India’s payment rails scale, a mule account can move victim funds before a manual review begins. MuleShield gives AML teams a defensible case before the money is flushed.” | Clear human/business problem |
| 10–20s | Click **Run guided investigation** | “This is an investigator workspace, not another fraud dashboard.” | Intentional product design |
| 20–35s | Click **Analyze case** | “We fuse profile behavior, transaction patterns, and network evidence—then keep working if network enrichment is unavailable.” | Technical differentiation + resilience |
| 35–55s | Fusion reveal / case brief | “This account is critical because a dormant account reactivated, showed high pass-through velocity, and connected to already-risky accounts. MuleShield recommends immediate review and escalation under bank policy.” | Explainable, safe recommendation |
| 55–70s | Expand network/lifecycle only if stable | “The lifecycle shows why timing matters: this account is in the stage where funds may be dispersed. The graph corroborates the linked pattern; the decision does not depend on a graph server being up.” | Operational insight, not graph theater |
| 70–88s | Click **Prepare report package** | “Instead of leaving an analyst with a score, MuleShield creates a review-ready goAML package and seals the evidence record with a SHA-256 hash.” | Unique end-to-end value |
| 88–100s | Report card / close | “That is financial trust infrastructure: explainable detection, resilient investigation, and accountable handoff for the next billion digital users.” | Strong track alignment |

### Backup demo plan

- **If backend is down:** use the cached Guided Demo result; narrate it explicitly as an offline-resilient demo fixture, not a live decision.
- **If graph is down:** keep the “ML + transaction evidence” fallback badge visible; do not apologize or troubleshoot live.
- **If XML download fails:** show the pre-rendered package preview and evidence hash, then state the export endpoint is available in the full stack.
- **Never switch to system-health pages, raw logs, Swagger, terminal windows, or model metric screens during the primary demo.**

---

## 11. Presentation strategy

### Desired judge perception

“This team understands both the engineering and the operating reality of financial-crime response. They did not just train a model; they designed a credible handoff system around it.”

### Deck (seven slides maximum)

1. **The urgency:** funds move faster than manual review. Avoid unsupported national-statistic claims unless sourced on the slide.
2. **The reframing:** protecting payment access means protecting the people newly brought onto digital rails from mule-account abuse.
3. **MuleShield:** one clear system image—Detect → Explain → Prepare evidence.
4. **Live product / recorded fallback:** show the investigation screen, not architecture first.
5. **Why it is defensible:** fusion, SHAP-to-language, lifecycle, and report/evidence package. Use a four-box diagram.
6. **Reliability and deployment:** FastAPI, offline graph degradation, audit trail, on-premise fit. Mention “designed for” rather than “production-ready.”
7. **Close:** “See the mule before the money moves.” State the realistic next step: supervised bank pilot / validation with real institutional data.

### Technical depth, in the right order

Lead with workflow and impact. Reveal architecture only after the judge asks “how.” Have one backup slide with the precise 40/40/20 fusion formula, fallback path, model evaluation caveat, and architecture. This will read as mature rather than evasive.

### Honest validation answer

Do not present the perfect AUC as evidence of production readiness. Say:

> “Our current held-out split is small—only 16 positive samples—so we treat the reported perfect ranking metric as a signal to audit, not a production claim. For a pilot, we would run temporal and institution-level validation, threshold calibration, and analyst review before operational use.”

This answer is stronger than defensiveness. It demonstrates model-risk awareness, exactly what a compliance product should have.

---

## 12. Risk register and mitigations

| Risk | Severity | Early signal | Mitigation | Owner |
|---|---|---|---|---|
| Unsupported claims damage credibility | Critical | “Live,” “auto-freeze,” absolute metrics visible | Claim sweep; use qualified copy and pitch-safe vocabulary | Product lead |
| Validation leakage/overfitting question | Critical | Judge asks about 1.0 AUC / small positives | Audit or state limitation plainly; do not headline score | ML owner |
| Live infrastructure fails | Critical | Neo4j/Postgres/API unavailable | Deterministic cached default; rehearse it as primary | Demo owner |
| UI redesign expands into a rewrite | High | New components/pages keep being proposed | Enforce P0 workflow boundary; timebox landing page | Engineering lead |
| Streamlit visual limitations leak into demo | High | Browser/chrome/widget artifacts in screenshots | CSS QA on target resolution; record reliable flow | Frontend owner |
| Graph visual is slow/unreadable | Medium | Force graph loads late / labels overlap | Cached static graph, small node count, collapsed by default | Frontend owner |
| Design becomes “cyberpunk demo” | Medium | Tickers, glow, rainbow metrics, motion everywhere | Follow token/motion rules; use glass once | Design owner |
| Presentation overload | Medium | Architecture shown before problem, >7 slides | 100-second product narrative, technical appendix backup | Presenter |
| Privacy/fairness concern | Medium | Questions about demographics or data origin | Hide sensitive exploratory UI; explain that outputs require institution validation and human review | Product + ML |
| Unresolved prior overclaim incident | High | Asked in Q&A | Do not invent a response; resolve with team before pitch or acknowledge only verified scope | Team lead |

---

## Definition of done

MuleShield is ready to submit only when all of the following are true:

- A first-time viewer can explain the product, the selected case, the recommendation, and the report handoff in under two minutes.
- The default demo succeeds without Neo4j, PostgreSQL, external LLMs, or venue Wi‑Fi.
- There are only three visible navigation destinations and one obvious primary action.
- Every visible score, threshold, formula, and capability statement is consistent with the backend and documented 40/40/20 fusion logic.
- The current live ticker, unsupported automation claims, raw model/data pages, and misleading readiness/performance claims are not in the primary experience.
- The report package is the ending, not an afterthought.
- The team can answer the validation question honestly and precisely.
- Final screenshots, the demo recording, and deck all share the same visual language and only show working or clearly simulated capability.

If time becomes scarce, cut optional visual features—not the investigator workflow, claim audit, offline fallback, or evidence handoff. The winning version of MuleShield is not the one with the most screens. It is the one that makes a judge believe a bank investigator could trust the next action.
