import unittest
import os
import sys
import pandas as pd

# Ensure project root is in the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.ml_service import MLService
from backend.utils import lookup_account_features

class TestMLPipeline(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ml = MLService()

    def test_ml_service_loading(self):
        """Verify that ML Service loaded the model classifiers and imputer assets successfully."""
        self.assertTrue(self.ml.is_loaded, "MLService model or preprocessors failed to load.")

    def test_single_prediction_and_shap(self):
        """Test single account prediction pipelines and SHAP explanation details."""
        # Standard input representation resembling account inspector search inputs
        test_features = {
            'Unnamed: 0': 28,
            'F670': 0.0,
            'F886': 0.2,
            'F3912': 1.0
        }
        result = self.ml.predict_single(test_features)
        
        # Verify schema expectations
        self.assertIn("ml_score", result)
        self.assertIn("mule_stage", result)
        self.assertIn("shap_signals", result)
        self.assertNotIn("error", result, f"Single prediction failed with error: {result.get('error')}")

        # Check score bounds
        self.assertGreaterEqual(result["ml_score"], 0.0)
        self.assertLessEqual(result["ml_score"], 1.0)
        
        # Verify SHAP attributions are generated (top features)
        self.assertGreater(len(result["shap_signals"]), 0, "No SHAP feature signals returned.")

    def test_batch_prediction(self):
        """Test batch prediction vectorised pipeline using actual dataset slices."""
        dataset_path = 'data/boi/DataSet.csv'
        if not os.path.exists(dataset_path):
            self.skipTest(f"Skipping batch prediction test since {dataset_path} is missing.")
            
        # Ingest a small batch
        df = pd.read_csv(dataset_path, nrows=5)
        results = self.ml.predict_batch(df)
        
        self.assertEqual(len(results), 5, f"Expected 5 batch results, got {len(results)}")
        for idx, row in enumerate(results):
            with self.subTest(row_index=idx):
                self.assertIn("ml_score", row)
                self.assertIn("mule_stage", row)
                self.assertIn("shap_signals", row)
                self.assertGreaterEqual(row["ml_score"], 0.0)
                self.assertLessEqual(row["ml_score"], 1.0)

    def test_dataset_seeker_lookup(self):
        """Verify that sequential seeker seeker features successfully scan DataSet.csv."""
        dataset_path = 'data/boi/DataSet.csv'
        if not os.path.exists(dataset_path):
            self.skipTest(f"Skipping dataset seeker lookup since {dataset_path} is missing.")
            
        # Standard lookups
        row = lookup_account_features(28)
        self.assertIsNotNone(row, "Failed to lookup index 28 in DataSet.csv.")
        self.assertEqual(int(row.get("Unnamed: 0", -1)), 28)

        # Fallback coordinate lookup
        fallback_row = lookup_account_features(999999)
        self.assertIsNotNone(fallback_row, "Failed to get fallback row representation.")
        self.assertEqual(int(fallback_row.get("Unnamed: 0", -1)), 999)

if __name__ == '__main__':
    unittest.main()
