"""
app.py
-------
Competitor SEO Analysis Tool - Streamlit dashboard.

Run:
    python -m streamlit run app.py
"""

import os
import joblib
import pandas as pd
import streamlit as st

from src.data_loader import load_seo_data
from src.feature_engineering import build_features, FEATURE_COLUMNS
from src.seo_scorer import add_seo_score

st.set_page_config(page_title="Competitor SEO Analysis Tool", layout="wide")
st.title("🔍 Competitor SEO Analysis Tool")
st.caption("Compare on-page SEO health across competitor websites using ML.")

MODEL_DIR = "models"
DEFAULT_DATA = "data/seo_crawl_data.csv"


@st.cache_resource
def load_models():
    reg_path = os.path.join(MODEL_DIR, "seo_score_regressor.pkl")
    clf_path = os.path.join(MODEL_DIR, "seo_category_classifier.pkl")
    reg = joblib.load(reg_path) if os.path.exists(reg_path) else None
    clf = joblib.load(clf_path) if os.path.exists(clf_path) else None
    return reg, clf


def process(csv_path_or_buffer):
    raw = pd.read_csv(csv_path_or_buffer, low_memory=False)
    raw.to_csv("data/_uploaded_temp.csv", index=False)
    df = load_seo_data("data/_uploaded_temp.csv")
    df = build_features(df)
    df = add_seo_score(df)
    return df


st.sidebar.header("Data")
uploaded = st.sidebar.file_uploader("Upload competitor crawl CSV", type="csv")
use_sample = st.sidebar.button("Use bundled sample data")

if "data" not in st.session_state:
    st.session_state.data = None

if uploaded is not None:
    st.session_state.data = process(uploaded)
elif use_sample:
    if not os.path.exists(DEFAULT_DATA):
        st.sidebar.warning("No sample data yet — run generate_sample_data.py first.")
    else:
        st.session_state.data = process(DEFAULT_DATA)

df = st.session_state.data

if df is None:
    st.info("⬅️ Upload a crawl CSV (or click 'Use bundled sample data') to get started.")
    st.stop()

col1, col2, col3 = st.columns(3)
col1.metric("Pages Analyzed", len(df))
col2.metric("Competitors (Domains)", df["domain"].nunique() if "domain" in df else "N/A")
col3.metric("Avg SEO Score", f"{df['seo_score'].mean():.1f} / 100")

st.divider()

st.subheader("📊 Competitor Comparison")
if "domain" in df.columns:
    comp = df.groupby("domain")["seo_score"].mean().sort_values(ascending=False)
    st.bar_chart(comp)
else:
    st.warning("No 'domain' column detected — showing overall scores only.")

st.subheader("📈 SEO Category Breakdown")
cat_counts = df["seo_category"].value_counts()
st.bar_chart(cat_counts)

st.subheader("🏆 Top & Bottom Pages by SEO Score")
show_cols = [c for c in ["url", "domain", "title", "seo_score", "seo_category"] if c in df.columns]
c1, c2 = st.columns(2)
with c1:
    st.write("**Top 5**")
    st.dataframe(df.sort_values("seo_score", ascending=False)[show_cols].head(5))
with c2:
    st.write("**Bottom 5**")
    st.dataframe(df.sort_values("seo_score")[show_cols].head(5))

st.subheader("🤖 What Drives SEO Score (ML Feature Importance)")
reg, clf = load_models()
if reg is not None:
    importance = pd.Series(reg.feature_importances_, index=FEATURE_COLUMNS).sort_values()
    st.bar_chart(importance)
else:
    st.info("Train the model first: `python -m src.train_model`")

# --- Full table + download ---
st.subheader("📄 Full Data")
display_cols = show_cols + ["title_length", "meta_desc_length", "word_count", "load_time"]
st.dataframe(df[display_cols].head(500))
if len(df) > 500:
    st.caption(f"Showing first 500 of {len(df)} rows.")

st.write("")
if st.button("Prepare CSV for download"):
    with st.spinner("Building CSV..."):
        export_df = df[display_cols]  # only the clean, relevant columns
        csv_bytes = export_df.to_csv(index=False).encode("utf-8-sig")  # utf-8-sig = opens correctly in Excel
    st.download_button(
        "Download scored data as CSV",
        csv_bytes,
        file_name="competitor_seo_scored.csv",
        mime="text/csv",
    )
