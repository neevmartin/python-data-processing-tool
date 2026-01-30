import pandas as pd
import numpy as np

def drop_empty_rows(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove rows where all values are missing.
    """
    return df.dropna(how='all').reset_index(drop=True)


def fill_missing_values(
    df: pd.DataFrame,
    strategy: str = "mean"
) -> pd.DataFrame:
    """
    Fill missing numerical values using:
    - mean
    - median
    - zero
    """
    df = df.copy()
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    
    for col in numeric_cols:
        if strategy == "mean":
            fill_value = df[col].mean()
        elif strategy == "median":
            fill_value = df[col].median()
        elif strategy == "zero":
            fill_value = 0
        else:
            raise ValueError(f"Unknown strategy: {strategy}")
        
        df[col] = df[col].fillna(fill_value)
    
    return df


def convert_column_types(
    df: pd.DataFrame,
    schema: dict[str, type]
) -> pd.DataFrame:
    """
    Convert columns to expected data types.
    Example schema:
    {"age": int, "salary": float}
    """
    df = df.copy()
    try:
        return df.astype(schema)
    except Exception as e:
        raise ValueError(f"Error converting column types: {e}")
