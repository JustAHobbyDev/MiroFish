#!/usr/bin/env python3
"""
Build private-company diligence plans from live issuer-resolution results.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from app.services.private_company_diligence_planner import build_private_company_diligence_plan_batch


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("issuer_resolution_live_json", help="Path to live issuer-resolution JSON.")
    parser.add_argument("--output-json", required=True, help="Path to write the diligence plan JSON.")
    args = parser.parse_args()

    issuer_resolution_batch = json.loads(Path(args.issuer_resolution_live_json).read_text(encoding="utf-8"))
    output = build_private_company_diligence_plan_batch(issuer_resolution_batch)

    output_path = Path(args.output_json)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(output, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
