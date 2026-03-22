"""
Deterministic route-aware priority scoring for bounded entity follow-up queues.
"""

from __future__ import annotations

from typing import Any, Dict, List


def _coerce_string(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def _priority_weight(priority_tier: str) -> int:
    return {"high": 30, "medium": 20, "low": 10}.get(_coerce_string(priority_tier).lower(), 0)


def _support_bonus(support_status: str) -> int:
    return {
        "supported_public_filing": 24,
        "supported_private_company": 18,
        "private_company_planned": 8,
        "needs_public_support_refresh": 4,
        "needs_live_resolution": 0,
        "not_yet_supported": 0,
    }.get(_coerce_string(support_status), 0)


def _route_bonus(route_type: str, route_assessment: str) -> int:
    route = _coerce_string(route_type)
    assessment = _coerce_string(route_assessment).lower()
    if route == "public_filing":
        if any(token in assessment for token in ("sec", "10-k", "20-f", "annual_report", "edinet")):
            return 6
        return 4
    if route == "private_company":
        return 3
    return 0


def _equipment_score(row: Dict[str, Any]) -> int:
    return (
        _priority_weight(row.get("priority_tier"))
        + _support_bonus(row.get("support_status"))
        + int(row.get("support_strong_evidence_item_count", 0)) * 2
        + int(row.get("support_component_specific_count", 0)) * 3
        + int(row.get("support_pressure_or_capacity_count", 0))
        + int(row.get("support_expansion_or_capex_count", 0))
        + int(row.get("support_financing_or_capital_count", 0))
        + _route_bonus(row.get("support_route_type"), row.get("route_assessment"))
    )


def _utility_score(row: Dict[str, Any]) -> int:
    utility_summary = dict(row.get("role_specific_evidence_summary", {}))
    return (
        _priority_weight(row.get("priority_tier"))
        + _support_bonus(row.get("support_status"))
        + int(row.get("support_strong_evidence_item_count", 0)) * 2
        + int(utility_summary.get("load_and_demand_signal_count", 0)) * 3
        + int(utility_summary.get("grid_response_signal_count", 0)) * 2
        + int(utility_summary.get("capex_response_signal_count", 0)) * 2
        + int(row.get("support_component_specific_count", 0))
        + int(row.get("support_financing_or_capital_count", 0))
        + _route_bonus(row.get("support_route_type"), row.get("route_assessment"))
    )


def _score_row(row: Dict[str, Any]) -> int:
    if _coerce_string(row.get("role_lane")) == "utility_or_operator":
        return _utility_score(row)
    return _equipment_score(row)


def _priority_tier(score: int, support_status: str) -> str:
    status = _coerce_string(support_status)
    if status == "supported_public_filing" and score >= 55:
        return "high"
    if status == "supported_private_company" and score >= 45:
        return "high"
    if score >= 35:
        return "medium"
    return "low"


def _selection_action(row: Dict[str, Any]) -> str:
    status = _coerce_string(row.get("support_status"))
    if status == "supported_public_filing":
        return "advance_with_public_filing_weight"
    if status == "supported_private_company":
        return "advance_with_private_company_weight"
    if status == "private_company_planned":
        return "collect_private_company_diligence"
    if status == "needs_public_support_refresh":
        return "refresh_public_filing_support"
    if status == "needs_live_resolution":
        return "resolve_issuer_and_collect_filing_route"
    return "hold_for_additional_source_coverage"


def build_bounded_entity_route_priority_batch(
    route_support_batch: Dict[str, Any],
) -> Dict[str, Any]:
    priority_rows: List[Dict[str, Any]] = []

    for row in route_support_batch.get("support_rows", []):
        score = _score_row(row)
        support_status = _coerce_string(row.get("support_status"))
        priority_rows.append(
            {
                **row,
                "route_aware_priority_score": score,
                "route_aware_priority_tier": _priority_tier(score, support_status),
                "selection_action": _selection_action(row),
            }
        )

    priority_rows.sort(
        key=lambda item: (
            {
                "supported_public_filing": 0,
                "supported_private_company": 1,
                "private_company_planned": 2,
                "needs_public_support_refresh": 3,
                "needs_live_resolution": 4,
                "not_yet_supported": 5,
            }.get(item["support_status"], 6),
            {"high": 0, "medium": 1, "low": 2}.get(item["route_aware_priority_tier"], 3),
            -item["route_aware_priority_score"],
            item["canonical_entity_name"],
        )
    )

    return {
        "name": "bounded_entity_route_priority_batch_v1",
        "priority_rows": priority_rows,
        "metrics": {
            "input_support_count": len(route_support_batch.get("support_rows", [])),
            "supported_public_count": len(
                [row for row in priority_rows if row["support_status"] == "supported_public_filing"]
            ),
            "supported_private_count": len(
                [row for row in priority_rows if row["support_status"] == "supported_private_company"]
            ),
            "high_priority_count": len(
                [row for row in priority_rows if row["route_aware_priority_tier"] == "high"]
            ),
        },
    }
