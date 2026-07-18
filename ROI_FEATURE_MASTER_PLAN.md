# MuleShield AI — ROI Feature Master Plan

## Executive Summary

MuleShield is already technically credible. The remaining opportunity is not another model, page, or integration; it is making the existing intelligence feel inevitable, understandable, and memorable in a two-to-three-minute judge experience.

The winning strategy is to turn the product into a sequence of visible decisions:

**A suspicious trail appears → MuleShield investigates → evidence unfolds → a recommendation becomes clear → the case is sealed for human handoff.**

The product should make judges remember three moments:

1. The risk score assembles from three independent evidence sources.
2. The AI Case Brief explains the finding in plain language while preserving technical provenance.
3. The evidence package seals with a visible integrity state and becomes ready for review.

No backend rewrite, ML retraining, database redesign, authentication, multi-tenancy, or complex agent is justified in the remaining window. All recommendations below reuse the current React frontend, FastAPI contracts, SHAP output, graph context, lifecycle state, goAML XML, SHA-256 hash, Decision Ledger, and offline fixtures.

The interaction direction follows two useful product principles: AI suggestions should expose why they were made and leave the operator in control, as demonstrated by Linear’s triage suggestions; motion should be brief, precise, and tied to system feedback, as recommended by Apple’s Human Interface Guidelines. [Linear Triage Intelligence](https://linear.app/docs/triage-intelligence) · [Apple Motion HIG](https://developer.apple.com/design/human-interface-guidelines/motion)

### Scoring model

- **Judge Impact:** likelihood of improving immediate judge perception.
- **User Delight:** reduction in friction or increase in confidence for an investigator.
- **Innovation:** distinctiveness beyond a conventional fraud dashboard.
- **Demo Value:** usefulness during the live narrative.
- **Engineering Effort:** 1 = small polish, 10 = major implementation.
- **Risk:** 1 = very safe, 10 = likely to destabilize the demo.
- **ROI:** `(Judge Impact + User Delight + Innovation + Demo Value) / (Engineering Effort + Risk) × 2`, capped at 10.
- **Memorability:** probability that a judge recalls the feature after the demo.
- **Hackathon Score:** holistic score for pitch usefulness, clarity, trust, and technical proof.

## Top 25 ROI Features

### P0 — Implement before submission

| # | Feature | Problem solved / why judges care | Impact / effort / ROI | Time / dependencies | Mockup and motion | Acceptance criteria |
|---:|---|---|---|---|---|---|
| 1 | **Guided Investigation Launch** | Removes blank-state hesitation and gives the presenter a deterministic opening. Judges see the product working immediately. | Judge 10 · Delight 9 · Innovation 7 · Demo 10 · Effort 2 · Risk 1 · **ROI 10** · Memorable 9 · Hackathon 10 | 1–2h. Existing fallback fixture and router. | One primary “Run guided investigation” action. Button compresses, then transitions to the case workspace. | Works offline; opens the same case every time; completes in one click; label states that it is a guided demo fixture. |
| 2 | **Evidence Unfolding Sequence** | Current data can feel dumped onto the screen. Sequential evidence creates narrative and gives judges time to understand the system. | 10 · 9 · 8 · 10 · 3 · 2 · **ROI 9.5** · 10 · 10 | 2–3h. Framer Motion and existing case fields. | “Profile signal” → “Transaction pattern” → “Network context” → “Recommendation” appear in four short stages. | Every stage is skippable; no information is animation-only; reduced motion shows the completed state immediately. |
| 3 | **Composite Risk Assembly** | A static score looks like a metric. An assembling score makes fusion tangible and demonstrates the 40/40/20 architecture. | 10 · 9 · 8 · 10 · 3 · 2 · **ROI 9.5** · 10 · 10 | 2h. Existing risk fields. | Three contributor bars animate in, then converge into one score. Final state shows exact weights. | Final value exactly matches backend/fallback data; no invented latency; animation finishes under 1.2s. |
| 4 | **AI Case Brief** | Raw SHAP labels are not a story. A bounded narrative makes the model legible to non-ML judges and investigators. | 10 · 10 · 8 · 10 · 3 · 1 · **ROI 10** · 10 · 10 | 2–3h. Existing feature map, SHAP, lifecycle, and explanation fields. | Heading types in once, then three evidence bullets resolve with checkmarks. | Copy is generated only from known response fields; technical factors remain inspectable; no chatbot claims. |
| 5 | **Investigator Recommendation Card** | Scores do not answer “what happens next?” A recommendation converts analytics into supervised workflow. | 10 · 10 · 8 · 10 · 2 · 1 · **ROI 10** · 9 · 10 | 1–2h. Severity thresholds already exist. | Card enters after Case Brief with “Recommended next step” and an explicit boundary: review, escalation, monitoring, or no escalation. | Never says automatic freeze or regulatory submission; recommendation differs correctly by severity. |
| 6 | **Evidence Timeline** | The current product risks feeling like disconnected panels. A timeline turns signals into a causal investigation. | 9 · 9 · 8 · 10 · 3 · 2 · **ROI 9** · 10 · 9 | 2–3h. Existing evidence, lifecycle, and case state. | Nodes draw from left to right: reactivation → velocity → network link → recommendation. | Timeline includes timestamps where available; missing timestamps are labeled; current stage is visually distinct. |
| 7 | **Sealed Evidence Moment** | goAML and SHA-256 are technically strong but easy to overlook. A visible seal makes the backend’s trust layer emotionally legible. | 10 · 9 · 9 · 10 · 3 · 2 · **ROI 9.5** · 10 · 10 | 2h. Existing XML and hash. | “Preparing” → “Hash verified” → “Ready for review/export”; a restrained checkmark resolves at the end. | Hash is the existing value; export works; state is honest if XML is absent; no “admissible” or “submitted” claim. |
| 8 | **Decision Ledger Reveal** | The audit trail is otherwise invisible. Showing the chain signal → recommendation → handoff differentiates MuleShield from a classifier. | 9 · 9 · 9 · 9 · 3 · 1 · **ROI 9.7** · 10 · 10 | 2–3h. Existing audit/hash fields and frontend state. | Three ledger rows stamp in sequentially with timestamps and status chips. | Ledger shows the selected case, recommendation, analyst review state, and evidence hash; no fake audit events. |
| 9 | **Compact Network Evidence** | A force graph can look like technical theater. A small, stable relationship view provides corroboration without derailing the story. | 8 · 8 · 8 · 8 · 3 · 3 · **ROI 8** · 8 · 8 | 2–3h. Existing graph output or static fallback. | Central account node pulses once; linked nodes appear with labeled relationship edges. | Works when Neo4j is unavailable; fallback is explicit; no unreadable full-screen graph. |
| 10 | **Truthful Offline State** | Demo failure is catastrophic. A transparent fallback makes resilience a product strength instead of an apology. | 10 · 9 · 8 · 10 · 2 · 1 · **ROI 10** · 9 · 10 | 1–2h. Existing fallback JSON/fixture provider. | Small “Guided demo · offline provider” badge; no fake loading or live telemetry. | Full flow works without API, Neo4j, PostgreSQL, or Wi-Fi; copy never implies live data. |
| 11 | **Case Queue with Narrative Signals** | A generic account list forces the judge to infer priority. One-line signals make triage glanceable. | 9 · 9 · 7 · 9 · 2 · 1 · **ROI 10** · 8 · 9 | 1–2h. Existing alerts. | Rows show severity, account suffix, lifecycle, score, and one human-readable reason. | Sorting is by risk/lifecycle urgency; selected row persists; queue is usable by keyboard. |
| 12 | **One-Click Report Handoff** | The final action is currently buried in a compliance screen. A clear ending gives the demo closure. | 9 · 9 · 8 · 10 · 2 · 1 · **ROI 10** · 9 · 10 | 1–2h. Existing report/export functions. | Primary header action changes from “Prepare evidence” to “Package ready” after completion. | Export XML/JSON works; UI clearly says “ready for investigator review/export.” |
| 13 | **Presenter Reset / Demo Mode** | A live demo can become unrehearsed and fragile after a click. Reset restores the known story instantly. | 9 · 8 · 6 · 9 · 2 · 1 · **ROI 9** · 8 · 9 | 1h. Client state only. | Command-menu or quiet “Reset guided case” action; reset crossfades to the initial queue. | Reset clears transient state without reload; does not delete backend data. |
| 14 | **Command Bar Shortcuts** | Premium tools feel fast when the primary actions are discoverable and keyboard-accessible. | 7 · 8 · 7 · 7 · 3 · 2 · **ROI 7.5** · 7 · 8 | 2–3h. React Router and client state. | `⌘K` opens “Run guided case,” “Open evidence,” “Reset demo,” and case search. | Every command has a visible button equivalent; no command is required to complete the demo. |
| 15 | **Credibility Copy Sweep** | Unsupported “live,” “auto-freeze,” and perfect-readiness language can erase trust instantly. | 10 · 10 · 7 · 10 · 1 · 1 · **ROI 10** · 9 · 10 | 1h. Search rendered strings and source copy. | Replace claims with “recommended,” “simulated,” “review-ready,” and “offline-capable.” | No unsupported claims appear in primary routes, landing page, screenshots, or demo narration. |

### P1 — Implement only if P0 is stable

| # | Feature | Problem solved / why judges care | Impact / effort / ROI | Time / dependencies | Mockup and motion | Acceptance criteria |
|---:|---|---|---|---|---|---|
| 16 | **Scenario Switcher** | Shows that the product is a reusable investigation system, not a single hardcoded case. | 7 · 8 · 7 · 8 · 3 · 2 · **ROI 8** · 8 · 8 | 2h. Existing scenario fixtures. | Three quiet scenario chips: dormant ring, student recruitment, structuring. | Switching preserves layout and produces honest case-specific narratives. |
| 17 | **Evidence-to-Factor Hover Link** | Judges often ask “which evidence caused that?” Direct linking answers immediately. | 8 · 8 · 8 · 8 · 4 · 2 · **ROI 8** · 8 · 8 | 2–3h. Stable IDs for factors/evidence. | Hovering a brief bullet highlights its corresponding contributor bar and timeline node. | Keyboard focus produces the same relationship; no hover-only information. |
| 18 | **Report Preview with Real Metadata** | Raw XML feels unfinished. A document-like preview makes the compliance artifact feel real. | 8 · 8 · 8 · 9 · 3 · 2 · **ROI 8** · 8 · 8 | 2h. Existing XML/case fields. | Clean letterhead, case metadata, evidence summary, integrity strip, export actions. | Never impersonates a government portal; all displayed values come from the selected case. |
| 19 | **Methodology as an Inspector Drawer** | Technical judges need depth, but a separate analytics dashboard adds cognitive load. | 7 · 7 · 8 · 7 · 3 · 1 · **ROI 8** · 6 · 8 | 1–2h. Existing methodology data. | “How this decision was formed” drawer from the score surface. | Shows 40/40/20, SHAP factors, graph availability, and fallback state; hidden from the primary narrative. |
| 20 | **Case Search with Command Highlighting** | Search becomes more credible when matching context is visible, not just account IDs. | 7 · 8 · 6 · 7 · 3 · 2 · **ROI 7** · 6 · 7 | 2h. Client-side case collection. | Search results highlight matched account, severity, or signal phrase. | Search is case-insensitive, clears safely, and opens the selected case. |
| 21 | **Analyst Review Capture** | AI should recommend, not silently decide. A small accept/change state makes human control visible. | 8 · 9 · 8 · 8 · 4 · 2 · **ROI 8** · 8 · 9 | 2–3h. Frontend session state; no backend schema change. | “Accept recommendation” / “Mark for review” becomes a ledger state. | State is explicitly local/demo-only unless backend persistence exists; no claim of institutional approval. |

### P2 — Future roadmap, do not risk the submission

| # | Feature | Problem solved / why judges care | Impact / effort / ROI | Time / dependencies | Mockup and motion | Acceptance criteria |
|---:|---|---|---|---|---|---|
| 22 | **Interactive Network Exploration** | Lets an investigator inspect connected accounts in depth. | 7 · 7 · 8 · 6 · 7 · 5 · **ROI 5** · 7 · 6 | 1–2 days. Stable graph API and layout performance. | Pan/zoom graph with relationship filters and node drawer. | Must remain responsive with real graph data and preserve the decision context. |
| 23 | **Collaborative Case Notes** | Supports real AML team handoff and institutional memory. | 7 · 8 · 7 · 6 · 8 · 6 · **ROI 4** · 6 · 6 | Multi-user persistence required. | Threaded notes and mentions beside the ledger. | Requires authenticated persistence and audit semantics. |
| 24 | **Temporal Risk Replay** | Shows how risk evolved across transactions and lifecycle stages. | 8 · 8 · 8 · 7 · 8 · 5 · **ROI 5** · 8 · 7 | Historical event model required. | Scrubbable case playback with synchronized score and graph. | Must use real historical timestamps, not synthetic animation. |
| 25 | **Institutional Feedback Loop** | Lets analysts label useful or incorrect explanations for future model governance. | 8 · 8 · 9 · 6 · 9 · 6 · **ROI 4** · 7 · 7 | Backend storage, governance, and review workflow. | Factor feedback attached to the Case Brief. | Requires a governed data model and cannot be simulated as production learning. |

## Top 10 WOW Moments

### 1. The quiet opening

The Cases screen opens with one critical case and a single sentence: “Four signals need a defensible next move.” The judge immediately understands that this is an operational workspace, not a chart collection.

### 2. Guided investigation launch

The presenter clicks **Run guided investigation**. The selected case moves into the workspace; the queue remains visible, preserving context. A small offline-provider label makes resilience feel intentional.

### 3. Score assembly

Profile, transaction, and network contributors appear in order. The three bars settle at 40%, 40%, and 20% weights, then resolve into the composite score. The judge sees the architecture as a decision, not an architecture diagram.

### 4. Evidence finds its language

The Case Brief types in from verified signals: dormant reactivation, high pass-through velocity, linked accounts. Each sentence maps to a visible factor. This is the moment “explainable AI” becomes concrete.

### 5. Human control remains visible

The recommendation card says “Immediate review and escalation under bank policy,” not “account frozen.” This earns trust because the product knows the boundary between intelligence and authority.

### 6. Lifecycle turns urgency into a story

The lifecycle trace moves from DORMANT toward BEING FLUSHED, showing why timing matters. The current state is emphasized without introducing another dashboard chart.

### 7. Network corroboration

Three linked nodes expand around the selected account. The graph is compact and legible; it supports the case instead of becoming the case.

### 8. Evidence becomes an artifact

The presenter clicks **Prepare evidence**. The interface steps through preparing, sealing, and hash verification. A plain-language report preview replaces the feeling of “downloaded XML.”

### 9. Decision Ledger closure

The ledger stamps the path: signal detected → recommendation recorded → evidence sealed. This is the strongest distinction from a classifier demo.

### 10. Honest resilience finish

The presenter mentions that the same investigation can continue without Neo4j or venue Wi-Fi. The UI already proves it, so the claim feels engineered rather than defensive.

## Demo Flow Improvements

### Target: 120 seconds

| Time | Interaction | Presenter narrative | Judge takeaway |
|---:|---|---|---|
| 0–10s | Cases opens | “MuleShield gives an AML investigator the next defensible move—not another risk dashboard.” | Clear category and problem |
| 10–20s | Click guided investigation | “I’ll open a prepared investigation so the evidence path is repeatable.” | Product feels intentional |
| 20–38s | Score assembly | “The decision combines profile, transaction, and network evidence at 40/40/20.” | Technical depth is understandable |
| 38–58s | Case Brief unfolds | “The model found a dormant reactivation, high-velocity pass-through, and linked accounts.” | AI is explainable |
| 58–72s | Recommendation/lifecycle | “It recommends immediate review and escalation; it does not silently execute a bank action.” | Trust and human control |
| 72–88s | Network evidence | “The network corroborates the pattern, but the workflow remains resilient if enrichment is unavailable.” | Engineering maturity |
| 88–110s | Prepare evidence | “MuleShield turns the decision into a review-ready package.” | End-to-end value |
| 110–120s | Seal and ledger | “The recommendation, evidence, and hash are now one accountable handoff.” | Memorable close |

Reduce cognitive load by removing all nonessential routes from the main demo, avoiding raw model metrics, and narrating only one case. Keep Methodology as a backup if a technical judge asks how the score is formed.

## Screens to Improve

### Cases

Current problems:

- Dashboard language encourages monitoring rather than action.
- KPI cards use unsupported estimates and operational claims.
- Queue priority is not connected to a human-readable narrative.

Improvements:

- Replace KPI wall with four action-linked summary facts.
- Make the queue the visual center of gravity.
- Add guided investigation as the only dominant CTA.
- Show severity, lifecycle, score, and one reason per row.

Estimated effort: 3–4 hours including responsive polish.

### Investigate

Current problems:

- Evidence, score, lifecycle, graph, and compliance are separate mental models.
- Technical labels appear before the human explanation.
- The user must infer the next action.

Improvements:

- Use a three-pane investigation workspace.
- Sequence the evidence reveal.
- Make the recommendation the central output.
- Keep graph and SHAP detail behind progressive disclosure.

Estimated effort: 5–7 hours including motion.

### Evidence

Current problems:

- Raw XML looks like an implementation artifact.
- Hash and audit state lack narrative context.
- Export is not positioned as the product’s conclusion.

Improvements:

- Use a report preview with real case metadata.
- Present hash verification as a sealed integrity state.
- Show Decision Ledger beside the artifact.

Estimated effort: 3–4 hours.

### Methodology

Current problems:

- Model analytics and dataset surfaces distract from the primary workflow.
- Perfect validation metrics create avoidable credibility risk.

Improvements:

- Move technical detail into a secondary route/drawer.
- Show 40/40/20, SHAP provenance, graph fallback, and decision boundaries.
- Keep validation caveats available for Q&A without making them the hero.

Estimated effort: 1–2 hours.

## Motion Opportunities

Use motion only when it communicates state, causality, or completion. Apple’s guidance is especially relevant here: brief, precise feedback should help users understand what happened without making them wait or forcing attention onto decoration. [Apple Motion HIG](https://developer.apple.com/design/human-interface-guidelines/motion)

- Case selection: 180ms surface transition.
- Score assembly: synchronized number count and contributor bars.
- Brief generation: one-time text reveal, not a perpetual typing animation.
- Evidence timeline: causal nodes draw in sequence.
- Network context: small node expansion around the selected account.
- Report preparation: explicit state machine, not a generic spinner.
- Critical status: restrained pulse only while active.
- Buttons: 0.98 press scale and subtle lift.
- Reduced motion: show final states immediately.

Avoid particles, background data streams, bouncing cards, decorative chart motion, artificial “AI thinking” delays, and animations that hide values from screen readers.

## Visual Polish

### Typography

- Inter or DM Sans for UI text.
- IBM Plex Mono for account IDs, timestamps, XML, and hashes.
- Tabular numerals for scores.
- Headings use tight tracking and restrained weight.

### Spacing and hierarchy

- 8px base grid.
- 24px card padding.
- 32px section spacing.
- One dominant surface per screen.
- Use empty space to signal confidence.

### Cards

- Quiet dark surfaces for supporting content.
- One focal treatment for the decision surface.
- Borders and shadows remain subtle.
- No colored card borders unless severity requires it.

### Icons and illustrations

- Lucide icons only.
- No emoji, clip-art, or generic shield illustrations.
- The only visual metaphor needed is the evidence path: signals becoming a decision becoming a sealed package.

### Micro-interactions

- Hover lifts 2px.
- Focus states are visible and indigo.
- Case rows highlight without changing their meaning.
- Copy-to-clipboard for hashes should confirm with a quiet toast.
- Export completion should change the action label to “Package ready.”

## Things to Remove

- Moving government or threat-intelligence tickers.
- “Auto-freeze,” “live I4C,” “admissible,” and unsupported SLA claims.
- Estimated interdicted funds as a hero metric.
- Duplicate score gauges, charts, and KPI cards.
- Demographic vulnerability charts in the primary workflow.
- Raw feature codes in default views.
- Generic chatbot surfaces.
- Full-screen force graphs.
- System health as a visible destination.
- Dataset intelligence as a visible destination.
- Decorative gradients, rainbow palettes, and emoji labels.
- Any interaction that requires live Neo4j, PostgreSQL, Wi-Fi, or external AI providers to succeed.

## Implementation Order

### P0 checklist

- [ ] Run credibility copy sweep across React, landing, and demo script.
- [ ] Make Guided Investigation deterministic and offline-first.
- [ ] Implement Case Queue with narrative signals.
- [ ] Implement Composite Risk Assembly.
- [ ] Implement Evidence Unfolding Sequence.
- [ ] Implement AI Case Brief with technical disclosure.
- [ ] Implement Investigator Recommendation Card.
- [ ] Implement Lifecycle and Evidence Timeline.
- [ ] Implement compact Network Evidence with truthful fallback.
- [ ] Implement Sealed Evidence Moment and export actions.
- [ ] Implement Decision Ledger reveal.
- [ ] Add presenter reset.
- [ ] Run three complete offline rehearsals.

### P1 checklist

- [ ] Add scenario switcher.
- [ ] Add evidence-to-factor linking.
- [ ] Improve report preview metadata.
- [ ] Add methodology inspector.
- [ ] Add command bar and case search.
- [ ] Add local analyst review state.

### P2 checklist

- [ ] Interactive graph exploration.
- [ ] Collaborative notes.
- [ ] Temporal risk replay.
- [ ] Governed analyst feedback loop.

## Final Success Criteria

- The first 10 seconds communicate the problem and the product category.
- The judge sees one memorable case rather than many disconnected features.
- The score is explained before it is celebrated.
- The AI recommends; the investigator remains in control.
- The graph corroborates without becoming visual noise.
- The final screen is an accountable evidence handoff.
- The full demo works offline.
- Every visible claim is defensible.
- Any feature that does not improve memorability, understanding, enterprise confidence, or the emotional close is removed.

The final product should leave the judge with one sentence:

> MuleShield did not just detect suspicious money movement; it showed me why the case mattered, what an investigator should do next, and how the evidence becomes accountable.
