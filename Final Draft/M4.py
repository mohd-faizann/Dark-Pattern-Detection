from bs4 import BeautifulSoup
import re
# main.py

from scraper import fetch_html, extract_text

# ==========================
# TEXT FEATURE EXTRACTION
# ==========================

class TextFeatureExtractor:

    URGENCY = [
        "hurry",
        "limited time",
        "act now",
        "expires soon",
        "offer ends"
    ]

    SCARCITY = [
        "only",
        "few left",
        "selling fast",
        "last chance"
    ]

    CONFIRMSHAMING = [
        "no thanks",
        "i don't want savings",
        "i prefer paying more"
    ]

    def extract(self, text):

        text = text.lower()

        return {

            "urgency_count":
                sum(text.count(x) for x in self.URGENCY),

            "scarcity_count":
                sum(text.count(x) for x in self.SCARCITY),

            "confirmshaming_count":
                sum(text.count(x) for x in self.CONFIRMSHAMING),

            "hidden_fee_count":
                len(re.findall(
                    r"additional fee|extra charge|processing fee",
                    text
                ))
        }


# ==========================
# UI FEATURE EXTRACTION
# ==========================

class UIFeatureExtractor:

    def extract(self, html):

        soup = BeautifulSoup(html, "html.parser")

        popups = soup.find_all(
            class_=lambda c:
            c and "popup" in str(c).lower()
        )

        checkboxes = soup.find_all(
            "input",
            {"type": "checkbox"}
        )

        prechecked = [
            box for box in checkboxes
            if box.has_attr("checked")
        ]

        return {

            "popup_count":
                len(popups),

            "prechecked_boxes":
                len(prechecked),

            # placeholders
            "button_size_ratio": 1.0,

            "contrast_ratio": 1.0
        }


# ==========================
# BEHAVIOURAL FEATURES
# ==========================

class BehaviourFeatureExtractor:

    def extract(self):

        # replace later with Playwright/Selenium

        return {

            "clicks_to_accept": 1,

            "clicks_to_reject": 4
        }


# ==========================
# CONFIDENCE ENGINE
# ==========================

class ConfidenceEngine:

    def calculate(self, features):

        score = 0

        score += min(features["urgency_count"], 5) * 3
        score += min(features["scarcity_count"], 5) * 3
        score += min(features["confirmshaming_count"], 5) * 6
        score += min(features["hidden_fee_count"], 5) * 5

        score += min(features["popup_count"], 5) * 4
        score += min(features["prechecked_boxes"], 5) * 5

        if features["clicks_to_reject"] > \
           features["clicks_to_accept"]:

            score += 15

        return min(score, 100)


# ==========================
# EXPLANATION GENERATOR
# ==========================

class ExplanationEngine:

    def generate(self, features):

        reasons = []

        if features["urgency_count"] > 0:
            reasons.append(
                "Urgency language detected"
            )

        if features["scarcity_count"] > 0:
            reasons.append(
                "Scarcity tactics detected"
            )

        if features["confirmshaming_count"] > 0:
            reasons.append(
                "Confirmshaming language detected"
            )

        if features["prechecked_boxes"] > 0:
            reasons.append(
                "Pre-selected checkbox found"
            )

        if features["popup_count"] > 0:
            reasons.append(
                "Popup behaviour detected"
            )

        if features["clicks_to_reject"] > \
           features["clicks_to_accept"]:

            reasons.append(
                "Reject path harder than accept path"
            )

        return reasons


# ==========================
# MAIN PIPELINE
# ==========================

class DarkPatternConfidenceChecker:

    def __init__(self):

        self.text_extractor = TextFeatureExtractor()

        self.ui_extractor = UIFeatureExtractor()

        self.behaviour_extractor = BehaviourFeatureExtractor()

        self.confidence_engine = ConfidenceEngine()

        self.explainer = ExplanationEngine()

    def analyze(self, text, html):

        features = {}

        features.update(
            self.text_extractor.extract(text)
        )

        features.update(
            self.ui_extractor.extract(html)
        )

        features.update(
            self.behaviour_extractor.extract()
        )

        confidence = \
            self.confidence_engine.calculate(
                features
            )

        reasons = \
            self.explainer.generate(
                features
            )

        return {

            "confidence": confidence,

            "risk_level":
                self.get_risk(confidence),

            "features": features,

            "reasons": reasons
        }

    def get_risk(self, score):

        if score >= 80:
            return "HIGH"

        elif score >= 50:
            return "MEDIUM"

        return "LOW"


# ==========================
# EXAMPLE
# ==========================

if __name__ == "__main__":

    text = """
    Hurry! Limited time offer.
    Only 2 seats left.
    No thanks, I don't want savings.
    """

    html = """
    <div class='popup'>
        Offer Ends Soon
    </div>

    <input
        type='checkbox'
        checked>
    """

    checker = \
        DarkPatternConfidenceChecker()

    result = checker.analyze(
        text,
        html
    )

    print(result)