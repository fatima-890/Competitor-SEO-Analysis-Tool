"""
train_model.py
----------------
Trains two models on the engineered features:
  1. RandomForestRegressor  -> predicts the continuous SEO score (0-100)
  2. RandomForestClassifier -> predicts the SEO category (Poor/Average/Good)

Run:
    python -m src.train_model
"""

import os
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.metrics import (
    mean_absolute_error, r2_score,
    accuracy_score, classification_report,
)

from src.data_loader import load_seo_data
from src.feature_engineering import build_features, FEATURE_COLUMNS
from src.seo_scorer import add_seo_score
from src.config import RANDOM_STATE

DATA_PATH = "data/seo_crawl_data.csv"
MODEL_DIR = "models"


def prepare_dataset(csv_path: str = DATA_PATH) -> pd.DataFrame:
    df = load_seo_data(csv_path)
    df = build_features(df)
    df = add_seo_score(df)
    return df


def train():
    os.makedirs(MODEL_DIR, exist_ok=True)
    df = prepare_dataset()

    X = df[FEATURE_COLUMNS]
    y_reg = df["seo_score"]
    y_clf = df["seo_category"]

    X_train, X_test, yreg_train, yreg_test, yclf_train, yclf_test = train_test_split(
        X, y_reg, y_clf, test_size=0.2, random_state=RANDOM_STATE
    )

    # --- Regressor ---
    reg = RandomForestRegressor(n_estimators=200, random_state=RANDOM_STATE)
    reg.fit(X_train, yreg_train)
    pred_reg = reg.predict(X_test)
    print("=== SEO Score Regressor ===")
    print(f"MAE : {mean_absolute_error(yreg_test, pred_reg):.2f}")
    print(f"R2  : {r2_score(yreg_test, pred_reg):.3f}\n")

    # --- Classifier ---
    clf = RandomForestClassifier(n_estimators=200, random_state=RANDOM_STATE)
    clf.fit(X_train, yclf_train)
    pred_clf = clf.predict(X_test)
    print("=== SEO Category Classifier ===")
    print(f"Accuracy: {accuracy_score(yclf_test, pred_clf):.3f}")
    print(classification_report(yclf_test, pred_clf))

    # --- Feature importance ---
    importance = pd.Series(reg.feature_importances_, index=FEATURE_COLUMNS)
    importance = importance.sort_values(ascending=False)
    print("=== Feature Importance (Regressor) ===")
    print(importance.round(3))

    # --- Save artifacts ---
    joblib.dump(reg, os.path.join(MODEL_DIR, "seo_score_regressor.pkl"))
    joblib.dump(clf, os.path.join(MODEL_DIR, "seo_category_classifier.pkl"))
    importance.to_csv(os.path.join(MODEL_DIR, "feature_importance.csv"))
    print(f"\nModels saved to {MODEL_DIR}/")

    return reg, clf, df


if __name__ == "__main__":
    train()