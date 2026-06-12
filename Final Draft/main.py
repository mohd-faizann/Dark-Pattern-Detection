"""Dark Pattern Detection System — main application entry point."""

import argparse
import json
import sys
from pathlib import Path

from confidence_checker import DarkPatternConfidenceChecker
from predict import predict
from scrapper import scrape


def analyze_url(url: str) -> dict:
    html, text = scrape(url)

    bert_result = predict(text)
    bert_probability = bert_result["bert_probability"]

    checker = DarkPatternConfidenceChecker()
    analysis = checker.analyze(text, html, bert_probability)

    report_features = {
        "urgency_count": analysis["features"].get("urgency_count", 0),
        "scarcity_count": analysis["features"].get("scarcity_count", 0),
        "confirmshaming_count": analysis["features"].get("confirmshaming_count", 0),
        "fear_count": analysis["features"].get("fear_count", 0),
        "hidden_fee_count": analysis["features"].get("hidden_fee_count", 0),
        "popup_count": analysis["features"].get("popup_count", 0),
        "prechecked_boxes": analysis["features"].get("prechecked_boxes", 0),
    }

    return {
        "url": url,
        "bert_probability": round(bert_probability, 4),
        "bert_class": bert_result["class"],
        "confidence": analysis["confidence"],
        "rule_score": analysis["rule_score"],
        "risk_level": analysis["risk_level"],
        "features": report_features,
        "reasons": analysis["reasons"],
        "text_preview": text[:500] + ("..." if len(text) > 500 else ""),
    }


def create_app():
    from flask import Flask, jsonify, render_template, request

    app = Flask(__name__)

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/analyze", methods=["POST"])
    def analyze():
        data = request.get_json(silent=True) or {}
        url = (data.get("url") or request.form.get("url", "")).strip()

        if not url:
            return jsonify({"error": "URL is required"}), 400

        try:
            result = analyze_url(url)
            return jsonify(result)
        except ValueError as exc:
            return jsonify({"error": str(exc)}), 400
        except ConnectionError as exc:
            return jsonify({"error": str(exc)}), 502
        except Exception as exc:
            return jsonify({"error": f"Analysis failed: {exc}"}), 500

    return app


def main():
    parser = argparse.ArgumentParser(
        description="Dark Pattern Detection System"
    )
    parser.add_argument("url", nargs="?", help="URL to analyze")
    parser.add_argument(
        "--web",
        action="store_true",
        help="Launch demo web interface",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=5000,
        help="Port for web demo (default: 5000)",
    )
    args = parser.parse_args()

    if args.web or not args.url:
        app = create_app()
        print(f"\n  Dark Pattern Detection System")
        print(f"  Demo UI: http://127.0.0.1:{args.port}\n")
        app.run(host="127.0.0.1", port=args.port, debug=False)
        return

    try:
        result = analyze_url(args.url)
        print(json.dumps(result, indent=2))
    except (ValueError, ConnectionError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
