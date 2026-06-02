# TASK_QUEUE.md
_Full project backlog. Load only when planning or assigning work. ~600 tokens._

---

## P0 — CRITICAL PATH (must complete for shortlist)

| Task | Owner | Time | Deps | Output |
|---|---|---|---|---|
| T1: Copy ML artifacts | Vikram | 30m | — | `backend/ml_artifacts/` (5 files) |
| T2: FastAPI ML endpoints | Vikram/Dhiren | 3h | T1 | `/predict/single` + `/predict/batch` live |
| T3: Score fusion | Dhiren | 2h | T2 | `calculate_composite_risk()` in risk_scoring.py |
| T4: Signal explanation card | Sujal | 4h | T2 | `SignalCard.jsx` wired to account detail page |
| T5: Batch CSV upload UI | Sujal | 3h | T2 | `BatchAnalysis.jsx` + `RiskTable.jsx` |
| T6: Mule lifecycle classifier | Vikram | 4h | T2 | `mule_stage` field in RiskResponse |
| T7: Auto-STR trigger | Dhiren | 2h | T3, T4 | STR modal auto-opens when score ≥ 80 |
| T13: Dataset documentation | Sujal | 2h | — | Dataset page + public PDF link |

**P0 total: ~20.5 hours**

---

## P1 — HIGH VALUE (improves ranking significantly)

| Task | Owner | Time | Deps | Output |
|---|---|---|---|---|
| T8: Feature importance viz | Vikram | 3h | T2 | Bar chart: top-20 features by SHAP/importance |
| T9: Alert funnel widget | Sujal | 2h | T5 | Dashboard widget: 9082 → N animated count |
| T10: Account type + region charts | Sujal | 3h | T2 | F3886 (account type) + F3890 (region) fraud rate charts |
| T11: Behavioral profile card | Sujal | 3h | T2 | Account age bucket, occupation, in/out ratio display |
| T12: PR-AUC model metrics page | Vikram | 2h | T8 | Precision-recall curve + confusion matrix screen |
| **BRANDING: Union Bank → Bank of India** | Shriraj | 1h | — | Zero "Union Bank" anywhere in UI/PPT/code |
| **PPT: Replace business model slide** | Sujal | 1h | — | 3-phase deployment roadmap slide |
| **PPT: Add F3889/F3891 insights slide** | Sujal | 2h | — | Dataset insights: 89% G365D, 28% students |

**P1 total: ~17 hours**

---

## P2 — NICE TO HAVE (only if time remains)

| Task | Owner | Time | Deps | Output |
|---|---|---|---|---|
| T14: Full demo scenario (upload DataSet.csv) | All | 2h | T5, T9 | Live demo: 9082 accounts → 16 critical → STR |
| T15: Integration test + demo rehearsal | All | 3h | All | End-to-end clean demo, timed under 5 min |
| **Backup: pre-compute demo_results.json** | Vikram | 30m | T2 | Fallback JSON for demo mode |
| **Backup: Demo Mode button in BatchAnalysis** | Sujal | 1h | T5 | "Load Pre-computed Results" button |
| I4C webhook endpoint | Dhiren | 1.5h | T2 | `POST /ingest-i4c` → cross-reference → risk score |
| NL query wired to BOI dataset | Dhiren | 2h | T3 | Natural language → Cypher → account results |
| Geographic risk heatmap | Sujal | 2h | T10 | F3890 map visualization |
| Model comparison table | Vikram | 1h | T12 | XGBoost vs RF vs Isolation Forest metrics |

**P2 total: ~13 hours**

---

## EXECUTION PHASES (dependency order)

```
Phase 0 (parallel, no deps):
  T1 (Vikram) + T13 (Sujal) + BRANDING (Shriraj)

Phase 1 (sequential, needs T1):
  T2 (Vikram/Dhiren)

Phase 2 (parallel, needs T2):
  T3 (Dhiren) + T4 (Sujal) + T5 (Sujal) + T6 (Vikram)

Phase 3 (needs T3+T4):
  T7 (Dhiren) + T8 (Vikram) + T9 (Sujal) + T10 (Sujal) + T11 (Sujal)

Phase 4 (needs T8):
  T12 (Vikram) + T14 (all)

Phase 5 (needs all):
  T15 (all)
```

---

## DAY-BY-DAY SCHEDULE

| Day | AM | PM |
|---|---|---|
| **Day 1** | T1 (artifacts) + T13 (docs) + Branding | T2 (FastAPI ML endpoints) |
| **Day 2** | T3 (score fusion) | T4 (signal card) |
| **Day 3** | T5 + T9 (batch UI + funnel) | T6 + T7 (lifecycle + STR) |
| **Day 4** | T8 + T10 + T11 (analytics) | Backup prep (demo_results.json + demo mode) |
| **Day 5** | T15 (full integration test) | T13 PDF + submission checklist |

---

## COMPLETION GATE (required before June 15 submission)

- P0 tasks: ALL complete
- P1 branding + PPT tasks: ALL complete
- T14 or demo mode fallback: AT LEAST ONE working
- T15: demo runs clean once end-to-end
