"""BERT classifier — returns class label and probability."""

from pathlib import Path

import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer

MODEL_DIR = Path(__file__).resolve().parent.parent / "BERT model"
DARK_PATTERN_LABEL = 1
LABEL_NAMES = {0: "NotDarkPattern", 1: "DarkPattern"}


class BertPredictor:
    def __init__(self, model_dir: Path | None = None):
        model_path = model_dir or MODEL_DIR
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_path)
        self.model.eval()

    def predict(self, text: str) -> dict:
        if not text or not text.strip():
            return {
                "class": "NotDarkPattern",
                "probability": 0.0,
                "bert_probability": 0.0,
            }

        inputs = self.tokenizer(
            text,
            return_tensors="pt",
            truncation=True,
            max_length=512,
            padding=True,
        )

        with torch.no_grad():
            logits = self.model(**inputs).logits
            probabilities = torch.softmax(logits, dim=1)[0]

        predicted_id = int(probabilities.argmax().item())
        dark_pattern_prob = float(probabilities[DARK_PATTERN_LABEL].item())

        return {
            "class": LABEL_NAMES.get(predicted_id, f"LABEL_{predicted_id}"),
            "probability": dark_pattern_prob,
            "bert_probability": dark_pattern_prob,
        }


_predictor: BertPredictor | None = None


def get_predictor() -> BertPredictor:
    global _predictor
    if _predictor is None:
        _predictor = BertPredictor()
    return _predictor


def predict(text: str) -> dict:
    """Run BERT inference and return class + dark-pattern probability."""
    return get_predictor().predict(text)
