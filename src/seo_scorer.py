"""
seo_scorer.py
--------------
Rule-based SEO Health Score (0-100), built from established on-page
SEO best practices. This acts as the ML target: instead of needing
human-labeled data, we generate the label from the rules, then train
a model to *learn* and *generalize* that scoring logic.
"""

import pandas as pd
from src.config import THRESHOLDS as T


def _score_row(row) -> int:
    score = 0

    tl = row["title_length"]
    if T["title_len_ideal"][0] <= tl <= T["title_len_ideal"][1]:
        score += 20
    elif T["title_len_ok"][0] <= tl <= T["title_len_ok"][1]:
        score += 10

    ml = row["meta_desc_length"]
    if T["meta_len_ideal"][0] <= ml <= T["meta_len_ideal"][1]:
        score += 20
    elif ml > 0:
        score += 10

    wc = row["word_count"]
    if wc >= T["word_count_good"]:
        score += 15
    elif wc >= T["word_count_ok"]:
        score += 8

    h1 = row["h1_count"]
    if h1 == 1:
        score += 15
    elif h1 > 1:
        score += 7

    if row["has_meta_desc"] == 1:
        score += 10

    lt = row["load_time"]
    if lt <= T["load_time_good"]:
        score += 10
    elif lt <= T["load_time_ok"]:
        score += 5

    if row["internal_links"] >= T["min_internal_links"]:
        score += 10

    return min(score, 100)


def add_seo_score(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["seo_score"] = out.apply(_score_row, axis=1)
    out["seo_category"] = pd.cut(
        out["seo_score"],
        bins=[-1, 49, 74, 100],
        labels=["Poor", "Average", "Good"],
    )
    return out