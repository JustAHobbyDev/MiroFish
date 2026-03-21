#!/usr/bin/env python3
"""
Build a deterministic company-filing parse batch from a filing collection batch.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from app.services.company_filing_parser import build_company_filing_parse_batch


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_json", help="Path to the company filing collection batch JSON.")
    parser.add_argument("--output-json", required=True, help="Path to write the parse batch JSON.")
    args = parser.parse_args()

    input_path = Path(args.input_json)
    output_path = Path(args.output_json)

    collection_batch = json.loads(input_path.read_text(encoding="utf-8"))
    parse_batch = build_company_filing_parse_batch(collection_batch)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(parse_batch, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
