#!/usr/bin/env python3
"""
Build the live issuer-resolution batch for the narrowed backup-power lane.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from app.services.backup_power_live_resolution_builder import (
    build_backup_power_live_resolution_batch,
)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("followup_queue_json", help="Path to backup-power follow-up queue JSON.")
    parser.add_argument("--output-json", required=True, help="Path to write the live-resolution JSON.")
    args = parser.parse_args()

    followup_queue_batch = json.loads(Path(args.followup_queue_json).read_text(encoding="utf-8"))
    output = build_backup_power_live_resolution_batch(followup_queue_batch)

    output_path = Path(args.output_json)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(output, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
