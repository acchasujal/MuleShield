# PECHACKS_STRATEGY.md — PEC Hacks 4.0 Research & Submission Strategy

> Tags: `[FACT]` verified via web search this session or prior session · `[UNVERIFIED]` referenced in earlier conversation but not independently confirmed this session · `[INFERENCE]` reasoned · `[RECOMMENDATION]` strategic call · `[RISK]` flagged concern.

---

## 1. Event Facts (Verified)

`[FACT]`
- **Event**: PEC Hacks 4.0, a 36-hour national-level student hackathon.
- **Organizer**: Panimalar Engineering College (PEC), Chennai, Tamil Nadu.
- **Dates**: August 29–30, 2026.
- **Format**: Offline, in-person.
- **Eligibility**: Engineering students; also features a Best All-Girls Team Award and a High School Track.
- **Prize pool**: Reported as ₹80,00,000 (8,000,000) per EvePaper listing — `[FACT — third-party aggregator, not the primary source; treat prize figure as likely but not primary-source-confirmed]`.
- **Registration deadline**: Reported as 2026-07-22 per EvePaper — same caveat as above.
- **Domains/tracks**: AI, Web3, HealthTech, FinTech, EdTech, Sustainability, Open Innovation (per EvePaper description).
- **Process**: Registration → idea shortlisting → 1:1 mentoring for selected teams → 36-hour build → final pitches to a judge panel.
- **Official sites**: pechacks.org (primary) and pec-hacks.devfolio.co (Devfolio listing).

`[UNVERIFIED — from earlier in this conversation, not re-confirmed this session]`
- FinTech track brief: *"Reimagine money, banking, and financial access. Build the infrastructure for the next billion users."*
- Judging panel composition skewing toward engineers/CTOs (Freshworks, Cognizant, Vault Infosec were named).
- **Action required before finalizing pitch**: verify current judge list and exact track briefs directly on pechacks.org, since these may be updated closer to the event and the earlier reference was not re-verified this session.

## 2. Previous Editions / Winners

`[GAP — not found]` No previous-winner data for PEC Hacks 1.0–3.0 surfaced in research this session or prior. `[RECOMMENDATION]` Do not fabricate winner patterns. If you want this, search Devfolio's PEC Hacks 3.0 project gallery directly closer to submission — Devfolio typically publishes past winning project pages.

## 3. Judging Criteria

`[GAP]` No PEC Hacks-specific published rubric found. `[INFERENCE]` Standard student-hackathon judging (used generically across MLH-style events) typically weighs: **Technical difficulty, Design/UX, Completion/functionality, Impact/business potential, Presentation**. Treat this as a reasonable default, not a confirmed PEC Hacks rubric.

## 4. FinTech Track vs Open Innovation — Fit Analysis

| Dimension | FinTech | Open Innovation |
|---|---|---|
| Track brief alignment | `[UNVERIFIED brief]` "infrastructure for the next billion users" — mule detection is direct financial-crime infrastructure, no reframe needed | Would require no reframe either, but dilutes the fintech-specific differentiation (compliance/goAML) |
| Judge domain fit | Strong if panel includes engineers with fraud/compliance exposure | Weaker — less specialized appeal |
| Competitive field | `[INFERENCE]` Likely crowded with payment/lending/budgeting apps — a compliance/AML angle stands out as differentiated within the track | `[INFERENCE]` Broader, less predictable competition |

**`[DECISION]` Recommended track: FinTech.** Mule-account detection is financial infrastructure, not adjacent to it — this is a natural fit, not a stretch, unlike scenarios (e.g., a civic-accountability platform) that would require contorted "civic fintech" reframing.

## 5. Why MuleShield Fits

`[RECOMMENDATION — pitch narrative]` Digital financial inclusion at UPI scale creates new attack surface: mule accounts recruited from newly-banked, vulnerable populations. Protecting that rail *is* "infrastructure for the next billion users" — not a stretch of the brief, its literal application to fraud/trust infrastructure rather than payments/lending infrastructure.

## 6. Risks & Mitigation

| Risk | Severity | Mitigation |
|---|---|---|
| `[RISK]` ROC-AUC = 1.0 / PR-AUC = 1.0 on only 16 positive validation samples reads as overfitting/leakage to a technical judge | **High — credibility-breaking if unaddressed** | Re-audit for leakage beyond F3912 exclusion; if unresolved, reframe metric honestly in pitch (e.g., present cross-validated results, not a single split) rather than lead with the perfect score |
| `[RISK]` Prior "overclaiming incident" referenced but never specified by the user | **High — unresolved integrity risk** | User must identify and confirm resolution before the event; do not present unverified fixed claims |
| `[RISK]` Docker + Neo4j + PostgreSQL live demo on unknown hackathon wifi | **High — demo failure risk** | Default demo path must be offline-capable (ML score only, cached/static graph); live DB stack as bonus only |
| `[RISK]` "100% GitHub Readiness / Portability Score" self-reported in project docs is marketing language, not evidence | **Medium** | Strip from any pitch material; judges discount self-scored metrics |
| `[RISK]` FinTech track brief and judge panel details unverified this session | **Medium** | Re-check pechacks.org before finalizing pitch deck |

## 7. Submission Strategy

`[RECOMMENDATION]`
1. Lead the pitch with the compliance/evidence differentiator (goAML + SHA-256 hashing), not the ML model — this is the least-replicated asset among likely competitors.
2. Proactively address the validation-metric risk before a judge raises it.
3. Keep the "next billion users" framing explicit and literal — fraud protection as inclusion infrastructure — rather than assuming judges will make that connection unprompted.

## 8. Demo & PPT Strategy

See `BUILD_GUIDE.md` §Demo Flow and §PPT Flow for the executable version. Strategic principle: **rehearse the offline fallback path as the default demo**, not the live-infra path.

## 9. Judge Q&A Prep (anticipated questions)

`[RECOMMENDATION]`
- *"How is 1.0 AUC not overfitting on 16 positives?"* → Have a rehearsed, honest answer ready (cross-validation plan, leakage audit performed).
- *"What was the prior overclaiming issue?"* → User must resolve this before the event; do not improvise an answer live.
- *"Does this actually move or hold money?"* → No — be direct that this is fraud/compliance infrastructure protecting the money layer, not a payments product. Don't overclaim fintech-core status.
- *"What happens if your graph DB goes down?"* → Point to the documented graceful degradation to standalone ML mode (per ARCHITECTURE.md §5, RELEASE_READINESS.md).

## 10. References

- https://pechacks.org/ (primary site)
- https://pec-hacks.devfolio.co/ (Devfolio listing)
- https://evepaper.com/competitions/pec-hacks-4-0/ (third-party aggregator — prize pool, deadline, track list; not primary-source-confirmed)
- https://docs.pechacks.org/ (PEC Hacks 3.0 reference, prior edition)
