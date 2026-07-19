# MuleShield AI — Project Context

## 1. Executive Summary

**MuleShield AI** is a dual-engine (tabular ML + graph analytics) money-mule detection platform built for financial institutions. Positioned as **"the compliance officer's autopilot,"** MuleShield catches mule accounts before funds are flushed and auto-generates a regulator-ready evidence package with cryptographic integrity sealing.

- **Tagline**: *"See the mule before the money moves."*
- **Positioning**: High-fidelity infrastructure that merges profile analysis, transaction heuristics, and network topology to generate defensible, explainable compliance handoffs.

---

## 2. The Problem & Solution Space

### The Problem
India's digital payment rails (e.g. UPI) are heavily exploited by organized networks utilizing money-mule accounts—often recruited from vulnerable populations. Traditional rules-based systems lack network awareness, generate massive volumes of false positives, and fail to provide explainability, leaving compliance teams overwhelmed by manual review backlogs.

### The Solution
MuleShield introduces a **Composite Risk Fusion Engine** that computes a unified risk score across three distinct dimensions:
```
Composite Risk = (Profile Risk × 0.40) + (Transaction Risk × 0.40) + (Graph Risk × 0.20)
```
- **Profile Risk (40%)**: XGBoost ML model analyzing 122 profile variables with SHAP-based feature attribution.
- **Transaction Risk (40%)**: Heuristics tracking layering, circular loops, payment channel switching, and velocity spikes.
- **Graph Risk (20%)**: Graph analytics (degree centrality and page rank) mapping connections to known shell accounts and crypto/cash-out hubs.

---

## 3. Product Differentiators

1. **Compliance-Ready Handoffs**: Auto-generates goAML XML reports and computes SHA-256 evidence hashes designed to satisfy Section 65B of the Indian Evidence Act.
2. **Explainable AI (XAI)**: Mapped SHAP feature attributions tell analysts exactly *why* a profile was flagged, converting complex model weights into plain-English narratives.
3. **Mule Lifecycle Stages**: Tracks accounts as they progress through dynamic lifecycle phases (`DORMANT` → `ACTIVATION` → `NEWLY_RECRUITED` → `ACTIVE_MULE` → `BEING_FLUSHED`) rather than using static threat scores.
4. **Resilient Offline Architecture**: Features dynamic mock fallback modes that degrade gracefully when Neo4j or external APIs are disconnected.

---

## 4. Technology Stack

- **Backend**: FastAPI, Python (XGBoost, SHAP)
- **Frontend**: React (Vite, TypeScript, TailwindCSS/Vanilla CSS)
- **Database/Graph**: Neo4j Graph Database, PostgreSQL
- **Infrastructure**: Docker Compose for local deployment
