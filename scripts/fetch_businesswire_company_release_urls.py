#!/usr/bin/env python3
"""
Fetch Business Wire article URLs into raw company-release records.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from app.services.businesswire_company_release_collector import (
    fetch_businesswire_company_release_records,
)


def _load_urls(args: argparse.Namespace) -> list[str]:
    urls = list(args.url or [])
    if args.urls_json:
        payload = json.loads(Path(args.urls_json).read_text(encoding="utf-8"))
        if isinstance(payload, list):
            urls.extend(str(item) for item in payload)
        elif isinstance(payload, dict) and isinstance(payload.get("urls"), list):
            urls.extend(str(item) for item in payload["urls"])
        else:
            raise ValueError("urls_json must be a list or an object with a 'urls' list")
    return urls


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", action="append", default=[])
    parser.add_argument("--urls-json")
    parser.add_argument("--output-json", required=True)
    args = parser.parse_args()

    urls = _load_urls(args)
    payload = {
        "name": "businesswire_company_release_raw_v1",
        "publisher": "Business Wire",
        "records": fetch_businesswire_company_release_records(urls),
        "metrics": {
            "requested_url_count": len(urls),
        },
    }

    output_path = Path(args.output_json)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
