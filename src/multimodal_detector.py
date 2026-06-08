from __future__ import annotations

from src.config import FUSION_WEIGHTS, RISK_BANDS
from src.explainability import build_explanations, reviewer_actions
from src.models.claim_model import ClaimVerificationModel
from src.models.image_model import ImageManipulationModel
from src.models.source_model import SourceReliabilityModel
from src.models.text_model import TextCredibilityModel
from src.schemas import NewsInput, PredictionResult
from src.utils import clamp


class MultiModalFakeNewsDetector:
    """Late-fusion detector combining NLP, CV, source, and claim signals."""

    def __init__(self) -> None:
        self.text_model = TextCredibilityModel()
        self.image_model = ImageManipulationModel()
        self.source_model = SourceReliabilityModel()
        self.claim_model = ClaimVerificationModel()

    def predict(self, item: NewsInput) -> PredictionResult:
        scores = [
            self.text_model.predict(item.headline, item.article),
            self.image_model.predict(item.image),
            self.source_model.predict(item.source),
            self.claim_model.predict(item.claim, item.article, item.evidence),
        ]

        weights_by_name = {
            "Text credibility": FUSION_WEIGHTS["text"],
            "Image manipulation": FUSION_WEIGHTS["image"],
            "Source reliability": FUSION_WEIGHTS["source"],
            "Claim verification": FUSION_WEIGHTS["claim"],
        }
        fake_probability = clamp(
            sum(score.fake_probability * weights_by_name[score.name] for score in scores)
        )
        confidence = clamp(
            sum(score.confidence * weights_by_name[score.name] for score in scores)
            + abs(fake_probability - 0.5) * 0.2
        )
        label = "Fake" if fake_probability >= 0.5 else "Real"
        risk_band = next(label for threshold, label in RISK_BANDS if fake_probability >= threshold)

        weighted_contributions = {
            score.name: (score.fake_probability - 0.5) * weights_by_name[score.name]
            for score in scores
        }

        return PredictionResult(
            label=label,
            fake_probability=fake_probability,
            confidence=confidence,
            risk_band=risk_band,
            modality_scores=scores,
            explanations=build_explanations(scores, weighted_contributions),
            reviewer_actions=reviewer_actions(fake_probability, scores),
        )
