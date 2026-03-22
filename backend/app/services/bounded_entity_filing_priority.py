"""
Deterministic filing-backed reprioritization for bounded entity expansions.
"""

from __future__ import annotations

from typing import Any, Dict, List


def _coerce_string(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def _priority_weight(priority_tier: str) -> int:
    return {"high": 30, "medium": 20, "low": 10}.get(_coerce_string(priority_tier).lower(), 0)


def _fallback_role_lane(entity_role: str) -> str:
    entity_role = _coerce_string(entity_role)
    if entity_role == "equipment_or_component_supplier":
        return "equipment_supplier"
    if entity_role in {"capacity_operator_or_owner", "power_or_utility_operator"}:
        return "utility_or_operator"
    return "general_beneficiary"


def _filling_route_bonus(route: str) -> int:
    route = _coerce_string(route).lower()
    if not route:
        return 0
    if any(token in route for token in ("sec", "10-k", "20-f", "annual_securities_report", "edinet")):
        return 6
    return 3


def _equipment_supplier_score(
    expansion: Dict[str, Any],
    support: Dict[str, Any],
    support_bonus: int,
) -> int:
    strong_count = int(support.get("filing_strong_evidence_item_count", 0))
    component_count = int(support.get("filing_component_specific_count", 0))
    capacity_count = int(support.get("filing_pressure_or_capacity_count", 0))
    expansion_count = int(support.get("filing_expansion_or_capex_count", 0))
    return (
        _priority_weight(_coerce_string(expansion.get("priority_tier")))
        + support_bonus
        + strong_count * 2
        + component_count * 3
        + capacity_count
        + expansion_count
        + _filling_route_bonus(_coerce_string(support.get("filing_route_assessment")))
    )


def _utility_operator_score(
    expansion: Dict[str, Any],
    support: Dict[str, Any],
    support_bonus: int,
) -> int:
    strong_count = int(support.get("filing_strong_evidence_item_count", 0))
    utility_summary = support.get("role_specific_evidence_summary", {})
    load_count = int(utility_summary.get("load_and_demand_signal_count", 0))
    grid_count = int(utility_summary.get("grid_response_signal_count", 0))
    capex_count = int(utility_summary.get("capex_response_signal_count", 0))
    component_count = int(support.get("filing_component_specific_count", 0))
    return (
        _priority_weight(_coerce_string(expansion.get("priority_tier")))
        + support_bonus
        + strong_count * 2
        + load_count * 3
        + grid_count * 2
        + capex_count * 2
        + component_count
        + _filling_route_bonus(_coerce_string(support.get("filing_route_assessment")))
    )


def _score_row(expansion: Dict[str, Any], support: Dict[str, Any]) -> int:
    support_bonus = 20 if _coerce_string(support.get("filing_support_status")) == "supported" else 0
    role_lane = _coerce_string(support.get("role_lane")) or _fallback_role_lane(
        _coerce_string(expansion.get("entity_role"))
    )
    if role_lane == "utility_or_operator":
        return _utility_operator_score(expansion, support, support_bonus)
    return _equipment_supplier_score(expansion, support, support_bonus)


def _priority_tier(score: int, support_status: str) -> str:
    support_status = _coerce_string(support_status)
    if support_status == "supported" and score >= 55:
        return "high"
    if support_status == "supported" and score >= 35:
        return "medium"
    if score >= 35:
        return "medium"
    return "low"


def _selection_action(support_status: str, next_priority_source_classes: List[str]) -> str:
    support_status = _coerce_string(support_status)
    if support_status == "supported":
        return "advance_with_filing_backed_weight"
    if "company_filing" in next_priority_source_classes:
        return "resolve_and_collect_filing_route"
    return "hold_for_additional_source_coverage"


def _index_support_rows(filing_support_batch: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    index: Dict[str, Dict[str, Any]] = {}
    for row in filing_support_batch.get("support_rows", []):
        canonical_entity_name = _coerce_string(row.get("canonical_entity_name"))
        if not canonical_entity_name:
            continue
        index[canonical_entity_name] = row
    return index


def build_bounded_entity_filing_priority_batch(
    entity_expansion_batch: Dict[str, Any],
    filing_support_batch: Dict[str, Any],
) -> Dict[str, Any]:
    support_index = _index_support_rows(filing_support_batch)
    priority_rows: List[Dict[str, Any]] = []

    for expansion in entity_expansion_batch.get("expansions", []):
        canonical_entity_name = _coerce_string(expansion.get("canonical_entity_name"))
        entity_role = _coerce_string(expansion.get("entity_role"))
        support = support_index.get(canonical_entity_name, {})
        role_lane = _coerce_string(support.get("role_lane")) or _fallback_role_lane(entity_role)
        next_priority_source_classes = [
            _coerce_string(item)
            for item in expansion.get("next_priority_source_classes", [])
            if _coerce_string(item)
        ]
        score = _score_row(expansion, support)
        support_status = _coerce_string(support.get("filing_support_status")) or "not_yet_supported"
        priority_rows.append(
            {
                "canonical_entity_name": canonical_entity_name,
                "system_label": _coerce_string(expansion.get("system_label")),
                "base_priority_tier": _coerce_string(expansion.get("priority_tier")) or "low",
                "entity_role": entity_role,
                "role_lane": role_lane,
                "support_provenance_status": _coerce_string(expansion.get("support_provenance_status")),
                "resolved_issuer_name": _coerce_string(support.get("resolved_issuer_name")),
                "filing_route_assessment": _coerce_string(support.get("filing_route_assessment")),
                "filing_support_status": support_status,
                "filing_evidence_item_count": int(support.get("filing_evidence_item_count", 0)),
                "filing_strong_evidence_item_count": int(
                    support.get("filing_strong_evidence_item_count", 0)
                ),
                "filing_component_specific_count": int(
                    support.get("filing_component_specific_count", 0)
                ),
                "filing_pressure_or_capacity_count": int(
                    support.get("filing_pressure_or_capacity_count", 0)
                ),
                "filing_expansion_or_capex_count": int(
                    support.get("filing_expansion_or_capex_count", 0)
                ),
                "role_specific_evidence_summary": dict(support.get("role_specific_evidence_summary", {})),
                "filing_backed_priority_score": score,
                "filing_backed_priority_tier": _priority_tier(score, support_status),
                "selection_action": _selection_action(support_status, next_priority_source_classes),
                "next_priority_source_classes": next_priority_source_classes,
                "top_filing_evidence_items": list(support.get("top_filing_evidence_items", [])),
            }
        )

    priority_rows.sort(
        key=lambda item: (
            0 if item["filing_support_status"] == "supported" else 1,
            {"equipment_supplier": 0, "utility_or_operator": 1, "general_beneficiary": 2}.get(
                item["role_lane"], 3
            ),
            {"high": 0, "medium": 1, "low": 2}.get(item["filing_backed_priority_tier"], 3),
            -item["filing_backed_priority_score"],
            item["canonical_entity_name"],
        )
    )
    priority_rows_by_role_lane = {
        "equipment_supplier": [row for row in priority_rows if row["role_lane"] == "equipment_supplier"],
        "utility_or_operator": [row for row in priority_rows if row["role_lane"] == "utility_or_operator"],
        "general_beneficiary": [row for row in priority_rows if row["role_lane"] == "general_beneficiary"],
    }
    return {
        "name": "bounded_entity_filing_priority_batch_v1",
        "priority_rows": priority_rows,
        "priority_rows_by_role_lane": priority_rows_by_role_lane,
        "metrics": {
            "input_entity_expansion_count": len(entity_expansion_batch.get("expansions", [])),
            "supported_priority_count": len(
                [row for row in priority_rows if row["filing_support_status"] == "supported"]
            ),
            "high_priority_count": len(
                [row for row in priority_rows if row["filing_backed_priority_tier"] == "high"]
            ),
            "role_lane_counts": {
                lane: len(rows) for lane, rows in priority_rows_by_role_lane.items()
            },
        },
    }
