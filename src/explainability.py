from __future__ import annotations

from src.schemas import ModalityScore


def build_explanations(
    scores: list[ModalityScore],
    weighted_contributions: dict[str, float],
) -> list[str]:
    explanations: list[str] = []
    ranked = sorted(
        scores,
        key=lambda score: abs(weighted_contributions[score.name]),
        reverse=True,
    )

    for score in ranked:
        if abs(score.fake_probability - 0.5) < 0.03:
            direction = "had a neutral effect on"
        else:
            direction = "increased" if score.fake_probability > 0.5 else "reduced"
        explanations.append(
            f"{score.name} {direction} the fake-news score: {score.signals[0]}."
        )

    explanations.append(
        "Fusion used weighted late ensembling across text, image, source, and claim modules."
    )
    return explanations


def reviewer_actions(fake_probability: float, scores: list[ModalityScore]) -> list[str]:
    actions = []
    if fake_probability >= 0.6:
        actions.append("Send to manual fact-checking before publication or sharing.")
    else:
        actions.append("Prediction is lower risk, but verify high-impact claims independently.")

    score_map = {score.name: score for score in scores}
    if score_map["Claim verification"].fake_probability > 0.55:
        actions.append("Gather stronger trusted evidence for the primary claim.")
    if score_map["Image manipulation"].fake_probability > 0.55:
        actions.append("Run a dedicated deepfake/image-forensics model on the media asset.")
    if score_map["Source reliability"].fake_probability > 0.55:
        actions.append("Check publisher history, ownership, and prior fact-check records.")

    return actions
