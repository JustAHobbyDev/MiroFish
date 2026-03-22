"""
Build deterministic public-symbol follow-up tasks for blocked public names.
"""

from __future__ import annotations

from typing import Any, Dict, Iterable, List


def _coerce_string(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def _followup_type(row: Dict[str, Any]) -> str:
    live_resolution_status = _coerce_string(row.get("live_resolution_status"))
    if live_resolution_status == "resolved_direct_foreign_public_route":
        return "foreign_public_symbol_followup"
    if live_resolution_status == "resolved_parent_route":
        return "parent_public_symbol_followup"
    return "public_symbol_followup"


def _followup_action(followup_type: str) -> str:
    if followup_type == "foreign_public_symbol_followup":
        return "confirm_primary_listing_symbol_and_tradable_market_code"
    if followup_type == "parent_public_symbol_followup":
        return "confirm_parent_listing_symbol_and_parent_entity_market_mapping"
    return "confirm_public_symbol_mapping"


def build_public_symbol_followup_batch(
    public_symbol_mapping_batches: Iterable[Dict[str, Any]],
) -> Dict[str, Any]:
    followup_rows: List[Dict[str, Any]] = []
    input_symbol_row_count = 0

    for batch in public_symbol_mapping_batches:
        symbol_rows = batch.get("symbol_rows", [])
        input_symbol_row_count += len(symbol_rows)
        for row in symbol_rows:
            status = _coerce_string(row.get("symbol_mapping_status"))
            if status not in {
                "public_symbol_followup_required",
                "public_symbol_followup_required_foreign_route",
            }:
                continue

            followup_type = _followup_type(row)
            followup_rows.append(
                {
                    "system_label": _coerce_string(row.get("system_label")),
                    "canonical_entity_name": _coerce_string(row.get("canonical_entity_name")),
                    "resolved_issuer_name": _coerce_string(row.get("resolved_issuer_name")),
                    "followup_type": followup_type,
                    "followup_action": _followup_action(followup_type),
                    "exchange_scope": _coerce_string(row.get("exchange_scope")),
                    "symbol_mapping_status": status,
                    "filing_route_assessment": _coerce_string(row.get("filing_route_assessment")),
                    "live_resolution_status": _coerce_string(row.get("live_resolution_status")),
                    "route_aware_priority_score": int(row.get("route_aware_priority_score", 0)),
                }
            )

    followup_rows.sort(
        key=lambda item: (
            {
                "foreign_public_symbol_followup": 0,
                "parent_public_symbol_followup": 1,
                "public_symbol_followup": 2,
            }.get(item["followup_type"], 3),
            -item["route_aware_priority_score"],
            item["canonical_entity_name"],
        )
    )

    return {
        "name": "public_symbol_followup_batch_v1",
        "followup_rows": followup_rows,
        "metrics": {
            "input_symbol_row_count": input_symbol_row_count,
            "followup_count": len(followup_rows),
            "foreign_public_symbol_followup_count": len(
                [row for row in followup_rows if row["followup_type"] == "foreign_public_symbol_followup"]
            ),
            "parent_public_symbol_followup_count": len(
                [row for row in followup_rows if row["followup_type"] == "parent_public_symbol_followup"]
            ),
        },
    }
