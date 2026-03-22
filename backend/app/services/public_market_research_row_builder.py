"""
Build deterministic public market-research rows from symbol mapping and role classification.
"""

from __future__ import annotations

from typing import Any, Dict, Iterable, List, Tuple


def _coerce_string(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def _role_index(classification_batches: Iterable[Dict[str, Any]]) -> Dict[Tuple[str, str], Dict[str, Any]]:
    index: Dict[Tuple[str, str], Dict[str, Any]] = {}
    for batch in classification_batches:
        for row in batch.get("classification_rows", []):
            key = (_coerce_string(row.get("system_label")), _coerce_string(row.get("canonical_entity_name")))
            index[key] = row
    return index


def _research_row_status(symbol_mapping_status: str) -> str:
    if symbol_mapping_status in {"mapped_public_symbol", "mapped_foreign_public_symbol"}:
        return "ready_for_market_research"
    return "symbol_followup_required_before_market_research"


def _research_row_action(symbol_row: Dict[str, Any], role_row: Dict[str, Any]) -> str:
    status = _coerce_string(symbol_row.get("symbol_mapping_status"))
    role_label = _coerce_string(role_row.get("bottleneck_role_label"))
    if status not in {"mapped_public_symbol", "mapped_foreign_public_symbol"}:
        return "resolve_public_symbol_before_market_research_row"
    if role_label == "bottleneck_candidate":
        return "build_bottleneck_market_research_row"
    if role_label == "capacity_response_operator":
        return "build_operator_market_research_row"
    return "build_beneficiary_market_research_row"


def build_public_market_research_row_batch(
    symbol_mapping_batches: List[Dict[str, Any]],
    bottleneck_classification_batches: List[Dict[str, Any]],
) -> Dict[str, Any]:
    role_by_key = _role_index(bottleneck_classification_batches)
    research_rows_by_key: Dict[Tuple[str, str], Dict[str, Any]] = {}

    for batch in symbol_mapping_batches:
        for row in batch.get("symbol_rows", []):
            key = (_coerce_string(row.get("system_label")), _coerce_string(row.get("canonical_entity_name")))
            role_row = role_by_key.get(key, {})
            symbol_mapping_status = _coerce_string(row.get("symbol_mapping_status"))
            research_rows_by_key[key] = {
                "system_label": _coerce_string(row.get("system_label")),
                "canonical_entity_name": _coerce_string(row.get("canonical_entity_name")),
                "resolved_issuer_name": _coerce_string(row.get("resolved_issuer_name")),
                "mapped_public_symbol": _coerce_string(row.get("mapped_public_symbol")),
                "exchange_scope": _coerce_string(row.get("exchange_scope")),
                "symbol_mapping_status": symbol_mapping_status,
                "market_expression_scope": _coerce_string(row.get("market_expression_scope")),
                "bottleneck_role_label": _coerce_string(role_row.get("bottleneck_role_label")),
                "classification_reason": _coerce_string(role_row.get("classification_reason")),
                "market_research_row_status": _research_row_status(symbol_mapping_status),
                "market_research_row_action": _research_row_action(row, role_row),
                "route_aware_priority_score": int(row.get("route_aware_priority_score", 0)),
            }

    research_rows = list(research_rows_by_key.values())

    research_rows.sort(
        key=lambda item: (
            item["system_label"],
            0 if item["market_research_row_status"] == "ready_for_market_research" else 1,
            {
                "bottleneck_candidate": 0,
                "capacity_response_operator": 1,
                "supply_chain_beneficiary": 2,
                "": 3,
            }.get(item["bottleneck_role_label"], 4),
            -item["route_aware_priority_score"],
            item["canonical_entity_name"],
        )
    )

    return {
        "name": "public_market_research_row_batch_v1",
        "research_rows": research_rows,
        "metrics": {
            "input_symbol_row_count": sum(len(batch.get("symbol_rows", [])) for batch in symbol_mapping_batches),
            "ready_for_market_research_count": len(
                [row for row in research_rows if row["market_research_row_status"] == "ready_for_market_research"]
            ),
            "symbol_followup_required_count": len(
                [
                    row
                    for row in research_rows
                    if row["market_research_row_status"] == "symbol_followup_required_before_market_research"
                ]
            ),
            "bottleneck_candidate_count": len(
                [row for row in research_rows if row["bottleneck_role_label"] == "bottleneck_candidate"]
            ),
            "capacity_response_operator_count": len(
                [row for row in research_rows if row["bottleneck_role_label"] == "capacity_response_operator"]
            ),
            "supply_chain_beneficiary_count": len(
                [row for row in research_rows if row["bottleneck_role_label"] == "supply_chain_beneficiary"]
            ),
        },
    }
