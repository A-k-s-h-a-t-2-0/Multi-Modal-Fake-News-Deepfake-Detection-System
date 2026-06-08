from __future__ import annotations

from urllib.parse import urlparse

from src.config import TRUSTED_SOURCE_HINTS, UNRELIABLE_SOURCE_HINTS
from src.schemas import ModalityScore
from src.utils import clamp


class SourceReliabilityModel:
    """Publisher/domain reliability estimator."""

    def predict(self, source: str) -> ModalityScore:
        normalized = self._normalize(source)
        signals: list[str] = []
        fake_probability = 0.48

        if not normalized:
            signals.append("source is missing")
            fake_probability += 0.22
        if any(hint in normalized for hint in TRUSTED_SOURCE_HINTS):
            signals.append("source resembles a known high-reliability publisher")
            fake_probability -= 0.32
        if any(hint in normalized for hint in UNRELIABLE_SOURCE_HINTS):
            signals.append("source contains low-reliability naming patterns")
            fake_probability += 0.24
        if normalized.endswith(".gov") or normalized.endswith(".edu"):
            signals.append("source has institutional domain suffix")
            fake_probability -= 0.16
        if normalized and "." not in normalized:
            signals.append("source does not look like a complete domain")
            fake_probability += 0.12
        if not signals:
            signals.append("source has no strong reliability prior in the baseline model")

        fake_probability = clamp(fake_probability)
        confidence = clamp(0.52 + abs(fake_probability - 0.5) * 0.8)
        return ModalityScore("Source reliability", fake_probability, confidence, signals)

    @staticmethod
    def _normalize(source: str) -> str:
        source = (source or "").strip().lower()
        if not source:
            return ""
        parsed = urlparse(source if "://" in source else f"https://{source}")
        return parsed.netloc.replace("www.", "") or source.replace("www.", "")
