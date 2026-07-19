# MuleShield AI — Build & Deployment Guide

This document specifies the setup, build steps, and environment configuration required to run the MuleShield AI platform locally.

---

## 1. System Requirements

- **Docker & Docker Compose**: Required for running graph database (Neo4j) and Postgres.
- **Node.js (v18+) & npm**: Required to build and run the React frontend workspace.
- **Python (v3.10+)**: Required for running the FastAPI backend server and ML training models.

---

## 2. Directory Structure

- `/backend`: FastAPI gateway, database ORM connectors, Neo4j graph connectors, and prediction modules.
- `/frontend-react`: Vite + React + TypeScript workspace.
- `/docs`: Structured project specification documents.

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

### Step 1: Start Databases
```bash
docker-compose up -d
```
This spawns:
- PostgreSQL on port `5432`
- Neo4j on port `7474` (HTTP) and `7687` (Bolt)

### Step 2: Initialize Backend
1. Navigate to `/backend`:
   ```bash
   pip install -r requirements.txt
   ```
2. Start the FastAPI gateway server:
   ```bash
   uvicorn app:app --reload --port 8000
   ```

### Step 3: Run React Workspace
1. Navigate to `/frontend-react`:
   ```bash
   npm install
   ```
2. Start the local dev server:
   ```bash
   npm run dev
   ```
   Open `http://localhost:5173/` in your browser.
