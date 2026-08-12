"""
config.py
---------
Central place to map YOUR dataset's actual column names to the
standard names the rest of the code uses.

Kaggle SEO crawl exports (e.g. "SEO Crawl Datasets" by eliasdabbas,
built with the `advertools` crawler) can have slightly different
column names depending on which file you download. Instead of hard
-coding one schema, we auto-detect the closest match for each field
from a list of common variants. If auto-detection misses something,
just add the real column name to the matching list below.
"""

COLUMN_MAP = {
    "url": ["url", "address", "page_url", "link"],
    "domain": ["domain", "host", "site", "netloc"],
    "title": ["title", "page_title", "title_1"],
    "meta_desc": ["meta_desc", "meta_description", "description"],
    "h1": ["h1", "h1_1", "heading_1"],
    "h2": ["h2", "h2_1", "heading_2"],
    "word_count": ["word_count", "size_words", "content_word_count"],
    "body_text": ["body_text", "body", "content"],
    "status_code": ["status", "status_code", "response_code"],
    "load_time": ["download_latency", "load_time", "response_time",
                   "load_time_sec"],
    "size_bytes": ["size", "size_bytes", "response_size"],
    "img_src": ["img_src", "images", "image_count"],
    "links_url": ["links_url", "links", "internal_links"],
    "canonical": ["canonical", "canonical_url"],
}

THRESHOLDS = {
    "title_len_ideal": (50, 60),
    "title_len_ok": (30, 80),
    "meta_len_ideal": (150, 160),
    "word_count_good": 1000,
    "word_count_ok": 300,
    "load_time_good": 2.0,
    "load_time_ok": 4.0,
    "min_internal_links": 3,
}

RANDOM_STATE = 42