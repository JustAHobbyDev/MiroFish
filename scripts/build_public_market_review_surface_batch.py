#!/usr/bin/env python3
"""
Build a combined public market review surface.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from app.services.public_market_review_surface_builder import (
    build_public_market_review_surface,
)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("public_market_pick_json")
    parser.add_argument("public_market_pick_assessment_json")
    parser.add_argument("public_market_us_accessibility_json")
    parser.add_argument("public_market_foreign_access_followup_json")
    parser.add_argument("--output-json", required=True)
    args = parser.parse_args()

    output = build_public_market_review_surface(
        json.loads(Path(args.public_market_pick_json).read_text(encoding="utf-8")),
        json.loads(Path(args.public_market_pick_assessment_json).read_text(encoding="utf-8")),
        json.loads(Path(args.public_market_us_accessibility_json).read_text(encoding="utf-8")),
        json.loads(Path(args.public_market_foreign_access_followup_json).read_text(encoding="utf-8")),
    )

    output_path = Path(args.output_json)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(output, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
