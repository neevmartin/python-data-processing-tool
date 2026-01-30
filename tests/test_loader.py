import unittest
import pandas as pd
import os
import json
import shutil
from src.loader import load_csv, load_json, load_data

class TestLoader(unittest.TestCase):
    def setUp(self):
        self.test_dir = "tests/temp_data"
        os.makedirs(self.test_dir, exist_ok=True)
        self.csv_path = os.path.join(self.test_dir, "test.csv")
        self.json_path = os.path.join(self.test_dir, "test.json")
        
        # Sample data
        self.data = [
            {"id": 1, "name": "Alice", "score": 85},
            {"id": 2, "name": "Bob", "score": 90}
        ]
        
        # Create CSV
        df = pd.DataFrame(self.data)
        df.to_csv(self.csv_path, index=False)
        
        # Create JSON
        with open(self.json_path, 'w') as f:
            json.dump(self.data, f)

    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_load_csv_success(self):
        df = load_csv(self.csv_path)
        self.assertEqual(len(df), 2)
        self.assertEqual(list(df.columns), ["id", "name", "score"])

    def test_load_csv_file_not_found(self):
        with self.assertRaises(ValueError) as cm:
            load_csv("non_existent.csv")
        self.assertIn("File not found", str(cm.exception))

    def test_load_json_success(self):
        df = load_json(self.json_path)
        self.assertEqual(len(df), 2)
        self.assertEqual(list(df.columns), ["id", "name", "score"])

    def test_load_json_file_not_found(self):
        with self.assertRaises(ValueError) as cm:
            load_json("non_existent.json")
        self.assertIn("File not found", str(cm.exception))

    def test_load_data_csv(self):
        df = load_data(self.csv_path)
        self.assertEqual(len(df), 2)

    def test_load_data_json(self):
        df = load_data(self.json_path)
        self.assertEqual(len(df), 2)

    def test_load_data_unsupported(self):
        txt_path = os.path.join(self.test_dir, "test.txt")
        with open(txt_path, 'w') as f:
            f.write("text")
        with self.assertRaises(ValueError) as cm:
            load_data(txt_path)
        self.assertIn("Unsupported file format", str(cm.exception))

if __name__ == "__main__":
    unittest.main()
