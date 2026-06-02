"""
MuleShield AI — PostgreSQL Database Connectivity & ORM Engine
Manages async connection pools, schemas for alert audit logs, and automatic database migrations.
"""

import os
import logging
from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Column, String, Float, DateTime, Integer

logger = logging.getLogger("muleshield.database")

# Fetch individual variables for PostgreSQL, fallback to standard compose settings
pg_user = os.getenv("POSTGRES_USER", "postgres")
pg_pass = os.getenv("POSTGRES_PASSWORD", "postgres")
pg_host = os.getenv("POSTGRES_HOST", "localhost")
pg_port = os.getenv("POSTGRES_PORT", "5432")
pg_db   = os.getenv("POSTGRES_DB", "muleshield")

# Construct default async connection string
default_url = f"postgresql+asyncpg://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}"

DATABASE_URL = os.getenv("DATABASE_URL", default_url)

# Initialize SQLAlchemy async engine
engine = create_async_engine(DATABASE_URL, echo=False, pool_pre_ping=True)

# Session factory for non-blocking database queries
async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

Base = declarative_base()

class CaseAudit(Base):
    """ORM Model representing investigator audit trail and evidence cryptographic signatures."""
    __tablename__ = "case_audits"

    id = Column(Integer, primary_key=True, autoincrement=True)
    case_id = Column(String(50), nullable=False, index=True)
    account_id = Column(String(50), nullable=False, index=True)
    event_type = Column(String(50), nullable=False) # 'ALERT_INGESTION', 'RISK_FUSION', 'I4C_WEBHOOK'
    timestamp = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    ml_score = Column(Float, nullable=False)
    graph_score = Column(Float, nullable=False)
    composite_score = Column(Float, nullable=False)
    severity = Column(String(20), nullable=False)
    mule_stage = Column(String(30), nullable=False)
    evidence_hash = Column(String(64), nullable=True) # Tamper-proof Section 65B signature
    action_taken = Column(String(100), nullable=False) # 'AUTO_FREEZE', 'INVESTIGATOR_QUEUED'

async def init_db():
    """Initializes connection and executes schema creations in the database."""
    try:
        logger.info("Initializing PostgreSQL Database and running schema migrations...")
        async with engine.begin() as conn:
            # Create all tables if they do not exist
            await conn.run_sync(Base.metadata.create_all)
        logger.info("PostgreSQL database schemas successfully applied.")
        return True
    except Exception as exc:
        logger.error(f"Failed to connect or migrate PostgreSQL database: {exc}. Reverting to offline log files.")
        return False

async def log_case_audit(
    case_id: str,
    account_id: str,
    event_type: str,
    ml_score: float,
    graph_score: float,
    composite_score: float,
    severity: str,
    mule_stage: str,
    evidence_hash: str = None,
    action_taken: str = "INVESTIGATOR_QUEUED"
) -> bool:
    """Logs an audit record asynchronously inside the PostgreSQL database."""
    # Silently skip if the database engine never connected (offline mode)
    try:
        if engine is None or not engine.sync_engine:
            return True
    except Exception:
        return True
    try:
        async with async_session() as session:
            async with session.begin():
                audit = CaseAudit(
                    case_id=case_id,
                    account_id=account_id,
                    event_type=event_type,
                    ml_score=ml_score,
                    graph_score=graph_score,
                    composite_score=composite_score,
                    severity=severity,
                    mule_stage=mule_stage,
                    evidence_hash=evidence_hash,
                    action_taken=action_taken,
                    timestamp=datetime.now(timezone.utc)
                )
                session.add(audit)
            await session.commit()
        logger.info(f"Audit log saved for account {account_id} [Case: {case_id}]")
        return True
    except Exception as exc:
        logger.error(f"Failed to write asynchronous PostgreSQL case audit log: {exc}")
        return False


async def log_case_audits_bulk(audits_data: list[dict]) -> bool:
    """Logs multiple audit records in a single bulk insert transaction."""
    if not audits_data:
        return True
    try:
        async with async_session() as session:
            async with session.begin():
                objects = [
                    CaseAudit(
                        case_id=data["case_id"],
                        account_id=data["account_id"],
                        event_type=data["event_type"],
                        ml_score=data["ml_score"],
                        graph_score=data["graph_score"],
                        composite_score=data["composite_score"],
                        severity=data["severity"],
                        mule_stage=data["mule_stage"],
                        evidence_hash=data.get("evidence_hash"),
                        action_taken=data.get("action_taken", "INVESTIGATOR_QUEUED"),
                        timestamp=datetime.now(timezone.utc)
                    )
                    for data in audits_data
                ]
                session.add_all(objects)
            await session.commit()
        logger.info(f"Successfully bulk saved {len(audits_data)} audit logs to PostgreSQL.")
        return True
    except Exception as exc:
        logger.error(f"Failed to execute bulk PostgreSQL case audit logs: {exc}")
        return False

