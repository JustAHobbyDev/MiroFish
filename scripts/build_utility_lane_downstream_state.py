#!/usr/bin/env python3
"""
Build consolidated utility-lane downstream state.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from app.services.utility_lane_downstream_state_builder import build_utility_lane_downstream_state


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("followup_queue_json", help="Path to utility follow-up queue JSON.")
    parser.add_argument("filing_support_json", help="Path to filing support JSON.")
    parser.add_argument("private_diligence_json", help="Path to private diligence plan JSON.")
    parser.add_argument("--output-json", required=True, help="Path to write the downstream state JSON.")
    args = parser.parse_args()

    queue_batch = json.loads(Path(args.followup_queue_json).read_text(encoding="utf-8"))
    filing_support_batch = json.loads(Path(args.filing_support_json).read_text(encoding="utf-8"))
    private_diligence_batch = json.loads(Path(args.private_diligence_json).read_text(encoding="utf-8"))
    output = build_utility_lane_downstream_state(
        queue_batch,
        filing_support_batch,
        private_diligence_batch,
    )

    output_path = Path(args.output_json)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(output, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
