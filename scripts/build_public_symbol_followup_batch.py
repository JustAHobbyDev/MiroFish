#!/usr/bin/env python3
"""
Build deterministic public-symbol follow-up tasks from public symbol mapping output.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from app.services.public_symbol_followup_builder import build_public_symbol_followup_batch


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--symbol-mapping-json", action="append", default=[])
    parser.add_argument("--output-json", required=True)
    args = parser.parse_args()

    mapping_batches = [
        json.loads(Path(path).read_text(encoding="utf-8")) for path in args.symbol_mapping_json
    ]
    output = build_public_symbol_followup_batch(mapping_batches)

    output_path = Path(args.output_json)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(output, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
