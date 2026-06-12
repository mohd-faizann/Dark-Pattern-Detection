"""Quick end-to-end pipeline test using built-in sample data."""

from confidence_checker import DarkPatternConfidenceChecker
from predict import predict

SAMPLE_TEXT = """
Hurry! Limited time offer.
Only 2 seats left.
No thanks, I don't want savings.
Additional fee may apply.
"""

SAMPLE_HTML = """
<html>
<body>
<div class="popup">Offer Ends Soon</div>
<input type="checkbox" checked>
<button>Continue</button>
<p>Subscribe now for a free trial with auto-renew.</p>
</body>
</html>
"""


def main():
    bert_result = predict(SAMPLE_TEXT)
    checker = DarkPatternConfidenceChecker()
    result = checker.analyze(
        SAMPLE_TEXT, SAMPLE_HTML, bert_result["bert_probability"]
    )

    print("BERT:", bert_result)
    print("Analysis:", result)
    assert result["risk_level"] in ("LOW", "MEDIUM", "HIGH")
    assert result["confidence"] >= 0
    assert len(result["reasons"]) > 0
    print("\nAll checks passed.")


if __name__ == "__main__":
    main()
