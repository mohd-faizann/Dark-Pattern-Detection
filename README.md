# Dark Pattern Detection System

A BERT-based dark pattern detection system with a rule-based confidence evaluation layer. Scrapes webpages, runs ML classification, extracts handcrafted features, and returns an explainable risk report.

## Features

- **Web scraping** — fetches HTML and extracts visible text
- **BERT classifier** — predicts dark patterns with probability scores
- **Feature extraction** — urgency, scarcity, confirmshaming, UI traps, and more
- **Confidence engine** — combines BERT (70%) + rule score (30%)
- **Explainable output** — human-readable reasons for each risk level
- **Demo web UI** — analyze any URL from the browser

## Project Structure

```
Final Draft/
├── main.py                 # Entry point (CLI + web demo)
├── scrapper.py             # URL fetching and text extraction
├── predict.py              # BERT classifier
├── text_features.py        # Text-based dark pattern signals
├── ui_features.py          # HTML/UI-based signals
├── confidence_checker.py   # Confidence + explanation engine
├── templates/index.html    # Demo web interface
└── requirements.txt

BERT model/                 # Pre-trained BERT weights (Git LFS)
webscraper/                 # Scraper module wrapper
```

## Setup

```bash
cd "Final Draft"
pip install -r requirements.txt
```

> **Note:** The BERT model (`model.safetensors`) is stored via Git LFS. After cloning, run `git lfs pull` if the model file is missing.

## Usage

### Web demo (recommended)

```bash
python main.py --web
```

Open http://127.0.0.1:5000, enter a URL, and click **Analyze**.

### CLI

```bash
python main.py https://example.com
```

### Sample output

```json
{
  "url": "https://example.com",
  "bert_probability": 0.91,
  "confidence": 86.5,
  "risk_level": "HIGH",
  "features": {
    "urgency_count": 3,
    "scarcity_count": 2,
    "confirmshaming_count": 1,
    "popup_count": 2,
    "prechecked_boxes": 1
  },
  "reasons": [
    "Urgency language detected",
    "Scarcity tactics detected",
    "BERT predicted dark pattern with 91% confidence"
  ]
}
```

## Risk Levels

| Score  | Level  |
|--------|--------|
| 0–39   | LOW    |
| 40–69  | MEDIUM |
| 70–100 | HIGH   |

## Team

Final Year Project — 5-member development team.

## License

MIT License — see [LICENSE](LICENSE).
