# MuleShield AI — Consolidated Changelog & History

This changelog outlines the key releases, features, visual redesigns, and bug fixes during the development of MuleShield AI.

---

## [1.1.0] — Final Polish (Current Release)

### Added
- Created `formatAccount` utility to mask account IDs into readable `BOI •••• 0028` values, with hover overlays.
- Replaced horizontal static timeline with dynamic investigation events timeline detailing transaction and network triggers.
- Re-styled scenario selection controls to behave as a single segmented pill control.

### Improved
- Standardized Card components padding to 24px and Unified border radius definitions.
- Refactored Case Queue lists to display as a professional inbox layout.
- Added high-contrast background highlights for network graph nodes to improve readability.

---

## [1.0.0] — Modular Restructure

### Added
- Split monolithic 815-line `App.tsx` file into dedicated routing files, contexts, page layouts, components, utilities, and services.
- Created `AppContext.tsx` to handle shared states (cases, selections, and mock connectivity) without prop drilling.
- Designed Raycast-style command palette overlay with full keyboard controls (`ArrowUp`, `ArrowDown`, `Enter`, `Esc`, `1-4`, letter shortcuts).
- Replaced CSS-only edge borders in graph visualizations with SVG lines.
- Extracted raw styles into modular sheets (`tokens.css`, `base.css`, `layout.css`, `typography.css`, `components.css`, `pages.css`).
