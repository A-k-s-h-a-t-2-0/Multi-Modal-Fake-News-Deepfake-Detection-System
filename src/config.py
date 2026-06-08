from __future__ import annotations


FUSION_WEIGHTS = {
    "text": 0.36,
    "image": 0.24,
    "source": 0.18,
    "claim": 0.22,
}

RISK_BANDS = (
    (0.75, "Critical"),
    (0.6, "High"),
    (0.4, "Medium"),
    (0.0, "Low"),
)

CLICKBAIT_TERMS = {
    "shocking",
    "unbelievable",
    "secret",
    "exposed",
    "miracle",
    "you won't believe",
    "breaking",
    "viral",
    "banned",
    "hidden truth",
}

MISINFORMATION_CUES = {
    "doctors hate",
    "government does not want you to know",
    "100% guaranteed",
    "no evidence",
    "anonymous sources",
    "deep state",
    "hoax",
    "crisis actor",
    "secret cure",
}

TRUSTED_SOURCE_HINTS = {
    "reuters",
    "apnews",
    "associatedpress",
    "bbc",
    "nature",
    "science.org",
    "who.int",
    "cdc.gov",
    "nih.gov",
    "thehindu",
}

UNRELIABLE_SOURCE_HINTS = {
    "viral",
    "truth",
    "patriot",
    "rumor",
    "click",
    "now8",
    "dailybuzz",
    "unknown",
    "conspiracy",
}
