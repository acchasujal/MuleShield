# DESIGN_SYSTEM.md — Visual Language for MuleShield PECHacks Edition

> All decisions here are `[DECISION]` (locked for this build) unless marked `[IDEA]` (optional, cut if time runs short). Chosen direction: **Minimal Enterprise + Soft Glass**, B2B compliance-tool aesthetic — closer to Stripe/Linear/Mercury than consumer fintech apps, because the actual user (bank compliance officer) and the actual judge (technical evaluator) both respond to precision/trust signals over playful/consumer signals.

---

## 1. Color Palette

| Token | Value | Usage |
|---|---|---|
| `bg-primary` | `#0A0B0D` | App background |
| `bg-surface` | `#141519` | Card surfaces |
| `bg-surface-raised` | `#1B1D22` | Hover/elevated cards |
| `text-primary` | `#F5F5F7` | Headings, key numbers |
| `text-muted` | `#8A8F98` | Body, labels |
| `accent` | `#5B5FEF` | Interactive elements only (buttons, links, focus rings) |
| `risk-critical` | `#DC2626` (red-600) | CRITICAL tier |
| `risk-high` | `#F59E0B` (amber-500) | HIGH tier |
| `risk-medium` | `#EAB308` (yellow-400) | MEDIUM tier |
| `risk-low` | `#10B981` (emerald-500) | LOW tier |

Rule: **no color outside this table appears anywhere in the UI.** Charts, badges, and icons all draw from this set only.

## 2. Typography

- Font: **Inter** or **Geist** (both free, CDN-loadable, close to Stripe/Linear's system font feel).
- Headings: weight 600-700, tight letter-spacing (-0.02em), text-primary.
- Body: weight 400, text-muted.
- Large numbers (KPIs, scores): weight 700, tabular-nums, text-primary — this is the single highest-leverage typographic choice for "premium fintech" perception.

## 3. Spacing & Layout

- Base unit: 8px grid.
- Card padding: 24px.
- Section gaps: 32-48px.
- Page max-width: 1280px, centered, generous side margins (min 5% viewport) — whitespace is a trust signal, don't fill every pixel.

## 4. Border Radius

- Cards: 16px.
- Buttons/inputs: 8px.
- Badges/pills: full (9999px).
Consistent across every component — no mixing radii.

## 5. Shadows & Glass

- Standard card shadow: `0 8px 24px rgba(0,0,0,0.24)`, soft, low-opacity.
- Glass effect: reserved for **one** focal element — the composite risk-fusion card — `backdrop-filter: blur(12px)`, semi-transparent surface over a subtle gradient background. Do not apply glass everywhere; it loses meaning if overused.

## 6. Gradients

- Subtle radial glow (accent color, low opacity) behind the landing hero headline.
- Subtle glow behind CRITICAL severity badges only — nowhere else.

## 7. Icons

- One consistent line-icon set: **Lucide** (or Phosphor), 1.5px stroke weight.
- No emoji anywhere in the UI (removes the "🔍 Account Inspector" style from current build).

## 8. Charts

- Single accent color + neutral grays only. No rainbow/multi-hue chart palettes.
- One visualization per metric — remove duplicate charts showing the same number differently.

## 9. Cards

- Standard card: `bg-surface`, 16px radius, 24px padding, soft shadow.
- KPI card: large tabular number (700 weight) + small label (muted) + optional sparkline trend line.
- No more than 4 KPI cards visible at once.

## 10. Buttons

- Primary: solid `accent` fill, white text, 8px radius.
- Secondary: ghost/outline, `text-muted` border, transparent fill.
- Maximum 2 button styles in the entire product.

## 11. Inputs

- Dark surface fill, 8px radius, subtle border (`rgba(255,255,255,0.08)`), accent-colored focus ring.

## 12. Tables

- Avoid raw `st.dataframe` in user-facing flows — wrap key rows in card components instead. Reserve tables for a collapsed "raw data" expander for technical judges who ask to see it.

## 13. Status / Risk Indicators

- Small colored dot + label text, using the 4-tier palette from §1.
- CRITICAL tier gets a subtle pulse animation (see §17); no other tier animates.

## 14. Empty States

- Skeleton shimmer blocks (never a blank white/black screen) while data loads.

## 15. Loading States

- Staged reveal: score assembles in 1-2s rather than dumping instantly — reinforces "AI is working" narrative without adding real latency.

## 16. Hover States

- Cards: 2px lift + shadow increase, 150ms ease-out.
- Buttons: slight brightness increase + 2px lift.

## 17. Motion System

- Duration: 150-250ms, ease-out, for all hover/reveal transitions.
- Card mount: fade + slide up 8px, staggered 50ms per card.
- Composite score: count-up animation from 0 on reveal.
- CRITICAL badge: subtle pulse loop (opacity 0.85→1, 2s cycle).
- **Avoid**: page transitions, 3D effects, particle backgrounds, bounce easing — anything that risks looking gimmicky or breaking live.

## 18. Page Layout / Navigation

- Persistent left rail, 3 items max: Overview / Investigate / Reports.
- No top nav bar clutter — logo + rail only.

## 19. Dashboard Layout

3-zone bento grid:
1. Top KPI strip (4 cards max)
2. Center: primary investigation panel (60% width)
3. Right rail: SHAP explanation card (40% width)

## 20. Component Hierarchy

```
App Shell
├── Left Rail (nav)
└── Content Area
    ├── KPI Strip (top, always visible on Overview)
    ├── Primary Panel (center, context-dependent: fusion score / report / graph)
    └── Secondary Panel (right rail: explanation / details)
```

## 21. Micro-interactions

- Button press: subtle scale-down (0.98) on click.
- Card hover: lift only, no color change.
- Score reveal: number count-up + accompanying bar/gauge fill in sync.

## 22. Screen-by-Screen Notes

- **Landing**: static, 4-section single scroll (hero / problem stats / how-it-works / trust footer). Build separately in React/Tailwind — see BUILD_GUIDE.md §Constraints.
- **Overview**: KPI strip + composite gauge, minimal, glanceable in under 3 seconds.
- **Investigate**: single upload action, animated fusion reveal, SHAP card same screen — no page jump.
- **Reports**: goAML XML card styled as a "document" (letterhead feel) + evidence hash + secondary graph-explore tab with cached fallback visualization.

## 23. `[IDEA]` — optional if time remains

- Risk heatmap mini-widget on Overview.
- Interactive fraud-journey timeline scrubber.
Cut both first if the 48-hour roadmap slips.
