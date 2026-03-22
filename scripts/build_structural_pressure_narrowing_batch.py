#!/usr/bin/env python3
"""
Build narrowed structural-pressure candidates from broad structural-pressure lanes.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from app.services.structural_pressure_narrower import build_structural_pressure_narrowing_batch


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("structural_pressure_json", help="Path to structural pressure JSON.")
    parser.add_argument("capital_cluster_json", help="Path to capital cluster JSON.")
    parser.add_argument("mixed_prefilter_json", help="Path to mixed prefilter JSON.")
    parser.add_argument("--output-json", required=True, help="Path to write the narrowed batch JSON.")
    args = parser.parse_args()

    structural_pressure_batch = json.loads(Path(args.structural_pressure_json).read_text(encoding="utf-8"))
    capital_cluster_batch = json.loads(Path(args.capital_cluster_json).read_text(encoding="utf-8"))
    mixed_prefilter_batch = json.loads(Path(args.mixed_prefilter_json).read_text(encoding="utf-8"))
    output = build_structural_pressure_narrowing_batch(
        structural_pressure_batch,
        capital_cluster_batch,
        mixed_prefilter_batch,
    )

    output_path = Path(args.output_json)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(output, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
