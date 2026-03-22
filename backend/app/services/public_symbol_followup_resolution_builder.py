"""
Build resolved public-symbol mapping rows from explicit follow-up resolutions.
"""

from __future__ import annotations

from typing import Any, Dict, List


def _coerce_string(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def _resolution_index(resolution_input_batch: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    index: Dict[str, Dict[str, Any]] = {}
    for row in resolution_input_batch.get("resolution_inputs", []):
        key = _coerce_string(row.get("canonical_entity_name"))
        if key:
            index[key] = row
    return index


def _mapping_status(exchange_scope: str) -> str:
    if exchange_scope in {"foreign_home_market_code", "foreign_home_market_symbol"}:
        return "mapped_foreign_public_symbol"
    return "mapped_public_symbol"


def build_public_symbol_followup_resolution_batch(
    public_symbol_followup_batch: Dict[str, Any],
    resolution_input_batch: Dict[str, Any],
) -> Dict[str, Any]:
    resolution_by_name = _resolution_index(resolution_input_batch)
    symbol_rows: List[Dict[str, Any]] = []

    for followup_row in public_symbol_followup_batch.get("followup_rows", []):
        entity_name = _coerce_string(followup_row.get("canonical_entity_name"))
        resolution_row = resolution_by_name.get(entity_name)
        if not resolution_row:
            continue

        exchange_scope = _coerce_string(resolution_row.get("exchange_scope"))
        symbol_rows.append(
            {
                "system_label": _coerce_string(followup_row.get("system_label")),
                "canonical_entity_name": entity_name,
                "resolved_issuer_name": _coerce_string(
                    resolution_row.get("resolved_issuer_name") or followup_row.get("resolved_issuer_name")
                ),
                "market_handoff_status": "public_investable_now",
                "market_expression_scope": _coerce_string(
                    resolution_row.get("market_expression_scope") or "public_supplier_expression"
                ),
                "route_aware_priority_score": int(followup_row.get("route_aware_priority_score", 0)),
                "mapped_public_symbol": _coerce_string(resolution_row.get("mapped_public_symbol")),
                "symbol_mapping_status": _mapping_status(exchange_scope),
                "exchange_scope": exchange_scope,
                "symbol_mapping_basis": _coerce_string(resolution_row.get("symbol_mapping_basis")),
                "symbol_mapping_evidence": dict(resolution_row.get("symbol_mapping_evidence", {})),
                "symbol_mapping_action": "build_market_research_row_from_mapped_public_symbol",
                "filing_route_assessment": _coerce_string(followup_row.get("filing_route_assessment")),
                "live_resolution_status": _coerce_string(followup_row.get("live_resolution_status")),
            }
        )

    symbol_rows.sort(
        key=lambda item: (
            item["system_label"],
            0 if item["symbol_mapping_status"] == "mapped_public_symbol" else 1,
            -item["route_aware_priority_score"],
            item["canonical_entity_name"],
        )
    )

    return {
        "name": "public_symbol_followup_resolution_batch_v1",
        "symbol_rows": symbol_rows,
        "metrics": {
            "input_followup_row_count": len(public_symbol_followup_batch.get("followup_rows", [])),
            "resolved_symbol_row_count": len(symbol_rows),
            "mapped_public_symbol_count": len(
                [row for row in symbol_rows if row["symbol_mapping_status"] == "mapped_public_symbol"]
            ),
            "mapped_foreign_public_symbol_count": len(
                [row for row in symbol_rows if row["symbol_mapping_status"] == "mapped_foreign_public_symbol"]
            ),
        },
    }
