#!/usr/bin/env python3
"""
Build filing-backed bounded entity priorities from entity expansions and filing support.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from app.services.bounded_entity_filing_priority import build_bounded_entity_filing_priority_batch


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("entity_expansion_json", help="Path to bounded entity expansion JSON.")
    parser.add_argument("filing_support_json", help="Path to filing support JSON.")
    parser.add_argument("--output-json", required=True, help="Path to write the priority JSON.")
    args = parser.parse_args()

    entity_batch = json.loads(Path(args.entity_expansion_json).read_text(encoding="utf-8"))
    support_batch = json.loads(Path(args.filing_support_json).read_text(encoding="utf-8"))
    output = build_bounded_entity_filing_priority_batch(entity_batch, support_batch)

    output_path = Path(args.output_json)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(output, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
