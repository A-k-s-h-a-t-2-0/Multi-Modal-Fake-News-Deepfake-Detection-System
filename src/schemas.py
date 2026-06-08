from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    import pandas as pd
    from PIL import Image


@dataclass
class NewsInput:
    headline: str
    article: str
    source: str = ""
    claim: str = ""
    evidence: list[str] = field(default_factory=list)
    image: "Image.Image | None" = None


@dataclass
class ModalityScore:
    name: str
    fake_probability: float
    confidence: float
    signals: list[str]


@dataclass
class PredictionResult:
    label: str
    fake_probability: float
    confidence: float
    risk_band: str
    modality_scores: list[ModalityScore]
    explanations: list[str]
    reviewer_actions: list[str]

    def to_score_frame(self) -> "pd.DataFrame":
        import pandas as pd

        return pd.DataFrame(
            [
                {
                    "Modality": score.name,
                    "Fake probability": f"{score.fake_probability:.1%}",
                    "Confidence": f"{score.confidence:.1%}",
                    "Top signals": "; ".join(score.signals[:3]),
                }
                for score in self.modality_scores
            ]
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "label": self.label,
            "fake_probability": round(self.fake_probability, 4),
            "confidence": round(self.confidence, 4),
            "risk_band": self.risk_band,
            "modality_scores": [
                {
                    "name": score.name,
                    "fake_probability": round(score.fake_probability, 4),
                    "confidence": round(score.confidence, 4),
                    "signals": score.signals,
                }
                for score in self.modality_scores
            ],
            "explanations": self.explanations,
            "reviewer_actions": self.reviewer_actions,
        }
