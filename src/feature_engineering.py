"""
feature_engineering.py
------------------------
Turns raw crawl fields (title text, meta description text, etc.)
into numeric features an ML model can use.
"""

import pandas as pd
import numpy as np


def _safe_len(x) -> int:
    if pd.isna(x):
        return 0
    return len(str(x).strip())


def _count_items(x) -> int:
    """Counts comma/@@-separated items (advertools joins multi-values
    with '@@'), falls back to 1 if a single non-empty string."""
    if pd.isna(x) or str(x).strip() == "":
        return 0
    text = str(x)
    if "@@" in text:
        return len([t for t in text.split("@@") if t.strip()])
    if "," in text:
        return len([t for t in text.split(",") if t.strip()])
    return 1


def _col_apply(out: pd.DataFrame, col: str, func, default=0):
    """Safely apply func to a column if it exists, else fill with default
    for every row (avoids index-mismatch bugs when a column is missing)."""
    if col in out.columns:
        return out[col].apply(func)
    return pd.Series([default] * len(out), index=out.index)


def build_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Input: standardized DataFrame from data_loader.load_seo_data()
    Output: same DataFrame + engineered numeric feature columns
    """
    out = df.copy()

    out["title_length"] = _col_apply(out, "title", _safe_len)
    out["meta_desc_length"] = _col_apply(out, "meta_desc", _safe_len)
    out["has_meta_desc"] = (out["meta_desc_length"] > 0).astype(int)

    out["h1_count"] = _col_apply(out, "h1", _count_items)
    out["h2_count"] = _col_apply(out, "h2", _count_items)

    if "word_count" in out.columns:
        out["word_count"] = pd.to_numeric(out["word_count"], errors="coerce").fillna(0)
    elif "body_text" in out.columns:
        out["word_count"] = out["body_text"].apply(
            lambda t: len(str(t).split()) if pd.notna(t) else 0
        )
    else:
        out["word_count"] = 0

    if "load_time" in out.columns:
        numeric_load = pd.to_numeric(out["load_time"], errors="coerce")
        fallback = numeric_load.median() if numeric_load.notna().any() else 3.0
        out["load_time"] = numeric_load.fillna(fallback)
    else:
        out["load_time"] = 3.0

    out["internal_links"] = _col_apply(out, "links_url", _count_items)
    out["image_count"] = _col_apply(out, "img_src", _count_items)

    if "status_code" in out.columns:
        out["is_200"] = (pd.to_numeric(out["status_code"], errors="coerce") == 200).astype(int)
    else:
        out["is_200"] = 1

    return out


FEATURE_COLUMNS = [
    "title_length", "meta_desc_length", "has_meta_desc",
    "h1_count", "h2_count", "word_count", "load_time",
    "internal_links", "image_count", "is_200",
]