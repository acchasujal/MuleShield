# 07_DEMO_GUIDE.md — MuleShield AI: Demo & Presentation Guide

This guide describes how to run a live demonstration of the MuleShield AI financial trust infrastructure.

---

## 1. Setup & Checks

1. Start the FastAPI backend server and Vite React frontend workspace.
2. Confirm the browser is opened to the Cases list: `http://localhost:5173/cases`.
3. Press **`Ctrl+K`** to open the Command Palette. Press `R` to reset all presentation states.
4. Verify "Demo Mode Active" is visible in the sidebar footer (indicating offline fallback dataset is loaded and ready).

---

## 2. Step-by-Step Demo Script

### Step 1: The Trust Dashboard (Time: 0 - 30s)
- **Action**: Show the Cases queue inbox.
- **Narrative**: *"Welcome. MuleShield AI is an AI-Native Financial Trust Infrastructure designed for the next billion users. Today, we are demonstrating our first flagship capability: Money Mule Intelligence. When a victim falls prey to a cyber fraud scam, banks face a critical 4-to-72 hour gap before manual AML teams can suspend the target accounts. MuleShield continuously understands transaction behaviors and constructs this prioritized trust-alert queue."*

### Step 2: Risk Fusion Engine (Time: 30 - 60s)
- **Action**: Click "Open case workspace" on the critical case `ACC05200000000028` (Ananya Rao).
- **Narrative**: *"As we enter this workspace, the system runs risk fusion. Observe the score compile in real time: Profile behavior (40%), Transaction heuristics (40%), and Graph network topology (20%). The score reaches 86, classifying this case as CRITICAL."*

### Step 3: Explainable Trust attributions (Time: 60 - 90s)
- **Action**: Hover over the SHAP signals in the brief panel ("Dormant reactivation" and "Velocity spike"). Note the corresponding contributor bars highlight in response.
- **Narrative**: *"Black-box models are operational liabilities. MuleShield translates mathematical attributions into plain-English. Hovering over 'Dormant reactivation' connects the signal back to Profile behavior, while 'Velocity spike' connects to Transaction behavior."*

### Step 4: Cryptographic Handoff (Time: 90 - 120s)
- **Action**: Click "Prepare Evidence" in the top header. Wait for the loading cycle to complete.
- **Narrative**: *"We seal the evidence package with a SHA-256 integrity hash for legal admissibility under Section 65B of the Indian Evidence Act, and auto-generate a goAML report. What previously took 8 hours of manual analysis now compiles in 8 seconds. This prototype is our stepping stone to a multi-bank federated trust infrastructure."*
