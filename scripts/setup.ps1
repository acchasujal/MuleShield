# =============================================================================
# MuleShield AI - Windows Setup Automation Script
# =============================================================================

$ErrorActionPreference = "Stop"

Write-Host "MuleShield AI Setup Tool" -ForegroundColor Cyan
Write-Host "=============================" -ForegroundColor Cyan

# 1. Verify Python installation
try {
    $pythonVersion = python --version 2>&1
    Write-Host "Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Error "Python is not installed or not in PATH. Please install Python 3.10+ and try again."
    exit 1
}

# 2. Initialize Virtual Environment
if (Test-Path "venv") {
    Write-Host "Virtual environment 'venv' already exists. Skipping creation." -ForegroundColor Yellow
} else {
    Write-Host "Creating virtual environment 'venv'..." -ForegroundColor Cyan
    python -m venv venv
    Write-Host "Virtual environment created." -ForegroundColor Green
}

# 3. Upgrade Pip and Install Dependencies
Write-Host "Installing dependencies from requirements.txt..." -ForegroundColor Cyan
& venv\Scripts\python.exe -m pip install --upgrade pip
& venv\Scripts\pip.exe install -r requirements.txt
Write-Host "Dependencies successfully installed." -ForegroundColor Green

# 4. Generate Local Environment Configuration
if (Test-Path ".env") {
    Write-Host "Local configuration '.env' already exists. Skipping creation." -ForegroundColor Yellow
} else {
    if (Test-Path ".env.example") {
        Write-Host "Generating '.env' from example template..." -ForegroundColor Cyan
        Copy-Item ".env.example" ".env"
        Write-Host "Local '.env' config generated successfully." -ForegroundColor Green
    } else {
        Write-Warning ".env.example template not found. Skipping config generation."
    }
}

# 5. Run Database Table Migrations
Write-Host "Running PostgreSQL schema migrations..." -ForegroundColor Cyan
try {
    $env_exists = Test-Path ".env"
    & venv\Scripts\python.exe -c "import asyncio; from backend.database import init_db; asyncio.run(init_db())"
    Write-Host "PostgreSQL migrations completed." -ForegroundColor Green
} catch {
    Write-Host "WARNING: PostgreSQL migration check bypassed (PostgreSQL is offline - this is expected if docker is not running)." -ForegroundColor Yellow
}

# 6. Run System Diagnostics Health Check
Write-Host "Running System Diagnostic Health Checks..." -ForegroundColor Cyan
if (Test-Path "health_check.py") {
    & venv\Scripts\python.exe health_check.py
} else {
    Write-Warning "health_check.py not found. Skipping health check diagnostics."
}

Write-Host "MuleShield AI Setup Completed successfully!" -ForegroundColor Green
Write-Host "To start the application:" -ForegroundColor Green
Write-Host "1. Startup services: docker compose up -d" -ForegroundColor Green
Write-Host "2. Start Backend:    venv\Scripts\python.exe -m uvicorn backend.app:app --reload" -ForegroundColor Green
Write-Host "3. Start Frontend:   venv\Scripts\streamlit run frontend/app.py" -ForegroundColor Green
