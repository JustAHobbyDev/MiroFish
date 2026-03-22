#!/usr/bin/env python3
"""
Build a broker-agnostic execution handoff object from the public execution queue.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from app.services.public_market_execution_handoff_builder import (
    build_public_market_execution_handoff,
)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("public_market_execution_queue_json")
    parser.add_argument("--output-json", required=True)
    args = parser.parse_args()

    queue_batch = json.loads(Path(args.public_market_execution_queue_json).read_text(encoding="utf-8"))
    output = build_public_market_execution_handoff(queue_batch)

    output_path = Path(args.output_json)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(output, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
