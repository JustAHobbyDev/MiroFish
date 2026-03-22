#!/usr/bin/env python3
"""
Build a narrowed bounded-entity follow-up queue from an exploratory lane.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from app.services.bounded_entity_lane_narrower import (
    build_bounded_entity_lane_narrowing_batch,
)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("entity_candidates_json")
    parser.add_argument("followup_queue_json")
    parser.add_argument("--output-json", required=True)
    args = parser.parse_args()

    entity_candidate_batch = json.loads(Path(args.entity_candidates_json).read_text(encoding="utf-8"))
    followup_queue_batch = json.loads(Path(args.followup_queue_json).read_text(encoding="utf-8"))

    output = build_bounded_entity_lane_narrowing_batch(
        entity_candidate_batch,
        followup_queue_batch,
    )

    output_path = Path(args.output_json)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(output, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
