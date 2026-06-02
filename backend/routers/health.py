"""
MuleShield AI — Health and System Status Router
"""

from fastapi import APIRouter
from backend.ai_service import nvidia_client, gemini_client

router = APIRouter(prefix="", tags=["System"])


@router.get("/")
async def root():
    """Welcome and API metadata gateway."""
    return {
        "title": "MuleShield AI API Gateway",
        "status": "active",
        "version": "3.0",
        "endpoints": {
            "health": "/health",
            "docs": "/docs"
        }
    }


@router.get("/health")
async def health():
    """Liveness probe — shows AI provider readiness."""
    return {
        "status":  "ok",
        "version": "3.0",
        "nvidia":  "ready" if nvidia_client else "disabled",
        "gemini":  "ready" if gemini_client else "disabled",
    }
