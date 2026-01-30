import unittest
import pandas as pd
import numpy as np
from src.cleaner import drop_empty_rows, fill_missing_values, convert_column_types

class TestCleaner(unittest.TestCase):
    def setUp(self):
        self.df_with_empty = pd.DataFrame({
            "a": [1, np.nan, 3, np.nan],
            "b": [4, np.nan, 6, np.nan]
        })
        
        self.df_with_nans = pd.DataFrame({
            "a": [1, np.nan, 3],
            "b": [np.nan, 5, 6],
            "c": ["x", "y", np.nan]
        })

    def test_drop_empty_rows(self):
        cleaned_df = drop_empty_rows(self.df_with_empty)
        self.assertEqual(len(cleaned_df), 2)
        self.assertEqual(cleaned_df.loc[0, "a"], 1)
        self.assertEqual(cleaned_df.loc[1, "a"], 3)

    def test_fill_missing_values_mean(self):
        df = pd.DataFrame({"a": [1, np.nan, 3]})
        filled_df = fill_missing_values(df, strategy="mean")
        self.assertEqual(filled_df.loc[1, "a"], 2.0)

    def test_fill_missing_values_median(self):
        df = pd.DataFrame({"a": [1, np.nan, 5]})
        filled_df = fill_missing_values(df, strategy="median")
        self.assertEqual(filled_df.loc[1, "a"], 3.0)

    def test_fill_missing_values_zero(self):
        df = pd.DataFrame({"a": [1, np.nan, 3]})
        filled_df = fill_missing_values(df, strategy="zero")
        self.assertEqual(filled_df.loc[1, "a"], 0.0)

    def test_fill_missing_values_invalid_strategy(self):
        with self.assertRaises(ValueError):
            fill_missing_values(self.df_with_nans, strategy="invalid")

    def test_convert_column_types(self):
        df = pd.DataFrame({"a": ["1", "2"], "b": [3.1, 4.2]})
        schema = {"a": int, "b": int}
        converted_df = convert_column_types(df, schema)
        self.assertEqual(converted_df["a"].dtype, int)
        self.assertEqual(converted_df["b"].dtype, int)
        self.assertEqual(converted_df.loc[0, "b"], 3)

    def test_convert_column_types_error(self):
        df = pd.DataFrame({"a": ["abc", "def"]})
        schema = {"a": int}
        with self.assertRaises(ValueError):
            convert_column_types(df, schema)

if __name__ == "__main__":
    unittest.main()
