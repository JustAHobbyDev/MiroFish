#!/usr/bin/env python3
"""
Build route-aware priority rows for a bounded entity follow-up queue.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from app.services.bounded_entity_route_priority import (
    build_bounded_entity_route_priority_batch,
)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("route_support_json")
    parser.add_argument("--output-json", required=True)
    args = parser.parse_args()

    route_support_batch = json.loads(Path(args.route_support_json).read_text(encoding="utf-8"))
    output = build_bounded_entity_route_priority_batch(route_support_batch)

    output_path = Path(args.output_json)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(output, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
