import pandas as pd
from pathlib import Path

CACHE_DIR = Path("data/processed")

def save(df: pd.DataFrame, name: str) -> None:
    CACHE_DIR.mkdir(exist_ok=True)
    df.to_parquet(CACHE_DIR / f"{name}.parquet")
    print(f"Saved {name}.parquet")

def load(name: str) -> pd.DataFrame:
    path = CACHE_DIR / f"{name}.parquet"
    if not path.exists():
        raise FileNotFoundError(f"{name}.parquet not found — run download first")
    return pd.read_parquet(path)