#!/usr/bin/env python3
"""
Build a consolidated multi-lane review surface from route-aware priority batches.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from app.services.bounded_entity_route_review_surface_builder import (
    build_bounded_entity_route_review_surface,
)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("route_priority_json", nargs="+")
    parser.add_argument("--output-json", required=True)
    args = parser.parse_args()

    route_priority_batches = [
        json.loads(Path(path).read_text(encoding="utf-8")) for path in args.route_priority_json
    ]
    output = build_bounded_entity_route_review_surface(route_priority_batches)

    output_path = Path(args.output_json)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(output, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
