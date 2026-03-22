"""
Build a deterministic U.S.-accessibility layer for public market picks.
"""

from __future__ import annotations

from typing import Any, Dict, Iterable, List, Tuple


def _coerce_string(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def _candidate_index(candidate_batch: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    return {
        _coerce_string(row.get("name")): row
        for row in candidate_batch.get("rows", [])
        if _coerce_string(row.get("name"))
    }


def _symbol_index(symbol_mapping_batches: Iterable[Dict[str, Any]]) -> Dict[Tuple[str, str], Dict[str, Any]]:
    index: Dict[Tuple[str, str], Dict[str, Any]] = {}
    for batch in symbol_mapping_batches:
        for row in batch.get("symbol_rows", []):
            key = (_coerce_string(row.get("system_label")), _coerce_string(row.get("canonical_entity_name")))
            if key[0] and key[1]:
                index[key] = row
    return index


def _has_us_reference(symbol_row: Dict[str, Any]) -> bool:
    evidence = symbol_row.get("symbol_mapping_evidence", {}) or {}
    note = _coerce_string(evidence.get("note")).lower()
    source_url = _coerce_string(evidence.get("source_url")).lower()
    return any(marker in note for marker in ("adr", "otc")) or any(
        marker in source_url for marker in ("/adr", "otc")
    )


def _us_accessibility_status(exchange_scope: str, symbol_row: Dict[str, Any]) -> str:
    if exchange_scope == "direct_public_market_symbol":
        return "us_direct_primary"
    if exchange_scope in {"foreign_home_market_code", "foreign_home_market_symbol"}:
        if _has_us_reference(symbol_row):
            return "foreign_home_with_us_reference"
        return "foreign_home_market_only"
    return "accessibility_unknown"


def _us_accessibility_action(status: str) -> str:
    if status == "us_direct_primary":
        return "use_direct_us_symbol"
    if status == "foreign_home_with_us_reference":
        return "verify_adr_or_otc_liquidity_before_us_expression"
    if status == "foreign_home_market_only":
        return "use_home_market_symbol_or_add_us_access_followup"
    return "resolve_us_accessibility_before_expression"


def build_public_market_us_accessibility_batch(
    public_market_pick_batch: Dict[str, Any],
    public_market_scan_candidate_batch: Dict[str, Any],
    public_symbol_mapping_batches: List[Dict[str, Any]],
) -> Dict[str, Any]:
    candidate_by_name = _candidate_index(public_market_scan_candidate_batch)
    symbol_by_key = _symbol_index(public_symbol_mapping_batches)
    accessibility_rows: List[Dict[str, Any]] = []

    for pick_row in public_market_pick_batch.get("rows", []):
        pick_name = _coerce_string(pick_row.get("name"))
        candidate_row = candidate_by_name.get(pick_name, {})
        market_theme = _coerce_string(pick_row.get("market_theme"))
        canonical_entity_name = ""
        linked_companies = candidate_row.get("linked_companies", [])
        if linked_companies:
            canonical_entity_name = _coerce_string(linked_companies[0])

        symbol_row = symbol_by_key.get((market_theme, canonical_entity_name), {})
        exchange_scope = _coerce_string(candidate_row.get("market_data_checks", {}).get("exchange_scope"))
        status = _us_accessibility_status(exchange_scope, symbol_row)

        accessibility_rows.append(
            {
                "name": pick_name,
                "canonical_entity_name": canonical_entity_name,
                "underlying": _coerce_string(pick_row.get("underlying")),
                "market_theme": market_theme,
                "final_expression": _coerce_string(pick_row.get("final_expression")),
                "exchange_scope": exchange_scope,
                "us_accessibility_status": status,
                "us_accessibility_action": _us_accessibility_action(status),
                "us_reference_present": _has_us_reference(symbol_row),
                "symbol_mapping_basis": _coerce_string(symbol_row.get("symbol_mapping_basis")),
                "symbol_mapping_evidence": dict(symbol_row.get("symbol_mapping_evidence", {})),
            }
        )

    accessibility_rows.sort(
        key=lambda row: (
            {
                "us_direct_primary": 0,
                "foreign_home_with_us_reference": 1,
                "foreign_home_market_only": 2,
                "accessibility_unknown": 3,
            }.get(row["us_accessibility_status"], 4),
            row["market_theme"],
            row["name"],
        )
    )

    return {
        "name": "public_market_us_accessibility_batch_v1",
        "accessibility_rows": accessibility_rows,
        "metrics": {
            "input_pick_row_count": len(public_market_pick_batch.get("rows", [])),
            "us_direct_primary_count": len(
                [row for row in accessibility_rows if row["us_accessibility_status"] == "us_direct_primary"]
            ),
            "foreign_home_with_us_reference_count": len(
                [
                    row
                    for row in accessibility_rows
                    if row["us_accessibility_status"] == "foreign_home_with_us_reference"
                ]
            ),
            "foreign_home_market_only_count": len(
                [row for row in accessibility_rows if row["us_accessibility_status"] == "foreign_home_market_only"]
            ),
        },
    }
