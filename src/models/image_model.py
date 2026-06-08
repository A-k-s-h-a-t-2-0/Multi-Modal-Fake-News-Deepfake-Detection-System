from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from PIL import Image

from src.schemas import ModalityScore
from src.utils import clamp


class ImageManipulationModel:
    """Computer-vision baseline for manipulation artifacts."""

    def predict(self, image: "Image.Image | None") -> ModalityScore:
        if image is None:
            return ModalityScore(
                "Image manipulation",
                0.5,
                0.45,
                ["no image was supplied"],
            )

        import cv2
        import numpy as np

        rgb = np.asarray(image.convert("RGB").resize((384, 384)))
        gray = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)
        laplacian_var = float(cv2.Laplacian(gray, cv2.CV_64F).var())
        edges = cv2.Canny(gray, 80, 180)
        edge_density = float(np.mean(edges > 0))
        color_std = float(np.std(rgb) / 255.0)
        saturation = cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV)[:, :, 1]
        saturation_mean = float(np.mean(saturation) / 255.0)
        jpeg_blocks = self._blockiness(gray)

        score = 0.0
        signals: list[str] = []

        if laplacian_var < 45:
            score += 0.2
            signals.append("image is unusually blurry")
        if edge_density > 0.2:
            score += 0.16
            signals.append("image has dense high-frequency edges")
        if color_std < 0.14:
            score += 0.12
            signals.append("image has low color variation")
        if saturation_mean > 0.72:
            score += 0.12
            signals.append("image has unusually high saturation")
        if jpeg_blocks > 0.018:
            score += 0.2
            signals.append("possible compression/blocking artifacts detected")

        fake_probability = clamp(0.38 + score)
        confidence = clamp(0.5 + abs(fake_probability - 0.5) * 0.8)
        if not signals:
            signals.append("baseline image checks found no strong manipulation artifacts")

        return ModalityScore("Image manipulation", fake_probability, confidence, signals)

    @staticmethod
    def _blockiness(gray: np.ndarray) -> float:
        vertical = np.abs(np.diff(gray[:, 7::8].astype(np.float32), axis=1)).mean()
        horizontal = np.abs(np.diff(gray[7::8, :].astype(np.float32), axis=0)).mean()
        return float((vertical + horizontal) / (2 * 255.0))
