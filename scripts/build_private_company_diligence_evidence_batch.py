#!/usr/bin/env python3
"""
Build evidence batches from parsed private-company diligence documents.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from app.services.private_company_diligence_evidence_builder import (
    build_private_company_diligence_evidence_batch,
)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("parsed_json", help="Path to private-company diligence parse JSON.")
    parser.add_argument("--output-json", required=True, help="Path to write the evidence JSON.")
    args = parser.parse_args()

    parsed_batch = json.loads(Path(args.parsed_json).read_text(encoding="utf-8"))
    output = build_private_company_diligence_evidence_batch(parsed_batch)

    output_path = Path(args.output_json)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(output, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
