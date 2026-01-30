import pandas as pd
import os

def load_csv(path: str) -> pd.DataFrame:
    """
    Load a CSV file into a DataFrame.
    Raises ValueError if file cannot be loaded.
    """
    if not os.path.exists(path):
        raise ValueError(f"File not found: {path}")
    try:
        return pd.read_csv(path)
    except Exception as e:
        raise ValueError(f"Error loading CSV file {path}: {e}")

def load_json(path: str) -> pd.DataFrame:
    """
    Load a JSON file into a DataFrame.
    Supports list-of-records JSON.
    """
    if not os.path.exists(path):
        raise ValueError(f"File not found: {path}")
    try:
        return pd.read_json(path, orient='records')
    except Exception as e:
        raise ValueError(f"Error loading JSON file {path}: {e}")

def load_data(path: str) -> pd.DataFrame:
    """
    Detect file type by extension and delegate
    to the appropriate loader.
    """
    _, ext = os.path.splitext(path)
    ext = ext.lower()
    
    if ext == '.csv':
        return load_csv(path)
    elif ext == '.json':
        return load_json(path)
    else:
        raise ValueError(f"Unsupported file format: {ext}")
