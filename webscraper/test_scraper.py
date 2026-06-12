"""Basic scraper tests."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "Final Draft"))

from scrapper import extract_text, scrape


def test_extract_text():
    html = "<html><body><p>Hello World</p><script>ignore</script></body></html>"
    text = extract_text(html)
    assert "Hello World" in text
    assert "ignore" not in text


def test_scrape_returns_tuple():
    html, text = scrape("https://example.com")
    assert isinstance(html, str) and len(html) > 0
    assert isinstance(text, str) and len(text) > 0
