#!/usr/bin/env python3
"""
Adapt filing-backed priority rows into a route-review-surface-compatible batch.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from app.services.filing_priority_review_surface_adapter import (
    build_filing_priority_review_surface_batch,
)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("filing_priority_json")
    parser.add_argument("--output-json", required=True)
    args = parser.parse_args()

    filing_priority_batch = json.loads(Path(args.filing_priority_json).read_text(encoding="utf-8"))
    output = build_filing_priority_review_surface_batch(filing_priority_batch)

    output_path = Path(args.output_json)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(output, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
