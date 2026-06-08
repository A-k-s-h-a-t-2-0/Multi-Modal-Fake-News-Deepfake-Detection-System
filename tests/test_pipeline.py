from __future__ import annotations

from src.multimodal_detector import MultiModalFakeNewsDetector
from src.schemas import NewsInput


def test_detector_returns_complete_prediction() -> None:
    detector = MultiModalFakeNewsDetector()
    result = detector.predict(
        NewsInput(
            headline="SHOCKING secret cure exposed",
            article="Anonymous sources claim a secret cure exists with no peer-reviewed evidence.",
            source="unknownviralnews.example",
            claim="A secret cure exists.",
            evidence=["Peer-reviewed medical claims require transparent clinical evidence."],
        )
    )

    assert result.label in {"Fake", "Real"}
    assert 0 <= result.fake_probability <= 1
    assert 0 <= result.confidence <= 1
    assert len(result.modality_scores) == 4
    assert result.explanations
