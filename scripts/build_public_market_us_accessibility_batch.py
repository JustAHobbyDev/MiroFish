#!/usr/bin/env python3
"""
Build a deterministic U.S.-accessibility layer for public market picks.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from app.services.public_market_us_accessibility_builder import (
    build_public_market_us_accessibility_batch,
)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("public_market_pick_json")
    parser.add_argument("public_market_scan_candidate_json")
    parser.add_argument("--symbol-mapping-json", action="append", default=[])
    parser.add_argument("--output-json", required=True)
    args = parser.parse_args()

    pick_batch = json.loads(Path(args.public_market_pick_json).read_text(encoding="utf-8"))
    candidate_batch = json.loads(Path(args.public_market_scan_candidate_json).read_text(encoding="utf-8"))
    symbol_mapping_batches = [
        json.loads(Path(path).read_text(encoding="utf-8")) for path in args.symbol_mapping_json
    ]
    output = build_public_market_us_accessibility_batch(
        pick_batch,
        candidate_batch,
        symbol_mapping_batches,
    )

    output_path = Path(args.output_json)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(output, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
