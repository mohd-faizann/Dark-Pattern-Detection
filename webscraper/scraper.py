"""Web scraper module — fetches HTML and extracts visible text."""

import re
import sys
from pathlib import Path

import requests
from bs4 import BeautifulSoup

# Allow importing from Final Draft when run standalone
_FINAL_DRAFT = Path(__file__).resolve().parent.parent / "Final Draft"
if str(_FINAL_DRAFT) not in sys.path:
    sys.path.insert(0, str(_FINAL_DRAFT))

from scrapper import extract_text, fetch_html, scrape  # noqa: E402

__all__ = ["fetch_html", "extract_text", "scrape"]
