from __future__ import annotations

from src.schemas import ModalityScore
from src.utils import clamp, cosine_similarity


class ClaimVerificationModel:
    """Lightweight retrieval-style claim verifier."""

    def predict(self, claim: str, article: str, evidence: list[str]) -> ModalityScore:
        query = claim or article[:400]
        if not query.strip():
            return ModalityScore(
                "Claim verification",
                0.55,
                0.5,
                ["no claim text was provided for verification"],
            )

        similarities = [cosine_similarity(query, item) for item in evidence]
        best_similarity = max(similarities, default=0.0)
        fake_probability = clamp(0.68 - best_similarity * 0.75)
        confidence = clamp(0.5 + abs(fake_probability - 0.5) * 0.7)

        signals = []
        if not evidence:
            signals.append("no trusted evidence snippets were supplied")
            fake_probability = max(fake_probability, 0.58)
        elif best_similarity > 0.45:
            signals.append(f"claim overlaps with trusted evidence ({best_similarity:.2f} similarity)")
        elif best_similarity > 0.2:
            signals.append(f"claim has partial evidence overlap ({best_similarity:.2f} similarity)")
        else:
            signals.append("claim has weak overlap with supplied trusted evidence")

        return ModalityScore("Claim verification", fake_probability, confidence, signals)
