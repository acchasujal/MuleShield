import unittest
import os
import sys

# Ensure project root is in the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class TestCoreSystem(unittest.TestCase):
    def test_backend_module_imports(self):
        """Verify that all core backend python modules compile and import successfully."""
        modules_to_test = [
            'backend.app',
            'backend.ml_service',
            'backend.graph_service',
            'backend.database',
            'backend.risk_scoring',
            'backend.xml_generator',
            'backend.routers.ml_predict',
            'backend.routers.i4c_webhook',
            'backend.explain',
            'backend.fraud_detection',
            'backend.graph_builder',
            'backend.ml.predictor',
            'backend.ml.shap_engine',
            'backend.ml.feature_lookup',
            'backend.ml.lifecycle_engine',
            'backend.ml.score_fusion',
            'backend.ml.schemas'
        ]
        for mod in modules_to_test:
            with self.subTest(module=mod):
                try:
                    imported_mod = __import__(mod, fromlist=['*'])
                    self.assertIsNotNone(imported_mod)
                except Exception as e:
                    self.fail(f"Failed to import {mod}: {e}")

    def test_configuration_blueprints(self):
        """Verify that the environmental .env.example blueprint exists."""
        self.assertTrue(os.path.exists('.env.example'), "Blueprint .env.example is missing from repository root.")

    def test_json_demo_fallbacks_existence(self):
        """Verify that all front-end fallback JSON data matrices exist in data/."""
        fallback_files = [
            'data/fallback_roundtrip_analysis.json',
            'data/fallback_structuring_analysis.json',
            'data/fallback_dormant_analysis.json',
        ]
        for fp in fallback_files:
            with self.subTest(file=fp):
                self.assertTrue(os.path.exists(fp), f"Fallback JSON file {fp} is missing.")

    def test_scenario_csvs_existence(self):
        """Verify that demo scenario CSV files exist in data/."""
        scenario_files = [
            'data/scenario_roundtrip.csv',
            'data/scenario_structuring.csv',
            'data/scenario_dormant.csv',
        ]
        for fp in scenario_files:
            with self.subTest(file=fp):
                self.assertTrue(os.path.exists(fp), f"Scenario CSV file {fp} is missing.")

if __name__ == '__main__':
    unittest.main()
