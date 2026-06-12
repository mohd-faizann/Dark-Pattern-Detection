"""Dictionary-driven text feature extraction for dark pattern signals."""

import re


class TextFeatureExtractor:
    URGENCY = [
        "hurry",
        "limited time",
        "act now",
        "expires soon",
        "offer ends",
        "don't miss",
        "today only",
        "ends tonight",
    ]

    SCARCITY = [
        "only",
        "few left",
        "selling fast",
        "last chance",
        "almost gone",
        "limited stock",
        "while supplies last",
    ]

    CONFIRMSHAMING = [
        "no thanks",
        "i don't want savings",
        "i prefer paying more",
        "no, i hate saving",
        "i'll pay full price",
    ]

    FEAR = [
        "you will miss out",
        "don't lose",
        "risk missing",
        "before it's too late",
        "you may regret",
        "warning",
    ]

    HIDDEN_FEE_PATTERNS = [
        r"additional fee",
        r"extra charge",
        r"processing fee",
        r"service fee",
        r"hidden fee",
        r"convenience fee",
    ]

    def extract(self, text: str) -> dict:
        text = text.lower()

        return {
            "urgency_count": sum(text.count(phrase) for phrase in self.URGENCY),
            "scarcity_count": sum(text.count(phrase) for phrase in self.SCARCITY),
            "confirmshaming_count": sum(
                text.count(phrase) for phrase in self.CONFIRMSHAMING
            ),
            "fear_count": sum(text.count(phrase) for phrase in self.FEAR),
            "hidden_fee_count": sum(
                len(re.findall(pattern, text))
                for pattern in self.HIDDEN_FEE_PATTERNS
            ),
        }
