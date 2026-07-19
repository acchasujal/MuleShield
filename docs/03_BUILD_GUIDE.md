# 03_BUILD_GUIDE.md — MuleShield AI: Build & Deployment Guide

This document specifies the setup, build steps, and environment configuration required to deploy the MuleShield AI financial trust infrastructure locally.

---

## 1. System Requirements

- **Docker & Docker Compose**: Required to spin up the local graph database (Neo4j) and the database audit logger (PostgreSQL).
- **Node.js (v18+) & npm**: Required to build and run the React workspace.
- **Python (v3.10+)**: Required for running the FastAPI backend gateway and explainable ML scoring modules.

---

## 2. Repository Directory Structure

- `/backend`: FastAPI service layers, database ORM connectors, Neo4j graph connectors, and prediction modules.
- `/frontend-react`: Vite + React + TypeScript workspace containing the Investigator Workspace interface.
- `/docs`: Consolidated 12-file numbered documentation tree.

---

## 3. Environment Variables

Create a `.env` file in the project root:
```ini
# FastAPI Backend
PORT=8000
VITE_API_URL=http://localhost:8000

# PostgreSQL Configuration
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=muleshield
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

# Neo4j Configuration
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=password
```

---

## 4. Setup & Ingestion

### Step 1: Start Database Containers
```bash
docker-compose up -d
```
This spawns:
- PostgreSQL on port `5432`
- Neo4j on port `7474` (HTTP interface) and `7687` (Bolt interface)

### Step 2: Initialize FastAPI Backend
1. From the project root, activate your virtual environment:
   ```bash
   # Windows Command Prompt
   call venv\Scripts\activate
   # Windows PowerShell
   .\venv\Scripts\Activate.ps1
   # macOS/Linux
   source venv/bin/activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the API server:
   ```bash
   # Windows Command Prompt
   set PYTHONPATH=.
   uvicorn backend.app:app --reload --port 8000
   # Windows PowerShell
   $env:PYTHONPATH="."
   uvicorn backend.app:app --reload --port 8000
   # macOS/Linux
   export PYTHONPATH=.
   uvicorn backend.app:app --reload --port 8000
   ```
   * Swagger docs are live at `http://localhost:8000/docs`.

### Step 3: Run React Workspace
1. Navigate to `/frontend-react`:
   ```bash
   npm install
   ```
2. Start the local dev server:
   ```bash
   npm run dev
   ```
   Open `http://localhost:5173/` in your browser to access the Investigator Workspace.
