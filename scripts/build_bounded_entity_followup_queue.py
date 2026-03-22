#!/usr/bin/env python3
"""
Build a bounded entity follow-up queue from bounded entity candidates and filing support.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from app.services.bounded_entity_followup_queue import build_bounded_entity_followup_queue


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("bounded_entity_candidates_json", help="Path to bounded entity candidate batch JSON.")
    parser.add_argument("filing_support_json", help="Path to filing support batch JSON.")
    parser.add_argument("--system-label", required=True, help="System label to filter for.")
    parser.add_argument(
        "--entity-role",
        dest="entity_roles",
        action="append",
        required=True,
        help="Allowed entity role. Repeat for multiple roles.",
    )
    parser.add_argument("--output-json", required=True, help="Path to write the follow-up queue JSON.")
    args = parser.parse_args()

    candidate_batch = json.loads(Path(args.bounded_entity_candidates_json).read_text(encoding="utf-8"))
    filing_support_batch = json.loads(Path(args.filing_support_json).read_text(encoding="utf-8"))
    output = build_bounded_entity_followup_queue(
        candidate_batch,
        filing_support_batch,
        system_label=args.system_label,
        allowed_entity_roles=args.entity_roles,
    )

    output_path = Path(args.output_json)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(output, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
