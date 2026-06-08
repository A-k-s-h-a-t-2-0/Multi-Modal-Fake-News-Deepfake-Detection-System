from __future__ import annotations

import math
import re
from collections import Counter


WORD_PATTERN = re.compile(r"[a-zA-Z][a-zA-Z'-]+")


def clamp(value: float, low: float = 0.0, high: float = 1.0) -> float:
    return max(low, min(high, value))


def sigmoid(value: float) -> float:
    return 1.0 / (1.0 + math.exp(-value))


def tokenize(text: str) -> list[str]:
    return [match.group(0).lower() for match in WORD_PATTERN.finditer(text or "")]


def keyword_hits(text: str, terms: set[str]) -> list[str]:
    lowered = (text or "").lower()
    return sorted(term for term in terms if term in lowered)


def cosine_similarity(left: str, right: str) -> float:
    left_tokens = tokenize(left)
    right_tokens = tokenize(right)
    if not left_tokens or not right_tokens:
        return 0.0

    left_counts = Counter(left_tokens)
    right_counts = Counter(right_tokens)
    shared = set(left_counts) & set(right_counts)
    numerator = sum(left_counts[token] * right_counts[token] for token in shared)
    left_norm = math.sqrt(sum(count * count for count in left_counts.values()))
    right_norm = math.sqrt(sum(count * count for count in right_counts.values()))
    if left_norm == 0 or right_norm == 0:
        return 0.0
    return numerator / (left_norm * right_norm)
