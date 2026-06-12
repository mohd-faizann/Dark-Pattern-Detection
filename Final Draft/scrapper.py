"""Web scraper module — fetches HTML and extracts visible text."""

import re
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}

REQUEST_TIMEOUT = 15


def _normalize_url(url: str) -> str:
    url = url.strip()
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    return url


def fetch_html(url: str) -> str:
    """Fetch page HTML, following redirects and handling network errors."""
    url = _normalize_url(url)
    parsed = urlparse(url)
    if not parsed.netloc:
        raise ValueError(f"Invalid URL: {url}")

    try:
        response = requests.get(
            url,
            headers=DEFAULT_HEADERS,
            timeout=REQUEST_TIMEOUT,
            allow_redirects=True,
        )
        response.raise_for_status()
    except requests.exceptions.Timeout as exc:
        raise ConnectionError(f"Request timed out for {url}") from exc
    except requests.exceptions.ConnectionError as exc:
        raise ConnectionError(f"Could not connect to {url}") from exc
    except requests.exceptions.HTTPError as exc:
        raise ConnectionError(
            f"HTTP {response.status_code} for {url}"
        ) from exc
    except requests.exceptions.RequestException as exc:
        raise ConnectionError(f"Failed to fetch {url}: {exc}") from exc

    response.encoding = response.apparent_encoding or "utf-8"
    return response.text


def extract_text(html: str) -> str:
    """Extract visible text from HTML, stripping scripts and styles."""
    soup = BeautifulSoup(html, "lxml")

    for tag in soup(["script", "style", "noscript", "svg", "meta", "link"]):
        tag.decompose()

    text = soup.get_text(separator=" ", strip=True)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def scrape(url: str) -> tuple[str, str]:
    """Download a page and return (html, visible_text)."""
    html = fetch_html(url)
    text = extract_text(html)
    return html, text
