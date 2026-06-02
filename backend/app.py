"""
MuleShield AI — FastAPI Backend Gateway
App configuration, lifespan, and router aggregation.
"""

import logging
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Initialize environment variables
load_dotenv()

# Logger setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("muleshield")

# Internal Service imports
from backend.ml_service import MLService
from backend.graph_service import Neo4jService
from backend.database import init_db

# Router imports
from backend.routers.ml_predict import router as ml_predict_router
from backend.routers.i4c_webhook import router as i4c_webhook_router
from backend.routers.analyze import router as analyze_router
from backend.routers.ai_chat import router as ai_chat_router
from backend.routers.health import router as health_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Initializing MuleShield ML Service...")
    ml_service = MLService()
    app.state.ml_service = ml_service

    logger.info("Initializing MuleShield Graph Database Service...")
    graph_service = Neo4jService()
    app.state.graph_service = graph_service

    # PostgreSQL Database Pool Initialization & Migrations
    await init_db()

    yield

    logger.info("Shutting down MuleShield Services...")
    graph_service.close()
    logger.info("MuleShield Services shutdown complete.")


app = FastAPI(title="MuleShield-AI", version="3.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501", "http://127.0.0.1:8501"],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# Route registrations
app.include_router(health_router)
app.include_router(analyze_router)
app.include_router(ai_chat_router)
app.include_router(ml_predict_router)
app.include_router(i4c_webhook_router)
