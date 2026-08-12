"""
data_loader.py
---------------
Loads a competitor SEO crawl CSV and normalizes its column names to
the standard schema defined in config.COLUMN_MAP, no matter what the
original headers were called.
"""

import os
import re
import pandas as pd
from urllib.parse import urlparse
from src.config import COLUMN_MAP


def _normalize(col_name: str) -> str:
    """lowercase + strip spaces/underscores for fuzzy matching."""
    return re.sub(r"[\s_]+", "", str(col_name).lower())


def _auto_map_columns(df: pd.DataFrame) -> dict:
    """
    Returns {standard_field_name: actual_column_in_df}
    for every field we can find a match for.
    """
    normalized_lookup = {_normalize(c): c for c in df.columns}
    resolved = {}
    for standard_field, variants in COLUMN_MAP.items():
        for variant in variants:
            key = _normalize(variant)
            if key in normalized_lookup:
                resolved[standard_field] = normalized_lookup[key]
                break
    return resolved


def load_seo_data(csv_path: str) -> pd.DataFrame:
    """
    Load the raw crawl CSV and return a DataFrame with standardized
    column names (only the columns that were found are included).
    """
    if not os.path.exists(csv_path):
        raise FileNotFoundError(
            f"Couldn't find {csv_path}. Download the dataset from Kaggle "
            "and place the CSV in the data/ folder (see README)."
        )

    raw = pd.read_csv(csv_path, low_memory=False)
    mapping = _auto_map_columns(raw)

    missing = [f for f in ["url", "title", "meta_desc", "word_count"]
               if f not in mapping]
    if missing:
        print(
            f"[WARNING] Couldn't auto-detect columns for: {missing}. "
            "Open the CSV, check the real header names, and add them "
            "to COLUMN_MAP in src/config.py."
        )

    clean = pd.DataFrame()
    for standard_field, actual_col in mapping.items():
        clean[standard_field] = raw[actual_col]

    if "domain" not in clean.columns and "url" in clean.columns:
        clean["domain"] = clean["url"].apply(
            lambda u: urlparse(str(u)).netloc if pd.notna(u) else "unknown"
        )

    return clean


if __name__ == "__main__":
    df = load_seo_data("data/seo_crawl_data.csv")
    print(df.head())
    print(f"\nLoaded {len(df)} rows, {df['domain'].nunique() if 'domain' in df else '?'} domains")