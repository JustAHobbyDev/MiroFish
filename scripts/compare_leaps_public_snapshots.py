#!/usr/bin/env python3
"""
Compare far-dated public options-chain snapshots for a small candidate set.

This is intentionally lightweight and file-based. It operates on the normalized
JSON snapshots captured through the public Playwright workflow.
"""

from __future__ import annotations

import argparse
import json
import statistics
from pathlib import Path
from typing import Any, Dict, List


REFERENCE_SPOTS = {
    "MP": {
        "spot": 63.013,
        "note": "Recent public delayed reference from ADVFN snapshot noted in the live mispricing memo.",
    },
    "MU": {
        "spot": 401.10,
        "note": "Recent public delayed reference from ADVFN snapshot noted in the live mispricing memo.",
    },
    "VRT": {
        "spot": 243.00,
        "note": "Recent public delayed reference from ADVFN snapshot noted in the live mispricing memo.",
    },
}


def _load_contracts(path: Path) -> tuple[Dict[str, Any], List[Dict[str, Any]]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    expiry = payload["expiries"][0]
    return payload["capture_meta"], expiry["contracts"]


def _rel_spread(contract: Dict[str, Any]) -> float | None:
    bid = contract.get("bid")
    ask = contract.get("ask")
    if not isinstance(bid, (int, float)) or not isinstance(ask, (int, float)):
        return None
    midpoint = (bid + ask) / 2
    if midpoint <= 0:
        return None
    return (ask - bid) / midpoint


def _liquid_calls(contracts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    rows = []
    for contract in contracts:
        if contract.get("right") != "call":
            continue
        if not isinstance(contract.get("bid"), (int, float)):
            continue
        if not isinstance(contract.get("ask"), (int, float)):
            continue
        if contract.get("ask", 0) <= 0:
            continue
        rows.append(contract)
    return rows


def _percentile_median(values: List[float]) -> float | None:
    if not values:
        return None
    return statistics.median(values)


def _pick_candidate(contracts: List[Dict[str, Any]], reference_spot: float) -> Dict[str, Any]:
    target_strike = reference_spot * 1.10
    eligible = [
        contract
        for contract in contracts
        if (contract.get("open_interest") or 0) >= 100 and _rel_spread(contract) is not None
    ]
    pool = eligible or contracts
    best = min(
        pool,
        key=lambda contract: (
            abs(float(contract["strike"]) - target_strike),
            -float(contract.get("open_interest") or 0),
            _rel_spread(contract) or 999,
        ),
    )
    midpoint = (best["bid"] + best["ask"]) / 2
    return {
        "option_symbol": best["option_symbol"],
        "strike": best["strike"],
        "target_strike": round(target_strike, 3),
        "reference_spot": reference_spot,
        "bid": best["bid"],
        "ask": best["ask"],
        "mid": round(midpoint, 3),
        "open_interest": best.get("open_interest"),
        "volume": best.get("volume"),
        "implied_volatility": best.get("implied_volatility"),
        "relative_spread": round(_rel_spread(best) or 0.0, 4),
    }


def _analyze_symbol(symbol: str, snapshot_path: Path) -> Dict[str, Any]:
    meta, contracts = _load_contracts(snapshot_path)
    calls = _liquid_calls(contracts)
    liquid_for_stats = [row for row in calls if (row.get("open_interest") or 0) >= 100]
    ivs = [
        row["implied_volatility"]
        for row in liquid_for_stats
        if isinstance(row.get("implied_volatility"), (int, float)) and row["implied_volatility"] > 0
    ]
    spreads = [
        _rel_spread(row)
        for row in liquid_for_stats
        if _rel_spread(row) is not None
    ]
    strongest_oi = max(liquid_for_stats or calls, key=lambda row: row.get("open_interest") or 0)
    ref = REFERENCE_SPOTS[symbol]
    candidate = _pick_candidate(calls, ref["spot"])

    return {
        "symbol": symbol,
        "snapshot_path": str(snapshot_path),
        "source_page": meta.get("source_page"),
        "expiry": calls[0]["expiry"] if calls else None,
        "reference_spot": ref,
        "chain_stats": {
            "contract_count": len(calls),
            "liquid_contract_count": len(liquid_for_stats),
            "median_implied_volatility": round(_percentile_median(ivs), 4) if ivs else None,
            "median_relative_spread": round(_percentile_median(spreads), 4) if spreads else None,
            "max_open_interest": strongest_oi.get("open_interest"),
            "max_open_interest_contract": strongest_oi.get("option_symbol"),
        },
        "candidate_call": candidate,
    }


def _rank(records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    # Lower IV and lower spread are better; higher OI is better.
    ranked = []
    for record in records:
        stats = record["chain_stats"]
        candidate = record["candidate_call"]
        composite = (
            (stats["median_implied_volatility"] or 9.999) * 100
            + (candidate["relative_spread"] * 100)
            - min(candidate["open_interest"] or 0, 10000) / 1000
        )
        copy = dict(record)
        copy["comparison_score"] = round(composite, 3)
        ranked.append(copy)
    return sorted(ranked, key=lambda row: row["comparison_score"])


def main() -> int:
    parser = argparse.ArgumentParser(description="Compare public LEAPS snapshot candidates")
    parser.add_argument(
        "--output-json",
        required=True,
        help="Path to write machine-readable analysis JSON",
    )
    args = parser.parse_args()

    snapshot_paths = {
        "MP": Path("research/options-data/2026-03-15/MP-chain-yahoo-2027-01-15.json"),
        "MU": Path("research/options-data/2026-03-15/MU-chain-yahoo-2027-01-15.json"),
        "VRT": Path("research/options-data/2026-03-15/VRT-chain-yahoo-2027-01-15.json"),
    }

    records = [_analyze_symbol(symbol, path) for symbol, path in snapshot_paths.items()]
    output = {
        "generated_from": "public delayed Yahoo Jan 15 2027 chain captures",
        "records": _rank(records),
    }

    out_path = Path(args.output_json)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
