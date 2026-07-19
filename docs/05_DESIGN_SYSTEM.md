# MuleShield AI — Design System Specification

## 1. Visual Language & Philosophy

The MuleShield AI interface is designed with a **Minimal Enterprise + Soft Glass** aesthetic. Reserved for professional compliance environments, it utilizes dark-mode-first interfaces, crisp high-contrast layout bounds, and reserved accent highlights.

---

## 2. Design Tokens

### Color Tokens (mapped to HSL in styles)
- **Background (`bg-primary`)**: `#0A0B0D`
- **Surface (`bg-surface`)**: `#141519`
- **Raised Surface (`bg-surface-raised`)**: `#1B1D22`
- **Border (`color-border`)**: `rgba(255, 255, 255, 0.08)`
- **Accent Highlight (`accent`)**: `#5B5FEF`

### Severity Colors
- **Critical**: `#ef4444` (Red)
- **High**: `#f97316` (Orange)
- **Medium**: `#eab308` (Yellow)
- **Low**: `#10b981` (Green)

---

## 3. Component styling rules

1. **Segmented Controls**: Switched from separated buttons to wrapper segment bars (`.scenario-switcher`) with background pills for selected values.
2. **Case Inbox**: Rows stacked inside a unified border box (`.case-list`) with thin dividing lines.
3. **Card Padding**: Standardized card paddings to `var(--space-6)` (24px) for perfect grid alignment.
4. **Focus Rings**: Accessible `:focus-visible` ring outlines using `var(--color-accent)`.
