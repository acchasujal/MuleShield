# 01_PROJECT_CONTEXT.md — MuleShield AI: Project Context & Strategy

## 1. Executive Summary

**MuleShield AI** is an **AI-Native Financial Trust Infrastructure for the Next Billion Users**. It transforms raw financial behavior into explainable trust intelligence, enabling banks and payment networks to build trust at scale in digital finance.

- **Tagline**: *"Infrastructure for Trust at Scale in Digital Finance"*
- **Core Positioning**: Rather than acting as a static fraud detector or standard compliance dashboard, MuleShield AI provides the trust layer for high-volume digital financial networks. The first flagship capability demonstrating this infrastructure is **Money Mule Intelligence**.

---

## 2. The Prototype vs. Platform vs. Vision Matrix

To inspire trust and demonstrate clear technical execution, MuleShield AI maintains a strict division between current capabilities, near-term platform expansions, and long-term ecosystem vision:

### 1. Prototype (Current State: Money Mule Intelligence)
*Our implementation demonstrates immediate execution and builds technical credibility.*
- **Dual-Engine Risk Fusion**: Real-time 40/40/20 composite risk scoring combining tabular XGBoost ML probabilities, transaction rule heuristics, and Neo4j graph centrality metrics.
- **Explainable AI (XAI)**: Mapped SHAP feature attributions translating complex model weights into plain-English reasoning.
- **Mule Lifecycle Staging**: Classifies accounts into dynamic threat stages (`DORMANT` → `ACTIVATION` → `NEWLY_RECRUITED` → `ACTIVE_MULE` → `BEING_FLUSHED`).
- **Cryptographic Autopilot**: Automatic compilation of goAML-compliant XML compliance reports sealed with SHA-256 evidence hashes for Indian Evidence Act Section 65B compliance.

### 2. Platform (Near-term: Explainable Financial Trust Intelligence)
*Programmatic APIs and tools to scale integration across a bank's operations.*
- **Trust APIs**: Real-time programmatic trust-signal access for core banking systems (CBS).
- **Merchant Trust Intelligence**: Custom heuristics and models tracking business account layering, merchant loop routing, and settlement anomalies.
- **Lending Trust Intelligence**: Pre-disbursement trust scoring to verify loan application authenticity.

### 3. Vision (Long-term: AI-Native Financial Trust Infrastructure)
*Our strategic direction to protect the next billion users.*
- **Cross-Bank Trust Federation**: Federated, privacy-preserving shared risk networks using differential privacy.
- **Federated Trust Learning**: Training behavioral threat models across multiple participating institutions without centralizing raw transaction graphs.
- **Regulator Integration**: Direct real-time feedback loops between banking evidence generators and regulatory portals (FIU-IND/RBI).

---

## 3. Core Differentiators

1. **Category Creator**: Moves beyond isolated "fraud detection" to build **Financial Trust Infrastructure** that continuously understands financial behavior, assists investigator workflows, and generates regulatory evidence.
2. **Explainability Over Black Boxes**: Mapped SHAP attributions convert model feature weights into transparent, defensible, plain-English narratives.
3. **Resilient Offline Architecture**: Features dynamic mock fallback modes that degrade gracefully when Neo4j or external APIs are disconnected.
4. **Regulatory-Native Design**: goAML XML generation and SHA-256 evidence hashing are core architectural constraints, not cosmetic add-ons.
