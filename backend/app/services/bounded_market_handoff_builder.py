"""
Build a deterministic bounded market handoff layer from route-backed entity rows.
"""

from __future__ import annotations

from typing import Any, Dict, List


def _coerce_string(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def _market_expression_scope(row: Dict[str, Any]) -> str:
    role_lane = _coerce_string(row.get("role_lane"))
    support_route_type = _coerce_string(row.get("support_route_type"))
    if support_route_type == "private_company" and role_lane == "equipment_supplier":
        return "private_supplier_chain_expression"
    if support_route_type == "private_company":
        return "private_capacity_watchlist_expression"
    if role_lane == "utility_or_operator":
        return "public_operator_expression"
    return "public_supplier_expression"


def _market_handoff_status(row: Dict[str, Any]) -> str:
    support_status = _coerce_string(row.get("support_status"))
    route_priority_tier = _coerce_string(row.get("route_aware_priority_tier"))
    role_lane = _coerce_string(row.get("role_lane"))

    if support_status == "supported_public_filing" and route_priority_tier == "high":
        return "public_investable_now"
    if support_status == "supported_private_company" and role_lane == "equipment_supplier":
        return "supplier_chain_followup"
    if support_status == "supported_private_company":
        return "private_watchlist_only"
    return "hold_for_more_corroboration"


def _market_handoff_action(row: Dict[str, Any], handoff_status: str) -> str:
    if handoff_status == "public_investable_now":
        return "resolve_public_market_symbol_and_build_market_research_row"
    if handoff_status == "supplier_chain_followup":
        return "map_public_suppliers_customers_and_expression_candidates"
    if handoff_status == "private_watchlist_only":
        return "track_private_capacity_and_map_public_counterparties"

    support_status = _coerce_string(row.get("support_status"))
    if support_status == "needs_live_resolution":
        return "resolve_issuer_route_before_market_handoff"
    if support_status == "private_company_planned":
        return "collect_private_company_diligence_before_market_handoff"
    if support_status == "needs_public_support_refresh":
        return "refresh_public_support_before_market_handoff"
    return "hold_for_additional_corroboration"


def _ticker_handoff_status(row: Dict[str, Any], handoff_status: str) -> str:
    if handoff_status == "public_investable_now":
        return "eligible_for_public_symbol_mapping"

    support_route_type = _coerce_string(row.get("support_route_type"))
    if support_route_type == "private_company":
        return "blocked_private_route"
    return "not_ready"


def _ticker_handoff_block_reason(row: Dict[str, Any], handoff_status: str) -> str:
    if handoff_status == "public_investable_now":
        return ""

    support_route_type = _coerce_string(row.get("support_route_type"))
    support_status = _coerce_string(row.get("support_status"))
    if support_route_type == "private_company":
        return "private_company_route_has_no_direct_public_symbol"
    if support_status == "needs_live_resolution":
        return "issuer_route_not_resolved"
    if support_status == "needs_public_support_refresh":
        return "public_support_not_yet_refreshed"
    if support_status == "private_company_planned":
        return "private_company_support_not_yet_collected"
    return "insufficient_market_handoff_support"


def _normalized_rows(review_surface_batch: Dict[str, Any]) -> List[Dict[str, Any]]:
    handoff_rows: List[Dict[str, Any]] = []
    for row in review_surface_batch.get("rows", []):
        handoff_status = _market_handoff_status(row)
        handoff_rows.append(
            {
                "system_label": _coerce_string(row.get("system_label")),
                "canonical_entity_name": _coerce_string(row.get("canonical_entity_name")),
                "resolved_issuer_name": _coerce_string(row.get("resolved_issuer_name")),
                "entity_role": _coerce_string(row.get("entity_role")),
                "role_lane": _coerce_string(row.get("role_lane")),
                "support_route_type": _coerce_string(row.get("support_route_type")),
                "support_status": _coerce_string(row.get("support_status")),
                "route_assessment": _coerce_string(row.get("route_assessment")),
                "route_aware_priority_score": int(row.get("route_aware_priority_score", 0)),
                "route_aware_priority_tier": _coerce_string(row.get("route_aware_priority_tier")),
                "selection_action": _coerce_string(row.get("selection_action")),
                "market_expression_scope": _market_expression_scope(row),
                "market_handoff_status": handoff_status,
                "market_handoff_action": _market_handoff_action(row, handoff_status),
                "ticker_handoff_status": _ticker_handoff_status(row, handoff_status),
                "ticker_handoff_block_reason": _ticker_handoff_block_reason(row, handoff_status),
                "source_classes": list(row.get("source_classes", [])),
                "top_support_evidence_items": list(row.get("top_support_evidence_items", [])),
            }
        )
    return handoff_rows


def _status_metrics(rows: List[Dict[str, Any]]) -> Dict[str, int]:
    return {
        "public_investable_now_count": len(
            [row for row in rows if row["market_handoff_status"] == "public_investable_now"]
        ),
        "private_watchlist_only_count": len(
            [row for row in rows if row["market_handoff_status"] == "private_watchlist_only"]
        ),
        "supplier_chain_followup_count": len(
            [row for row in rows if row["market_handoff_status"] == "supplier_chain_followup"]
        ),
        "hold_for_more_corroboration_count": len(
            [row for row in rows if row["market_handoff_status"] == "hold_for_more_corroboration"]
        ),
        "eligible_for_public_symbol_mapping_count": len(
            [row for row in rows if row["ticker_handoff_status"] == "eligible_for_public_symbol_mapping"]
        ),
    }


def build_bounded_market_handoff_batch(
    review_surface_batch: Dict[str, Any],
) -> Dict[str, Any]:
    rows = _normalized_rows(review_surface_batch)
    rows.sort(
        key=lambda item: (
            item["system_label"],
            {
                "public_investable_now": 0,
                "supplier_chain_followup": 1,
                "private_watchlist_only": 2,
                "hold_for_more_corroboration": 3,
            }.get(item["market_handoff_status"], 4),
            -item["route_aware_priority_score"],
            item["canonical_entity_name"],
        )
    )

    rows_by_lane: Dict[str, List[Dict[str, Any]]] = {}
    for row in rows:
        rows_by_lane.setdefault(row["system_label"], []).append(row)

    return {
        "name": "bounded_market_handoff_batch_v1",
        "handoff_rows": rows,
        "rows_by_lane": rows_by_lane,
        "metrics": {
            "input_review_row_count": len(review_surface_batch.get("rows", [])),
            **_status_metrics(rows),
        },
    }
