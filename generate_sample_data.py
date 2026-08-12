"""
generate_sample_data.py
-------------------------
Creates a small synthetic CSV that mimics the SEO Crawl Datasets
schema (from advertools crawls), so you can test the full pipeline
immediately -- BEFORE downloading the real Kaggle dataset.

Run:
    python generate_sample_data.py
"""

import random
import pandas as pd

random.seed(42)

domains = ["competitor-a.com", "competitor-b.com", "competitor-c.com", "yourbrand.com"]
titles = [
    "Best Running Shoes for 2026 | Buyer's Guide",
    "Top 10 Home Decor Ideas This Season",
    "Affordable Furniture Sale - Shop Now",
    "How to Choose Sports Merchandise",
    "Ultimate Guide",
    "Shop Deals Today Fast Shipping Free Returns Worldwide Everywhere",
]

rows = []
for i in range(300):
    domain = random.choice(domains)
    title = random.choice(titles)
    has_meta = random.random() > 0.15
    meta = ("Discover the best products with our expert guide, "
            "curated reviews, and unbeatable deals for every budget.") if has_meta else ""
    rows.append({
        "url": f"https://{domain}/page-{i}",
        "title": title,
        "meta_desc": meta,
        "h1": "Main Heading" if random.random() > 0.1 else "",
        "h2": "@@".join(["Section"] * random.randint(0, 4)),
        "word_count": random.choice([120, 350, 600, 900, 1500]),
        "status": 200,
        "download_latency": round(random.uniform(0.5, 5.5), 2),
        "links_url": "@@".join(["/link"] * random.randint(0, 8)),
        "img_src": "@@".join(["/img.jpg"] * random.randint(0, 6)),
    })

df = pd.DataFrame(rows)
df.to_csv("data/seo_crawl_data.csv", index=False)
print(f"Sample dataset written to data/seo_crawl_data.csv ({len(df)} rows)")