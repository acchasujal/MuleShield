import unittest
import os
import sys
import asyncio

# Ensure project root is in the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.risk_scoring import calculate_composite_risk, assign_tier, align_lifecycle_stage
from backend.ml.score_fusion import derive_behavioral_txn_score
from backend.xml_generator import generate_goaml_xml
from backend.database import init_db, log_case_audit

class TestIntegrations(unittest.TestCase):
    def test_composite_risk_score_fusion(self):
        """Test Fusion v5 risk scoring arithmetic weights and bounds."""
        # Case A: Balanced input: ml=50%, graph=50%, txn=50 points
        # Composite = (50 * 0.40) + (50 * 0.40) + (50 * 0.20) = 20 + 20 + 10 = 50.0 points (MEDIUM)
        score = calculate_composite_risk(0.5, 0.5, 50.0)
        self.assertEqual(score, 50.0)
        self.assertEqual(assign_tier(score), "MEDIUM")

        # Case B: Offline graph fallback: ml=85%, graph=None, txn=0
        # Composite = (85 * 0.40) + (0 * 0.40) + (85 * 0.20) = 51.0 points (MEDIUM)
        score_offline = calculate_composite_risk(0.85, None, 0.0)
        self.assertEqual(score_offline, 51.0)
        self.assertEqual(assign_tier(score_offline), "MEDIUM")

        # Case C: Extreme values clamping bounds [0.0, 100.0]
        self.assertEqual(calculate_composite_risk(-0.5, -0.2, -50), 0.0)
        self.assertEqual(calculate_composite_risk(1.5, 1.2, 150), 100.0)

    def test_derive_behavioral_txn_score(self):
        """Verify behavioral transaction score derivation from BOI features.
        A confirmed mule profile must produce a non-zero score that enables CRITICAL tier.
        """
        # Confirmed mule: max behavioral signals
        mule_features = {
            "F115":  0.90,   # High transaction throughput ratio → 27 pts
            "F886":  0.80,   # High UPI spike → 16 pts
            "F3908": 0.85,   # High velocity ratio → 21.25 pts
            "F670":  1.0,    # Regulatory watchlist flag → 15 pts
            "F3889": "G365D",# Dormant reactivation → 10 pts
        }
        score = derive_behavioral_txn_score(mule_features)
        # Minimum expected: 27 + 16 + 21.25 + 15 + 10 = 89.25, clamped to 100
        self.assertGreaterEqual(score, 80.0, "Confirmed mule behavioral score must be >= 80")
        self.assertLessEqual(score, 100.0, "Score must be clamped at 100")

        # Legitimate account: all zeros → score = 0
        legit_features = {"F115": 0.0, "F886": 0.0, "F3908": 0.0, "F670": 0.0, "F3889": "L365D"}
        legit_score = derive_behavioral_txn_score(legit_features)
        self.assertEqual(legit_score, 0.0, "Legitimate account should score 0.0")

    def test_confirmed_mule_reaches_critical(self):
        """Verify that a confirmed mule account can reach CRITICAL tier via fusion.

        Prior bug: txn_score=0.0 was hardcoded, so max achievable with ml=0.85 was 51.0 (MEDIUM).
        After fix: behavioral txn_score from BOI features raises composite above 80.0 (CRITICAL).
        """
        mule_features = {
            "F115":  0.90,
            "F886":  0.80,
            "F3908": 0.85,
            "F670":  1.0,
            "F3889": "G365D",
        }
        ml_score = 0.85
        graph_score = 0.85   # fallback = ml_score
        behav_txn_score = derive_behavioral_txn_score(mule_features)

        composite = calculate_composite_risk(ml_score, graph_score, behav_txn_score)
        tier = assign_tier(composite)

        self.assertGreaterEqual(composite, 80.0, f"Composite {composite} must reach >= 80.0 for CRITICAL")
        self.assertEqual(tier, "CRITICAL", "Confirmed mule with max behavioral signals must be CRITICAL")

    def test_mule_lifecycle_stage_alignments(self):
        """Verify the logic that uplifts LEGITIMATE profiles to UNDER_REVIEW."""
        # Upgrade condition: Current is LEGITIMATE, severity is MEDIUM/HIGH/CRITICAL, txn_score > 0.0
        aligned_stage = align_lifecycle_stage(
            current_stage="LEGITIMATE",
            severity="MEDIUM",
            transaction_risk=40.0
        )
        self.assertEqual(aligned_stage, "UNDER_REVIEW")

        # Preserves profile-driven stages (e.g., ACTIVE_MULE remains ACTIVE_MULE)
        preserved_stage = align_lifecycle_stage(
            current_stage="ACTIVE_MULE",
            severity="CRITICAL",
            transaction_risk=80.0
        )
        self.assertEqual(preserved_stage, "ACTIVE_MULE")

        # No upgrade if transaction risk is 0.0
        no_upgrade = align_lifecycle_stage(
            current_stage="LEGITIMATE",
            severity="MEDIUM",
            transaction_risk=0.0
        )
        self.assertEqual(no_upgrade, "LEGITIMATE")

    def test_goaml_compliance_xml_generator(self):
        """Verify the goAML regulatory reporting XML generation schema format."""
        xml_output = generate_goaml_xml(
            case_id='STR-TEST-1234',
            account_no='ACC0520000000028',
            ml_score=0.85,
            graph_score=0.70,
            composite_score=80.5,
            severity='CRITICAL',
            mule_stage='ACTIVE_MULE',
            explanations=['TMS WATCHLIST Flag active', 'High velocity pass-through'],
            evidence=[{
                'from_account': 'ACC0520000000028',
                'to_account': 'ACC05299999999999',
                'amount': 150000.0,
                'timestamp': '2026-06-01 12:00:00',
                'channel': 'UPI'
            }]
        )
        
        self.assertIsNotNone(xml_output)
        self.assertTrue(xml_output.startswith("<?xml"), "XML document must start with xml declaration tag.")
        self.assertIn("<report>", xml_output)
        self.assertIn("<report_ref>STR-TEST-1234</report_ref>", xml_output)
        self.assertIn("<transactions>", xml_output)
        self.assertIn("ACC0520000000028", xml_output)

    def test_postgres_database_fallback_behavior(self):
        """Test PostgreSQL async logger connectivity fallback bounds."""
        # Run DB initialization and check error handling (should return False if DB is offline,
        # but not crash the thread process).
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            db_connected = loop.run_until_complete(init_db())
            
            # Whether database is online or offline, logging an audit should either succeed
            # or gracefully degrade (return False) without throwing unhandled exceptions.
            log_result = loop.run_until_complete(log_case_audit(
                case_id="STR-TEST-1234",
                account_id="ACC999",
                event_type="TEST",
                ml_score=0.5,
                graph_score=0.5,
                composite_score=50.0,
                severity="MEDIUM",
                mule_stage="UNDER_REVIEW"
            ))
            # Just ensure no exception propagates. The result is boolean status.
            self.assertIsInstance(log_result, bool)
        finally:
            loop.close()

if __name__ == '__main__':
    unittest.main()
