#!/usr/bin/env python3
"""
Attach filing evidence back to bounded entity expansions.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from app.services.bounded_entity_filing_support import build_bounded_entity_filing_support_batch


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("entity_expansion_json", help="Path to the bounded entity expansion batch JSON.")
    parser.add_argument("evidence_json", help="Path to the company filing evidence batch JSON.")
    parser.add_argument("--output-json", required=True, help="Path to write the support batch JSON.")
    args = parser.parse_args()

    entity_batch = json.loads(Path(args.entity_expansion_json).read_text(encoding="utf-8"))
    evidence_batch = json.loads(Path(args.evidence_json).read_text(encoding="utf-8"))
    output = build_bounded_entity_filing_support_batch(entity_batch, evidence_batch)

    output_path = Path(args.output_json)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(output, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
