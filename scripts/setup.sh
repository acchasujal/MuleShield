#!/bin/bash

# =============================================================================
# MuleShield AI — Linux/macOS Setup Automation Script
# =============================================================================

set -e

# ANSI escape codes for colored output
CYAN='\033[0;36m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${CYAN}🛡️  MuleShield AI Setup Tool${NC}"
echo -e "${CYAN}=============================${NC}"

# 1. Verify Python installation
if command -v python3 &>/dev/null; then
    PYTHON_CMD="python3"
elif command -v python &>/dev/null; then
    PYTHON_CMD="python"
else
    echo -e "${RED}❌ Python is not installed or not in PATH. Please install Python 3.10+ and try again.${NC}"
    exit 1
fi

PYTHON_VERSION=$($PYTHON_CMD --version)
echo -e "${GREEN}✅ Python found: $PYTHON_VERSION${NC}"

# 2. Initialize Virtual Environment
if [ -d "venv" ]; then
    echo -e "${YELLOW}ℹ️  Virtual environment 'venv' already exists. Skipping creation.${NC}"
else
    echo -e "${CYAN}📦 Creating virtual environment 'venv'...${NC}"
    $PYTHON_CMD -m venv venv
    echo -e "${GREEN}✅ Virtual environment created.${NC}"
fi

# 3. Upgrade Pip and Install Dependencies
echo -e "${CYAN}🔌 Installing dependencies from requirements.txt...${NC}"
venv/bin/python -m pip install --upgrade pip
venv/bin/pip install -r requirements.txt
echo -e "${GREEN}✅ Dependencies successfully installed.${NC}"

# 4. Generate Local Environment Configuration
if [ -f ".env" ]; then
    echo -e "${YELLOW}ℹ️  Local configuration '.env' already exists. Skipping creation.${NC}"
else
    if [ -f ".env.example" ]; then
        echo -e "${CYAN}📝 Generating '.env' from example template...${NC}"
        cp .env.example .env
        echo -e "${GREEN}✅ Local '.env' config generated successfully.${NC}"
    else
        echo -e "${YELLOW}⚠️  .env.example template not found. Skipping config generation.${NC}"
    fi
fi

# 5. Run Database Table Migrations
echo -e "${CYAN}🗄️  Running PostgreSQL schema migrations...${NC}"
if venv/bin/python -c "import asyncio; from backend.database import init_db; asyncio.run(init_db())" 2>/dev/null; then
    echo -e "${GREEN}✅ PostgreSQL migrations completed.${NC}"
else
    echo -e "${YELLOW}⚠️  PostgreSQL migration check bypassed (PostgreSQL is likely offline — this is expected if docker composition is not running).${NC}"
fi

# 6. Run System Diagnostics Health Check
echo -e "\n${CYAN}🔍 Running System Diagnostic Health Checks...${NC}"
if [ -f "health_check.py" ]; then
    venv/bin/python health_check.py
else
    echo -e "${YELLOW}⚠️  health_check.py not found. Skipping health check diagnostics.${NC}"
fi

echo -e "\n${GREEN}🛡️  MuleShield AI Setup Completed successfully!${NC}"
echo -e "${GREEN}To start the application:${NC}"
echo -e "${GREEN}1. Startup services: docker compose up -d${NC}"
echo -e "${GREEN}2. Start Backend:    venv/bin/python -m uvicorn backend.app:app --reload${NC}"
echo -e "${GREEN}3. Start Frontend:   venv/bin/streamlit run frontend/app.py${NC}"
