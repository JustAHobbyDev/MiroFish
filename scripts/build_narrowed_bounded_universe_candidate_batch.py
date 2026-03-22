#!/usr/bin/env python3
"""
Build bounded-universe candidates from narrowed structural-pressure candidates.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from app.services.narrowed_bounded_universe_adapter import (
    build_narrowed_bounded_universe_candidate_batch,
)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("narrowing_json", help="Path to narrowed structural-pressure JSON.")
    parser.add_argument("--output-json", required=True, help="Path to write the bounded-universe JSON.")
    args = parser.parse_args()

    narrowing_batch = json.loads(Path(args.narrowing_json).read_text(encoding="utf-8"))
    output = build_narrowed_bounded_universe_candidate_batch(narrowing_batch)

    output_path = Path(args.output_json)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(output, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
