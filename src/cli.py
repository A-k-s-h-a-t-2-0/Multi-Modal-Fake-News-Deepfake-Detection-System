from __future__ import annotations

import argparse
import json
from pathlib import Path

from src.multimodal_detector import MultiModalFakeNewsDetector
from src.schemas import NewsInput


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run multi-modal fake news detection.")
    parser.add_argument("--sample", type=Path, required=True, help="Path to JSON sample input.")
    parser.add_argument("--image", type=Path, default=None, help="Optional image path.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    payload = json.loads(args.sample.read_text(encoding="utf-8"))
    image = None
    if args.image:
        from PIL import Image

        image = Image.open(args.image).convert("RGB")
    detector = MultiModalFakeNewsDetector()
    result = detector.predict(
        NewsInput(
            headline=payload.get("headline", ""),
            article=payload.get("article", ""),
            source=payload.get("source", ""),
            claim=payload.get("claim", ""),
            evidence=payload.get("evidence", []),
            image=image,
        )
    )
    print(json.dumps(result.to_dict(), indent=2))


if __name__ == "__main__":
    main()
