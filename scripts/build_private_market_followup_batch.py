#!/usr/bin/env python3
"""
Build a deterministic private-market follow-up batch from market handoff rows.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from app.services.private_market_followup_builder import build_private_market_followup_batch


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("market_handoff_json")
    parser.add_argument("--output-json", required=True)
    args = parser.parse_args()

    handoff_batch = json.loads(Path(args.market_handoff_json).read_text(encoding="utf-8"))
    output = build_private_market_followup_batch(handoff_batch)

    output_path = Path(args.output_json)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(output, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
