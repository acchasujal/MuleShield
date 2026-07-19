# MuleShield AI — Demo & Presentation Guide

This guide describes how to run a flawless live demonstration of the MuleShield AI platform.

---

## 1. Setup & Checks

1. Start the backend server and Vite React frontend.
2. Confirm the browser is opened to the Cases list: `http://localhost:5173/cases`.
3. Press **`Ctrl+K`** to open the Command Palette. Type `Reset` or press `R` to ensure all presentation states are normalized.
4. Verify "Demo Mode Active" is visible in the sidebar footer (indicating offline fallback is active and ready).

---

## 2. Step-by-Step Demo Script

### Step 1: The Queue overview (Time: 0 - 30s)
- **Action**: Show the Cases landing queue.
- **Narrative**: *"Good morning. When Mrs. Sharma falls victim to a fake investment scam, her bank has only a narrow window to freeze the funds before they leave the banking system. MuleShield AI automatically ingests transactions and populates this priority cases queue."*
- **Action**: Highlight the StatCards (e.g. "Critical cases: 1").

### Step 2: Ingest & Risk Fusion (Time: 30 - 60s)
- **Action**: Click "Open case workspace" on the critical case `ACC05200000000028` (Ananya Rao).
- **Narrative**: *"As we enter the workspace, the system automatically runs risk fusion. Watch the score compile: Profile behavior (40%), Transaction rules (40%), and Network context (20%). The score reaches 86, classifying this case as CRITICAL."*

### Step 3: Plain-English Explainability (Time: 60 - 90s)
- **Action**: Hover over the SHAP signals in the brief panel ("Dormant reactivation" and "Velocity spike"). Note the corresponding contributor bars highlight in response.
- **Narrative**: *"MuleShield translates complex mathematical attributions into human-readable flags. Hovering over 'Dormant reactivation' shows it contributed to Profile behavior; 'Velocity spike' connects to Transaction behavior."*

### Step 4: The Sealed Court Handoff (Time: 90 - 120s)
- **Action**: Click "Prepare Evidence" in the top header. Wait for the loading cycle to complete.
- **Narrative**: *"With one click, we compile the evidence. The system seals the package with a SHA-256 integrity hash for court admissibility and auto-generates a goAML report. We click 'Export XML' and the regulator-ready document is ready to download."*
