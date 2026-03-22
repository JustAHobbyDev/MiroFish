#!/usr/bin/env python3
"""
Build route-aware support rows for a bounded entity follow-up queue.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from app.services.bounded_entity_route_support import (
    build_bounded_entity_route_support_batch,
)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("followup_queue_json")
    parser.add_argument("public_support_json")
    parser.add_argument("private_plan_json")
    parser.add_argument("private_evidence_json")
    parser.add_argument("--output-json", required=True)
    args = parser.parse_args()

    followup_queue_batch = json.loads(Path(args.followup_queue_json).read_text(encoding="utf-8"))
    public_support_batch = json.loads(Path(args.public_support_json).read_text(encoding="utf-8"))
    private_plan_batch = json.loads(Path(args.private_plan_json).read_text(encoding="utf-8"))
    private_evidence_batch = json.loads(Path(args.private_evidence_json).read_text(encoding="utf-8"))

    output = build_bounded_entity_route_support_batch(
        followup_queue_batch,
        public_support_batch,
        private_plan_batch,
        private_evidence_batch,
    )

    output_path = Path(args.output_json)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(output, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
