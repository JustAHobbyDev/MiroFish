#!/usr/bin/env python3
"""
Build resolved public symbol rows from explicit public-symbol follow-up inputs.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from app.services.public_symbol_followup_resolution_builder import (
    build_public_symbol_followup_resolution_batch,
)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("public_symbol_followup_json")
    parser.add_argument("resolution_input_json")
    parser.add_argument("--output-json", required=True)
    args = parser.parse_args()

    followup_batch = json.loads(Path(args.public_symbol_followup_json).read_text(encoding="utf-8"))
    resolution_input_batch = json.loads(Path(args.resolution_input_json).read_text(encoding="utf-8"))
    output = build_public_symbol_followup_resolution_batch(followup_batch, resolution_input_batch)

    output_path = Path(args.output_json)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(output, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
