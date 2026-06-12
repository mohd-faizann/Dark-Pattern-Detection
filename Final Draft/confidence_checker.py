"""Confidence evaluation layer — combines BERT output with rule-based features."""

from text_features import TextFeatureExtractor
from ui_features import UIFeatureExtractor


class BehaviourFeatureExtractor:
    """Placeholder behaviour signals (Phase 2: Playwright)."""

    def extract(self) -> dict:
        return {
            "clicks_to_accept": 1,
            "clicks_to_reject": 4,
        }


class ConfidenceEngine:
    def calculate_rule_score(self, features: dict) -> float:
        score = 0.0

        score += min(features.get("urgency_count", 0), 5) * 3
        score += min(features.get("scarcity_count", 0), 5) * 3
        score += min(features.get("confirmshaming_count", 0), 5) * 6
        score += min(features.get("fear_count", 0), 5) * 4
        score += min(features.get("hidden_fee_count", 0), 5) * 5

        score += min(features.get("popup_count", 0), 5) * 4
        score += min(features.get("prechecked_boxes", 0), 5) * 5
        score += min(features.get("misleading_buttons", 0), 5) * 3
        score += min(features.get("subscription_traps", 0), 5) * 4
        score += min(features.get("hidden_cancellation_paths", 0), 5) * 3

        if features.get("clicks_to_reject", 0) > features.get("clicks_to_accept", 0):
            score += 15

        return min(score, 100.0)

    def calculate_final_confidence(
        self, bert_probability: float, rule_score: float
    ) -> float:
        bert_pct = bert_probability * 100
        return round(0.70 * bert_pct + 0.30 * rule_score, 1)


class ExplanationEngine:
    def generate(self, features: dict, bert_probability: float) -> list[str]:
        reasons = []

        if features.get("urgency_count", 0) > 0:
            reasons.append("Urgency language detected")

        if features.get("scarcity_count", 0) > 0:
            reasons.append("Scarcity tactics detected")

        if features.get("confirmshaming_count", 0) > 0:
            reasons.append("Confirmshaming language detected")

        if features.get("fear_count", 0) > 0:
            reasons.append("Fear-based wording detected")

        if features.get("hidden_fee_count", 0) > 0:
            reasons.append("Hidden fee wording detected")

        if features.get("prechecked_boxes", 0) > 0:
            reasons.append("Pre-selected checkbox detected")

        if features.get("popup_count", 0) > 0:
            reasons.append("Popup behaviour detected")

        if features.get("misleading_buttons", 0) > 0:
            reasons.append("Misleading button labels detected")

        if features.get("subscription_traps", 0) > 0:
            reasons.append("Subscription trap indicators detected")

        if features.get("hidden_cancellation_paths", 0) > 0:
            reasons.append("Hidden cancellation path detected")

        if features.get("clicks_to_reject", 0) > features.get("clicks_to_accept", 0):
            reasons.append("Reject path harder than accept path")

        bert_pct = round(bert_probability * 100)
        if bert_probability >= 0.5:
            reasons.append(
                f"BERT predicted dark pattern with {bert_pct}% confidence"
            )
        elif bert_probability > 0:
            reasons.append(
                f"BERT dark-pattern probability is {bert_pct}%"
            )

        if not reasons:
            reasons.append("No strong dark pattern indicators detected")

        return reasons


class DarkPatternConfidenceChecker:
    def __init__(self):
        self.text_extractor = TextFeatureExtractor()
        self.ui_extractor = UIFeatureExtractor()
        self.behaviour_extractor = BehaviourFeatureExtractor()
        self.confidence_engine = ConfidenceEngine()
        self.explainer = ExplanationEngine()

    def analyze(
        self, text: str, html: str, bert_probability: float
    ) -> dict:
        features = {}
        features.update(self.text_extractor.extract(text))
        features.update(self.ui_extractor.extract(html))
        features.update(self.behaviour_extractor.extract())

        rule_score = self.confidence_engine.calculate_rule_score(features)
        confidence = self.confidence_engine.calculate_final_confidence(
            bert_probability, rule_score
        )
        reasons = self.explainer.generate(features, bert_probability)

        return {
            "confidence": confidence,
            "rule_score": round(rule_score, 1),
            "risk_level": self.get_risk_level(confidence),
            "features": features,
            "reasons": reasons,
        }

    @staticmethod
    def get_risk_level(score: float) -> str:
        if score >= 70:
            return "HIGH"
        if score >= 40:
            return "MEDIUM"
        return "LOW"
