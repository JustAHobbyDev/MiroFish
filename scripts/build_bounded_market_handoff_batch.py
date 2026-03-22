#!/usr/bin/env python3
"""
Build a deterministic bounded market handoff batch from a route-backed review surface.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from app.services.bounded_market_handoff_builder import build_bounded_market_handoff_batch


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("review_surface_json")
    parser.add_argument("--output-json", required=True)
    args = parser.parse_args()

    review_surface_batch = json.loads(Path(args.review_surface_json).read_text(encoding="utf-8"))
    output = build_bounded_market_handoff_batch(review_surface_batch)

    output_path = Path(args.output_json)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(output, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
