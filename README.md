# 🛡️ MuleShield AI

> **Coordinated Mule Account Containment & Regulatory Autopilot Infrastructure**  
> Dual-engine money-mule detection platform co-developed by **Bank of India** and **IIT Hyderabad** for **PEC Hacks 4.0 (PS-2)**.

---

## 1. Project Vision

India loses ₹66 million daily to cyber fraud, with **66% of stolen funds routed through mule accounts**. 

MuleShield AI bridges the critical **4-to-72 hour gap** between a victim filing a complaint (e.g. via the MHA I4C portal) and a bank investigator freezing the target account. By fusing tabular ML, heuristic transaction rules, and topological graph analytics, MuleShield evaluates alerts and suspends accounts within **4 seconds** of complaint ingestion—protecting Mrs. Sharma's savings *before* the fraudster's automated dispersal script completes.

> **MuleShield AI is not a fraud detector. It is India's missing mule containment infrastructure.**

---

## 2. Technology Stack

- **ML Prediction**: Python, XGBoost Classifier, SHAP TreeExplainer
- **Graph Topology**: Neo4j Graph Database (GDS), NetworkX Heuristic Analyzers
- **Backend API**: FastAPI Gateway
- **Frontend Workspace**: Vite, React, TypeScript, Framer Motion
- **Audit Database**: PostgreSQL, SQLAlchemy ORM
- **Infrastructure**: Docker Compose, local and on-premise configurations

---

## 3. Repository Directory Structure

```
Muleshield/
├── backend/            # FastAPI gateways, ML engines, and XML auto-STR compilers
├── frontend-react/     # React web UI workspace (Vite, TypeScript, CSS Tokens)
├── docs/               # Consolidated 12-file numbered documentation tree
│   ├── 01_PROJECT_CONTEXT.md
│   ├── 02_ARCHITECTURE.md
│   ├── 03_BUILD_GUIDE.md
│   ...
├── docker-compose.yml  # PostgreSQL and Neo4j database containers
└── README.md           # Main project entry point (This file)
```

---

## 4. Documentation Index

For detailed guidelines, configurations, and scripts, refer to the numbered documentation in `/docs`:

1. **[01_PROJECT_CONTEXT.md](file:///d:/Projects/Muleshield/docs/01_PROJECT_CONTEXT.md)**: Problem statement, target personas, and differentiators.
2. **[02_ARCHITECTURE.md](file:///d:/Projects/Muleshield/docs/02_ARCHITECTURE.md)**: Score fusion formulas, system blueprints, API schemas, and Postgres ORM mappings.
3. **[03_BUILD_GUIDE.md](file:///d:/Projects/Muleshield/docs/03_BUILD_GUIDE.md)**: Setup variables, pip install steps, and database container commands.
4. **[04_UI_UX_GUIDE.md](file:///d:/Projects/Muleshield/docs/04_UI_UX_GUIDE.md)**: Navigation layouts, bento grids, and screen-by-screen page designs.
5. **[05_DESIGN_SYSTEM.md](file:///d:/Projects/Muleshield/docs/05_DESIGN_SYSTEM.md)**: Typography parameters, CSS HSL design tokens, and radius scales.
6. **[06_IMPLEMENTATION.md](file:///d:/Projects/Muleshield/docs/06_IMPLEMENTATION.md)**: AppContext states, file listings, and custom hooks details.
7. **[07_DEMO_GUIDE.md](file:///d:/Projects/Muleshield/docs/07_DEMO_GUIDE.md)**: Guided scenario pitch scripts and presentation timings.
8. **[08_DATASET.md](file:///d:/Projects/Muleshield/docs/08_DATASET.md)**: Connected money-laundering network topology.
9. **[09_PRESENTATION.md](file:///d:/Projects/Muleshield/docs/09_PRESENTATION.md)**: Competitive advantages and pitch deck presentation structures.
10. **[10_AI_CONTEXT.md](file:///d:/Projects/Muleshield/docs/10_AI_CONTEXT.md)**: Mapped SHAP indicators and ML feature index maps.
11. **[11_CHANGELOG.md](file:///d:/Projects/Muleshield/docs/11_CHANGELOG.md)**: Historical release notes and improvements.
12. **[12_FINAL_POLISH_REPORT.md](file:///d:/Projects/Muleshield/docs/12_FINAL_POLISH_REPORT.md)**: Polishing audits and readiness scores.

---

## 5. Setup & Ingestion

Ensure Docker Desktop, Node.js (v18+), and Python (v3.10+) are installed.

### Step 1: Start Databases
```bash
docker-compose up -d
```

### Step 2: Run FastAPI Backend
1. Go to `/backend` and install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Start the API server:
   ```bash
   uvicorn app:app --reload --port 8000
   ```
   * Swagger Documentation is live at `http://localhost:8000/docs`.

### Step 3: Run React Web Workspace
1. Go to `/frontend-react` and install node packages:
   ```bash
   npm install
   ```
2. Run the developer build:
   ```bash
   npm run dev
   ```
   * Access the UI workspace at `http://localhost:5173/`.
