from __future__ import annotations

from src.config import CLICKBAIT_TERMS, MISINFORMATION_CUES
from src.schemas import ModalityScore
from src.utils import clamp, keyword_hits, sigmoid, tokenize


class TextCredibilityModel:
    """Transparent baseline NLP model with a transformer-ready interface."""

    def predict(self, headline: str, article: str) -> ModalityScore:
        full_text = f"{headline}\n{article}".strip()
        tokens = tokenize(full_text)
        token_count = len(tokens)
        unique_ratio = len(set(tokens)) / max(token_count, 1)
        uppercase_ratio = sum(1 for char in headline if char.isupper()) / max(len(headline), 1)
        exclamation_count = full_text.count("!")
        question_count = full_text.count("?")
        clickbait_hits = keyword_hits(full_text, CLICKBAIT_TERMS)
        misinformation_hits = keyword_hits(full_text, MISINFORMATION_CUES)

        score = -0.65
        score += min(len(clickbait_hits), 5) * 0.35
        score += min(len(misinformation_hits), 5) * 0.48
        score += min(exclamation_count, 4) * 0.18
        score += min(question_count, 3) * 0.08
        score += 0.45 if uppercase_ratio > 0.22 and len(headline) > 12 else 0
        score += 0.28 if token_count < 80 else 0
        score -= 0.18 if token_count > 250 else 0
        score -= 0.22 if unique_ratio > 0.48 and token_count > 120 else 0

        fake_probability = clamp(sigmoid(score))
        confidence = clamp(0.55 + abs(fake_probability - 0.5) * 0.75)
        signals = []
        if clickbait_hits:
            signals.append(f"clickbait terms: {', '.join(clickbait_hits[:4])}")
        if misinformation_hits:
            signals.append(f"misinformation cues: {', '.join(misinformation_hits[:4])}")
        if uppercase_ratio > 0.22:
            signals.append("headline uses unusually high capitalization")
        if token_count < 80:
            signals.append("article is very short for a news report")
        if not signals:
            signals.append("text has limited sensational or manipulative language")

        return ModalityScore("Text credibility", fake_probability, confidence, signals)
