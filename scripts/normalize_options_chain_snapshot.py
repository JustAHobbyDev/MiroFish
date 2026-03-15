#!/usr/bin/env python3
"""
Normalize manually captured or Playwright-exported options chain snapshots.

The goal is not to scrape a broker directly in this script. Instead, it turns a
rough capture artifact into a stable JSON shape that later analysis can trust.
"""

from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List


NUMERIC_FIELDS = {
    "underlying_price",
    "strike",
    "bid",
    "ask",
    "last",
    "mark",
    "volume",
    "open_interest",
    "implied_volatility",
    "delta",
    "gamma",
    "theta",
    "vega",
    "days_to_expiry",
}


def _coerce_number(value: Any) -> Any:
    if value in ("", None):
        return None
    if isinstance(value, (int, float)):
        return value
    text = str(value).strip().replace(",", "")
    if text in {"--", "N/A", "na", "None"}:
        return None
    try:
        if "." in text:
            return float(text)
        return int(text)
    except ValueError:
        return value


def _coerce_bool(value: Any) -> bool | None:
    if value in ("", None):
        return None
    if isinstance(value, bool):
        return value
    text = str(value).strip().lower()
    if text in {"true", "yes", "y", "1"}:
        return True
    if text in {"false", "no", "n", "0"}:
        return False
    return None


def _normalize_contract(row: Dict[str, Any]) -> Dict[str, Any]:
    contract = {
        "option_symbol": row.get("option_symbol"),
        "underlying": row.get("underlying"),
        "expiry": row.get("expiry"),
        "right": row.get("right"),
        "strike": _coerce_number(row.get("strike")),
        "bid": _coerce_number(row.get("bid")),
        "ask": _coerce_number(row.get("ask")),
        "last": _coerce_number(row.get("last")),
        "mark": _coerce_number(row.get("mark")),
        "volume": _coerce_number(row.get("volume")),
        "open_interest": _coerce_number(row.get("open_interest")),
        "implied_volatility": _coerce_number(row.get("implied_volatility")),
        "delta": _coerce_number(row.get("delta")),
        "gamma": _coerce_number(row.get("gamma")),
        "theta": _coerce_number(row.get("theta")),
        "vega": _coerce_number(row.get("vega")),
        "in_the_money": _coerce_bool(row.get("in_the_money")),
        "raw_row": row,
    }
    return {key: value for key, value in contract.items() if value is not None}


def _load_csv(path: Path) -> List[Dict[str, Any]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        return [dict(row) for row in reader]


def _load_json_rows(path: Path) -> List[Dict[str, Any]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict) and isinstance(payload.get("rows"), list):
        return payload["rows"]
    raise ValueError("JSON input must be a list or an object with a 'rows' list")


def _group_by_expiry(rows: Iterable[Dict[str, Any]]) -> List[Dict[str, Any]]:
    expiries: Dict[str, Dict[str, Any]] = {}
    for row in rows:
        expiry = row.get("expiry")
        if not expiry:
            raise ValueError("each row must include 'expiry'")

        entry = expiries.setdefault(
            expiry,
            {
                "expiry": expiry,
                "days_to_expiry": _coerce_number(row.get("days_to_expiry")),
                "contracts": [],
            },
        )
        if entry.get("days_to_expiry") is None:
            entry["days_to_expiry"] = _coerce_number(row.get("days_to_expiry"))
        entry["contracts"].append(_normalize_contract(row))

    return [expiries[key] for key in sorted(expiries.keys())]


def _infer_capture_meta(
    rows: List[Dict[str, Any]],
    provider: str,
    source_page: str | None,
    notes: List[str],
) -> Dict[str, Any]:
    first = rows[0] if rows else {}
    meta = {
        "provider": provider,
        "captured_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "underlying": first.get("underlying"),
        "underlying_price": _coerce_number(first.get("underlying_price")),
        "currency": first.get("currency", "USD"),
        "capture_mode": "user_mediated_playwright",
        "source_page": source_page,
        "notes": notes,
    }
    return {key: value for key, value in meta.items() if value not in (None, [], "")}


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Normalize captured options chain rows into a stable JSON snapshot."
    )
    parser.add_argument("input_file", help="Input CSV or JSON file")
    parser.add_argument("--output-json", required=True, help="Output JSON path")
    parser.add_argument(
        "--provider",
        default="schwab-playwright-manual",
        help="Provider label for capture metadata",
    )
    parser.add_argument("--source-page", help="Optional source page URL")
    parser.add_argument(
        "--note",
        action="append",
        default=[],
        help="Optional note; may be repeated",
    )
    args = parser.parse_args()

    path = Path(args.input_file)
    suffix = path.suffix.lower()
    if suffix == ".csv":
        rows = _load_csv(path)
    elif suffix == ".json":
        rows = _load_json_rows(path)
    else:
        raise SystemExit("input file must be .csv or .json")

    if not rows:
        raise SystemExit("input file contains no rows")

    output = {
        "capture_meta": _infer_capture_meta(
            rows=rows,
            provider=args.provider,
            source_page=args.source_page,
            notes=args.note,
        ),
        "expiries": _group_by_expiry(rows),
    }

    out_path = Path(args.output_json)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
