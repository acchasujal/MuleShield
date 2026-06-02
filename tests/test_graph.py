import unittest
import os
import sys
import pandas as pd
import networkx as nx

# Ensure project root is in the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.graph_builder import build_graph
from backend.fraud_detection import (
    detect_cycles,
    detect_layering,
    detect_structuring,
    detect_velocity,
    detect_dormant,
    ml_anomaly
)
from backend.graph_service import Neo4jService

class TestGraphSystem(unittest.TestCase):
    def setUp(self):
        # Create a mock transaction dataframe representing typical scenarios
        self.df_mock = pd.DataFrame([
            {"from_account": "ACC1", "to_account": "ACC2", "amount": 50000.0, "timestamp": "2026-06-01 10:00:00", "channel": "UPI"},
            {"from_account": "ACC2", "to_account": "ACC3", "amount": 49000.0, "timestamp": "2026-06-01 10:15:00", "channel": "UPI"},
            {"from_account": "ACC3", "to_account": "ACC1", "amount": 48000.0, "timestamp": "2026-06-01 10:30:00", "channel": "UPI"}, # Cycle ACC1 -> ACC2 -> ACC3 -> ACC1
            {"from_account": "ACC4", "to_account": "ACC5", "amount": 90000.0, "timestamp": "2026-06-01 11:00:00", "channel": "RTGS"},
            {"from_account": "ACC4", "to_account": "ACC5", "amount": 85000.0, "timestamp": "2026-06-01 11:30:00", "channel": "RTGS"},
            {"from_account": "ACC4", "to_account": "ACC5", "amount": 75000.0, "timestamp": "2026-06-01 11:45:00", "channel": "RTGS"}, # Velocity ACC4
        ])

    def test_build_networkx_graph(self):
        """Verify building a NetworkX directed graph from tabular transaction data."""
        G = build_graph(self.df_mock)
        self.assertIsInstance(G, nx.DiGraph)
        self.assertEqual(len(G.nodes), 5)
        self.assertEqual(len(G.edges), 4) # 4 unique directed edges (ACC4 -> ACC5 merges duplicate transactions)
        
        # Verify edge attributes
        edge_data = G.get_edge_data("ACC1", "ACC2")
        self.assertEqual(edge_data["amount"], 50000.0)
        self.assertEqual(edge_data["channel"], "UPI")

    def test_circular_cycle_detection(self):
        """Verify detection of circular transaction loops (cycles)."""
        G = build_graph(self.df_mock)
        cycles = detect_cycles(G)
        self.assertGreater(len(cycles), 0, "No circular cycle detected.")
        self.assertIn("ACC1", cycles[0])
        self.assertIn("ACC2", cycles[0])
        self.assertIn("ACC3", cycles[0])

    def test_layering_detection(self):
        """Verify multi-hop fund routing (layering paths) detection."""
        # Setup a clean layering flow: A -> B -> C -> D -> E
        df_layering = pd.DataFrame([
            {"from_account": "ACCA", "to_account": "ACCB", "amount": 10000.0, "timestamp": "2026-06-02 09:00:00"},
            {"from_account": "ACCB", "to_account": "ACCC", "amount": 9900.0, "timestamp": "2026-06-02 09:10:00"},
            {"from_account": "ACCC", "to_account": "ACCD", "amount": 9800.0, "timestamp": "2026-06-02 09:20:00"},
            {"from_account": "ACCD", "to_account": "ACCE", "amount": 9700.0, "timestamp": "2026-06-02 09:30:00"}
        ])
        G = build_graph(df_layering)
        paths = detect_layering(G)
        self.assertGreater(len(paths), 0, "Layering loops failed to identify.")
        self.assertTrue(all(len(path) >= 4 for path in paths), "Found path shorter than 4 nodes.")

    def test_structuring_detection(self):
        """Verify structuring (smurfing) heuristic rules."""
        # 3 transactions of sub-100K summing to >500K in 4h window
        df_structuring = pd.DataFrame([
            {"from_account": "SMURF", "to_account": "SINK", "amount": 95000.0, "timestamp": "2026-06-02 12:00:00"},
            {"from_account": "SMURF", "to_account": "SINK", "amount": 95000.0, "timestamp": "2026-06-02 12:30:00"},
            {"from_account": "SMURF", "to_account": "SINK", "amount": 95000.0, "timestamp": "2026-06-02 13:00:00"},
            {"from_account": "SMURF", "to_account": "SINK", "amount": 95000.0, "timestamp": "2026-06-02 13:30:00"},
            {"from_account": "SMURF", "to_account": "SINK", "amount": 95000.0, "timestamp": "2026-06-02 14:00:00"},
            {"from_account": "SMURF", "to_account": "SINK", "amount": 95000.0, "timestamp": "2026-06-02 14:30:00"}, # Total sum = 570,000 in 2.5h
        ])
        flagged = detect_structuring(df_structuring)
        self.assertIn("SMURF", flagged, "Failed to flag structured transactions account.")

    def test_velocity_detection(self):
        """Verify transaction frequency velocity rules."""
        flagged = detect_velocity(self.df_mock)
        self.assertIn("ACC4", flagged, "Failed to flag high-velocity account ACC4.")

    def test_dormant_reactivation(self):
        """Verify sudden reactivation of dormant account alerts."""
        df_dormant = pd.DataFrame([
            {"from_account": "ACCX", "to_account": "ACCY", "amount": 1000.0, "timestamp": "2025-01-01 10:00:00"},
            {"from_account": "ACCX", "to_account": "ACCY", "amount": 95000.0, "timestamp": "2025-09-01 10:00:00"}, # Gap of 243 days reactivated
        ])
        flagged = detect_dormant(df_dormant)
        self.assertIn("ACCX", flagged, "Failed to identify dormant reactivation on ACCX.")

    def test_neo4j_service_fallback(self):
        """Verify Neo4j service initializes and falls back gracefully when offline."""
        try:
            ns = Neo4jService()
            # If offline (expected in sandbox without docker composition active),
            # verify that centrality and seeding calls do not crash but fallback.
            self.assertIsNotNone(ns)
            if not ns.is_connected:
                # Test silent fallback
                import asyncio
                centrality = asyncio.run(ns.get_centrality("ACC0520000000028"))
                self.assertEqual(centrality, 0.0, "Offline centrality should fall back to 0.0.")
            ns.close()
        except Exception as e:
            self.fail(f"Neo4jService initialization crashed: {e}")

if __name__ == '__main__':
    unittest.main()
