#!/usr/bin/env python3
"""
Build private-company diligence collections from plans and a local document manifest.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from app.services.private_company_diligence_collection_builder import (
    build_private_company_diligence_collection_batch,
)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("private_plan_json", help="Path to private-company diligence plan JSON.")
    parser.add_argument("manifest_json", help="Path to local diligence document manifest JSON.")
    parser.add_argument("--output-json", required=True, help="Path to write the collection JSON.")
    args = parser.parse_args()

    private_plan_batch = json.loads(Path(args.private_plan_json).read_text(encoding="utf-8"))
    manifest_batch = json.loads(Path(args.manifest_json).read_text(encoding="utf-8"))
    output = build_private_company_diligence_collection_batch(private_plan_batch, manifest_batch)

    output_path = Path(args.output_json)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(output, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
