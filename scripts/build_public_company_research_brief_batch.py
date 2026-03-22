#!/usr/bin/env python3
"""
Build filing-backed public company research briefs from execution handoff rows.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from app.services.public_company_research_brief_builder import (
    build_public_company_research_brief_batch,
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("public_market_execution_handoff_json", type=Path)
    parser.add_argument("bounded_entity_filing_support_json", type=Path)
    parser.add_argument("--output-json", type=Path, required=True)
    args = parser.parse_args()

    handoff_batch = json.loads(args.public_market_execution_handoff_json.read_text(encoding="utf-8"))
    support_batch = json.loads(args.bounded_entity_filing_support_json.read_text(encoding="utf-8"))
    output = build_public_company_research_brief_batch(handoff_batch, support_batch)

    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(
        json.dumps(output, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
