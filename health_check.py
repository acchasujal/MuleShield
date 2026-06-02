# =============================================================================
# MuleShield AI — System Diagnostic Health Check
# =============================================================================

import os
import sys
import socket
import logging
from dotenv import load_dotenv

# Suppress verbose loggers
logging.getLogger("muleshield").setLevel(logging.ERROR)

load_dotenv()

# ANSI escape codes for coloring terminal output
COLOR_GREEN = "\033[92m"
COLOR_YELLOW = "\033[93m"
COLOR_RED = "\033[91m"
COLOR_RESET = "\033[0m"

def print_result(label: str, status: str, message: str = ""):
    if status == "PASS":
        color = COLOR_GREEN
    elif status == "WARNING":
        color = COLOR_YELLOW
    else:
        color = COLOR_RED
    
    msg_str = f" - {message}" if message else ""
    print(f"[{color}{status:<7}{COLOR_RESET}] {label}{msg_str}")

def check_port(host: str, port: int, timeout: float = 1.0) -> bool:
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except Exception:
        return False

def run_health_check() -> int:
    has_failed = False
    has_warnings = False
    
    print("==================================================")
    print("MULESHIELD AI — HEALTH DIAGNOSTIC CHECK")
    print("==================================================")
    
    # 1. Check Required Directories
    required_dirs = ["backend", "frontend", "data", "lib"]
    dirs_missing = [d for d in required_dirs if not os.path.isdir(d)]
    if not dirs_missing:
        print_result("Required Directories", "PASS", "All directories exist.")
    else:
        print_result("Required Directories", "FAIL", f"Missing: {', '.join(dirs_missing)}")
        has_failed = True
        
    # 2. Check ML Model Artifacts
    ml_dir = "backend/ml_artifacts"
    artifacts = ["final_model.pkl", "imputer_full.pkl", "final_metadata.json", "cat_mappings.json", "feature_importances.csv"]
    missing_artifacts = [a for a in artifacts if not os.path.exists(os.path.join(ml_dir, a))]
    if not os.path.isdir(ml_dir):
        print_result("ML Model Artifacts", "FAIL", f"Directory {ml_dir} does not exist.")
        has_failed = True
    elif not missing_artifacts:
        print_result("ML Model Artifacts", "PASS", "All ML artifacts loaded.")
    else:
        print_result("ML Model Artifacts", "FAIL", f"Missing artifacts: {', '.join(missing_artifacts)}")
        has_failed = True

    # 3. Check DataSet.csv
    dataset_path = "data/boi/DataSet.csv"
    if os.path.exists(dataset_path):
        size_mb = os.path.getsize(dataset_path) / (1024 * 1024)
        print_result("DataSet.csv alert coordinates", "PASS", f"DataSet.csv found ({size_mb:.2f} MB).")
    else:
        print_result("DataSet.csv alert coordinates", "WARNING", f"Missing DataSet.csv at {dataset_path}. Account Inspector details page will revert to sandbox mode.")
        has_warnings = True

    # 4. Check Backend Imports
    try:
        # Check if we can import the FastAPI gateway
        sys.path.insert(0, ".")
        import backend.app # noqa: F401
        print_result("Python API Imports", "PASS", "Backend modules compiled successfully.")
    except Exception as exc:
        print_result("Python API Imports", "FAIL", f"Import failure: {exc}")
        has_failed = True

    # 5. Check PostgreSQL Connectivity
    pg_host = os.getenv("POSTGRES_HOST", "localhost")
    try:
        pg_port = int(os.getenv("POSTGRES_PORT", "5432"))
    except ValueError:
        pg_port = 5432
        
    if check_port(pg_host, pg_port):
        # Port is open, try actual import and connection check
        try:
            import asyncio
            from sqlalchemy.ext.asyncio import create_async_engine
            pg_user = os.getenv("POSTGRES_USER", "postgres")
            pg_pass = os.getenv("POSTGRES_PASSWORD", "postgres")
            pg_db = os.getenv("POSTGRES_DB", "muleshield")
            db_url = f"postgresql+asyncpg://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}"
            engine = create_async_engine(db_url)
            
            async def test_conn():
                async with engine.connect() as conn:
                    await conn.execute("SELECT 1")
            
            asyncio.run(test_conn())
            print_result("PostgreSQL Database", "PASS", f"Connected to postgres@{pg_host}:{pg_port}/{pg_db}.")
        except Exception as exc:
            print_result("PostgreSQL Database", "WARNING", f"Port {pg_port} is open, but connection handshake failed: {exc}.")
            has_warnings = True
    else:
        print_result("PostgreSQL Database", "WARNING", f"Connection refused at {pg_host}:{pg_port}. Offline audit logs active.")
        has_warnings = True

    # 6. Check Neo4j Connectivity
    # Parse neo4j host and port from NEO4J_URI (e.g. bolt://localhost:7687)
    neo_uri = os.getenv("NEO4J_URI", os.getenv("NEO4J_URL", "bolt://localhost:7687"))
    neo_host = "localhost"
    neo_port = 7687
    if "://" in neo_uri:
        host_port = neo_uri.split("://")[1]
        if ":" in host_port:
            neo_host, port_str = host_port.split(":")
            try:
                neo_port = int(port_str)
            except ValueError:
                pass
        else:
            neo_host = host_port
            
    if check_port(neo_host, neo_port):
        try:
            from neo4j import GraphDatabase
            neo_user = os.getenv("NEO4J_USER", "neo4j")
            neo_pass = os.getenv("NEO4J_PASSWORD", "password")
            with GraphDatabase.driver(neo_uri, auth=(neo_user, neo_pass)) as driver:
                driver.verify_connectivity()
            print_result("Neo4j Graph Database", "PASS", f"Connected to {neo_uri}.")
        except Exception as exc:
            print_result("Neo4j Graph Database", "WARNING", f"Port {neo_port} is open, but auth verification failed: {exc}.")
            has_warnings = True
    else:
        print_result("Neo4j Graph Database", "WARNING", f"Connection refused at {neo_host}:{neo_port}. Standalone ML mode active.")
        has_warnings = True

    print("==================================================")
    if has_failed:
        print(f"{COLOR_RED}HEALTH CHECK STATUS: FAIL{COLOR_RESET}")
        print("Please resolve the failures before starting MuleShield.")
        return 1
    elif has_warnings:
        print(f"{COLOR_YELLOW}HEALTH CHECK STATUS: WARNING{COLOR_RESET}")
        print("Application is fully functional in fallback/standalone mode.")
        return 0
    else:
        print(f"{COLOR_GREEN}HEALTH CHECK STATUS: PASS{COLOR_RESET}")
        print("MuleShield AI is ready for production deployment.")
        return 0

if __name__ == "__main__":
    sys.exit(run_health_check())
