"""
MuleShield AI — Neo4j Graph Database Connectivity Service
Manages Bolt connection pools, dynamic Cypher transactions, GDS centrality metrics, and 3-hop traversal traversals.
"""

import os
import logging
import pandas as pd
from neo4j import GraphDatabase, AsyncGraphDatabase

logger = logging.getLogger("muleshield.graph")

class Neo4jService:
    def __init__(self):
        self.uri = os.getenv("NEO4J_URI", os.getenv("NEO4J_URL", "bolt://localhost:7687"))
        self.user = os.getenv("NEO4J_USER", "neo4j")
        self.password = os.getenv("NEO4J_PASSWORD", "password")
        self.driver = None
        self.async_driver = None
        self.is_connected = False
        
        self.connect()

    def connect(self):
        """Initializes the Bolt driver and verifies database liveness."""
        try:
            logger.info(f"Connecting to Neo4j Community Server at {self.uri}...")
            self.driver = GraphDatabase.driver(self.uri, auth=(self.user, self.password))
            
            # Verify connectivity
            self.driver.verify_connectivity()
            self.is_connected = True
            logger.info("Successfully connected to Neo4j database (Bolt active).")
            
            # Initialize async driver for FastAPI non-blocking endpoints
            self.async_driver = AsyncGraphDatabase.driver(self.uri, auth=(self.user, self.password))
            
            # Create schema constraints
            self.create_constraints()
        except Exception as exc:
            logger.error(f"Failed to connect to Neo4j database: {exc}. Reverting to Standalone ML mode.")
            self.is_connected = False
            if self.driver:
                try:
                    self.driver.close()
                except Exception:
                    pass
                self.driver = None
            self.async_driver = None

    def create_constraints(self):
        """Creates unique node keys and transaction index indices inside Neo4j."""
        if not self.is_connected:
            return
        try:
            with self.driver.session() as session:
                # Create unique constraint on Account node
                session.run("CREATE CONSTRAINT account_id_unique IF NOT EXISTS FOR (a:Account) REQUIRE a.id IS UNIQUE")
                # Create index on transactions timestamp for rapid 3-hop sliding traversals
                session.run("CREATE INDEX transaction_ts_idx IF NOT EXISTS FOR ()-[r:TRANSACTED]-() REQUIRE r.timestamp IS NOT NULL")
                logger.info("Neo4j database schema constraints successfully applied.")
        except Exception as exc:
            logger.warning(f"Could not apply Neo4j constraints: {exc}")

    def close(self):
        """Closes all active database drivers."""
        if self.driver:
            self.driver.close()
            logger.info("Neo4j Bolt connection closed.")
        if self.async_driver:
            # Async close
            import asyncio
            try:
                loop = asyncio.get_event_loop()
                if loop.is_running():
                    loop.create_task(self.async_driver.close())
            except Exception:
                pass

    async def get_centrality(self, account_id: str) -> float:
        """Fetches degree centrality and connectivity score for an account.

        Returns:
            A score between [0.0, 1.0]. Defaults to 0.0 if not connected.
        """
        if not self.is_connected or not self.async_driver:
            return 0.0

        try:
            # We calculate degree centrality on-the-fly:
            # (In-degree + Out-degree) normalized by total possible connections in the immediate neighborhood
            query = """
            MATCH (a:Account {id: $account_id})
            OPTIONAL MATCH (a)-[r:TRANSACTED]-()
            WITH a, count(r) as degree
            MATCH (total:Account)
            WITH degree, count(total) as N
            RETURN case when N > 1 then toFloat(degree) / (N - 1) else 0.0 end as centrality
            """
            async with self.async_driver.session() as session:
                result = await session.run(query, account_id=account_id)
                record = await result.single()
                if record:
                    # Normalize and amplify the connectivity score to make graph differences visible
                    centrality = record.get("centrality", 0.0)
                    return min(1.0, centrality * 5.0)  # scale factor to make it visual
            return 0.0
        except Exception as exc:
            logger.warning(f"Error fetching Neo4j centrality for account {account_id}: {exc}")
            return 0.0

    async def seed_transaction(self, from_acc: str, to_acc: str, amount: float, timestamp: str, channel: str = "Unknown"):
        """Seeds a single transaction edge asynchronously in real-time."""
        if not self.is_connected or not self.async_driver:
            return

        try:
            query = """
            MERGE (s:Account {id: $from_acc})
            MERGE (t:Account {id: $to_acc})
            CREATE (s)-[:TRANSACTED {amount: $amount, timestamp: $timestamp, channel: $channel}]->(t)
            """
            async with self.async_driver.session() as session:
                await session.run(query, from_acc=from_acc, to_acc=to_acc, amount=float(amount), timestamp=timestamp, channel=channel)
        except Exception as exc:
            logger.warning(f"Failed to seed real-time transaction to Neo4j: {exc}")

    async def seed_batch_transactions(self, df: pd.DataFrame):
        """Asynchronously seeds a batch of transactions log from a pandas DataFrame."""
        if not self.is_connected or not self.async_driver:
            return

        try:
            logger.info(f"Seeding {len(df)} transactions into Neo4j in the background...")
            # Format dataframe records
            txns = []
            for _, row in df.head(1000).iterrows():  # Cap at 1000 for seed speed bounds
                txns.append({
                    "from_acc": str(row.get("from_account", "")),
                    "to_acc": str(row.get("to_account", "")),
                    "amount": float(row.get("amount", 0)),
                    "timestamp": str(row.get("timestamp", "")),
                    "channel": str(row.get("channel", "Unknown"))
                })

            query = """
            UNWIND $txns as txn
            MERGE (s:Account {id: txn.from_acc})
            MERGE (t:Account {id: txn.to_acc})
            CREATE (s)-[:TRANSACTED {amount: txn.amount, timestamp: txn.timestamp, channel: txn.channel}]->(t)
            """
            async with self.async_driver.session() as session:
                await session.run(query, txns=txns)
            logger.info("Neo4j background transaction seeding successfully completed.")
        except Exception as exc:
            logger.error(f"Failed to execute batch Neo4j seed: {exc}")

    async def get_centralities_bulk(self, account_ids: list[str]) -> dict[str, float]:
        """Fetches degree centrality scores for a list of accounts in a single batch query.

        Returns:
            A dictionary mapping account_id to normalized scaled centrality score.
        """
        if not self.is_connected or not self.async_driver or not account_ids:
            return {}

        try:
            query = """
            MATCH (total:Account)
            WITH count(total) as N
            MATCH (a:Account) WHERE a.id IN $account_ids
            OPTIONAL MATCH (a)-[r:TRANSACTED]-()
            RETURN a.id as id, count(r) as degree, N
            """
            scores = {}
            async with self.async_driver.session() as session:
                result = await session.run(query, account_ids=account_ids)
                async for record in result:
                    acc_id = record.get("id")
                    degree = record.get("degree", 0)
                    N = record.get("N", 0)
                    centrality = (degree / (N - 1)) if N > 1 else 0.0
                    scaled_score = min(1.0, centrality * 5.0)
                    scores[acc_id] = scaled_score
            return scores
        except Exception as exc:
            logger.warning(f"Error fetching bulk Neo4j centralities: {exc}")
            return {}
