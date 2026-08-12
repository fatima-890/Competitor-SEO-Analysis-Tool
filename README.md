# 🔍 Competitor SEO Analysis Tool

An ML-powered dashboard that scores competitor web pages on on-page SEO health using RandomForest models trained on rule-based SEO best-practice logic. Upload a competitor crawl CSV, compare domains side-by-side, spot weak pages, and see exactly which SEO factors matter most, all inside one interactive Streamlit app.

---

## 📖 Overview

This project analyzes crawled website data (titles, meta descriptions, headings, word count, page speed, links) for you and your competitors, then:

1. Engineers numeric SEO features from the raw crawl data
2. Computes a **rule-based SEO Health Score (0–100)** using established on-page SEO best practices
3. Trains a `RandomForestRegressor` and `RandomForestClassifier` to learn and generalize that scoring logic from the features
4. Visualizes competitor comparisons, top/bottom performing pages, and feature importance in a Streamlit dashboard

## ✨ Features

- 📤 Upload any competitor crawl CSV — column names are auto-detected, no fixed schema required
- 📊 Domain-vs-domain SEO score comparison
- 🏆 Top 5 / Bottom 5 pages by SEO score
- 🤖 ML feature importance — see what actually drives SEO performance
- 📥 One-click CSV export of scored results
- 🧩 Modular codebase (`src/`) — swap in a different dataset without rewriting the pipeline

## 📊 Dataset

[SEO Crawl Datasets](https://www.kaggle.com/datasets/eliasdabbas/seocrawldatasets) — real crawled website data by Elias Dabbas, creator of the `advertools` Python SEO library.

> **Note:** column names vary across the files in this dataset (e.g. this project was tested on `django.csv`, which has no `meta_desc` column, so `has_meta_desc` scores 0 for every page — a genuine data limitation, not a bug). `word_count` is derived from the `body_text` field when no explicit word-count column exists. The loader (`src/data_loader.py`) auto-detects common column-name variants; if something isn't picked up, add the real header to `COLUMN_MAP` in `src/config.py`.

## 🛠️ Tech Stack

- Python, Pandas
- Scikit-learn (RandomForestRegressor, RandomForestClassifier)
- Streamlit (dashboard)
- Joblib (model persistence)

## 📁 Project Structure

competitor-seo-analysis-tool/
├── src/
│ ├── config.py # column mapping + scoring thresholds
│ ├── data_loader.py # loads CSV, auto-detects columns
│ ├── feature_engineering.py # builds numeric ML features
│ ├── seo_scorer.py # rule-based SEO score (training target)
│ └── train_model.py # trains + saves the models
├── app.py # Streamlit dashboard
├── generate_sample_data.py # synthetic data for quick testing
├── requirements.txt
├── .gitignore
└── data/ # put your crawl CSV here


## 🚀 Setup & Usage

1. **Clone the repo & install dependencies**
```bash
git clone https://github.com/fatima-890/Competitor-SEO-Analysis-Tool.git
cd Competitor-SEO-Analysis-Tool
pip install -r requirements.txt
```

2. **Get the data** — download the [Kaggle dataset](https://www.kaggle.com/datasets/eliasdabbas/seocrawldatasets), unzip, and place a CSV at `data/seo_crawl_data.csv`.

3. **Train the models**
```bash
   python -m src.train_model
```
   Prints MAE/R² for the score regressor, accuracy for the category classifier, and feature importances, then saves both models to `models/`.

4. **Launch the dashboard**
```bash
   python -m streamlit run app.py
```
   (Use `python -m streamlit run app.py`, not just `streamlit run app.py`, to avoid PATH issues on Windows.)

5. In the sidebar, click **"Use bundled sample data"** to load `data/seo_crawl_data.csv` directly from disk (no upload-size limits), or upload a different crawl CSV.

## 📈 Results

On the Django docs crawl dataset (35,463 pages, 3 domains):

- SEO Score Regressor: R² = 1.000, MAE = 0.01
- SEO Category Classifier: 100% accuracy
- Top predictive features: `title_length` (65.6%), `word_count` (33.1%)

> Since the target label (`seo_score`) is rule-derived from these same input features, near-perfect performance is expected — it confirms the model correctly learned the scoring logic rather than reflecting real-world unpredictability. On this dataset, every page fell into the "Average" or "Poor" category; none scored "Good," largely because no page had a meta description.

## 🔮 Possible Extensions

- Add real keyword-ranking data to correlate SEO score with actual search rankings
- NLP-based content/keyword-gap analysis between you and competitors
- Automated weekly re-crawl + score-trend tracking over time

## 🤝 Contributing

Contributions are welcome! If you'd like to improve this project:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/your-feature-name`)
3. Make your changes and commit (`git commit -m "Add: your feature"`)
4. Push to your branch (`git push origin feature/your-feature-name`)
5. Open a Pull Request describing what you changed and why

Bug reports and feature suggestions are also welcome via GitHub Issues.

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 👤 About Me

**Esha Fatima**
AI/ML student building a portfolio of machine learning and NLP projects, with a growing interest in the intersection of AI and SEO.

- GitHub: [@fatima-890](https://github.com/fatima-890)
- LinkedIn: [Esha Fatima] www.linkedin.com/in/esha-fatima-bba9423bb
- Check out my other projects: Search Intent Classifier, Meta Title Generator, Spam Detection System, Website Traffic Prediction, and more on my profile.

⭐ If you found this project useful, consider giving it a star!