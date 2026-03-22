#!/usr/bin/env python3
"""
Build deterministic bottleneck-role classifications from route review and handoff batches.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from app.services.bottleneck_role_classifier import build_bottleneck_role_classification_batch


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("route_review_surface_json")
    parser.add_argument("market_handoff_json")
    parser.add_argument("--output-json", required=True)
    args = parser.parse_args()

    route_review_surface = json.loads(Path(args.route_review_surface_json).read_text(encoding="utf-8"))
    market_handoff = json.loads(Path(args.market_handoff_json).read_text(encoding="utf-8"))
    output = build_bottleneck_role_classification_batch(route_review_surface, market_handoff)

    output_path = Path(args.output_json)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(output, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
