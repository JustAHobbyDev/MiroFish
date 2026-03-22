#!/usr/bin/env python3
"""
Build a deterministic public-market symbol mapping batch from market handoff rows.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from app.services.public_market_symbol_mapper import build_public_market_symbol_mapping_batch


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("market_handoff_json")
    parser.add_argument("--issuer-resolution-json", action="append", default=[])
    parser.add_argument("--filing-collection-json", action="append", default=[])
    parser.add_argument("--output-json", required=True)
    args = parser.parse_args()

    handoff_batch = json.loads(Path(args.market_handoff_json).read_text(encoding="utf-8"))
    resolution_batches = [
        json.loads(Path(path).read_text(encoding="utf-8")) for path in args.issuer_resolution_json
    ]
    collection_batches = [
        json.loads(Path(path).read_text(encoding="utf-8")) for path in args.filing_collection_json
    ]
    output = build_public_market_symbol_mapping_batch(
        handoff_batch,
        issuer_resolution_batches=resolution_batches,
        filing_collection_batches=collection_batches,
    )

    output_path = Path(args.output_json)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(output, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
