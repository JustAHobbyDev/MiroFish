#!/usr/bin/env python3
"""
Build parsed private-company diligence batches from collected documents.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from app.services.private_company_diligence_parser import (
    build_private_company_diligence_parse_batch,
)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("collection_json", help="Path to private-company diligence collection JSON.")
    parser.add_argument("--output-json", required=True, help="Path to write the parse JSON.")
    args = parser.parse_args()

    collection_batch = json.loads(Path(args.collection_json).read_text(encoding="utf-8"))
    output = build_private_company_diligence_parse_batch(collection_batch)

    output_path = Path(args.output_json)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(output, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
