"""
Deterministic bottleneck-role classification for bounded downstream entities.
"""

from __future__ import annotations

from typing import Any, Dict, List, Tuple


CONSTRAINED_COMPONENT_TOKENS = (
    "transformer",
    "grid equipment",
    "switchgear",
    "substation",
)


def _coerce_string(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def _row_key(row: Dict[str, Any]) -> Tuple[str, str]:
    return (_coerce_string(row.get("system_label")), _coerce_string(row.get("canonical_entity_name")))


def _handoff_index(market_handoff_batch: Dict[str, Any]) -> Dict[Tuple[str, str], Dict[str, Any]]:
    return {_row_key(row): row for row in market_handoff_batch.get("handoff_rows", [])}


def _has_constrained_component_context(review_row: Dict[str, Any]) -> bool:
    system_label = _coerce_string(review_row.get("system_label")).lower()
    if any(token in system_label for token in CONSTRAINED_COMPONENT_TOKENS):
        return True

    for item in review_row.get("top_support_evidence_items", []):
        keyword = _coerce_string(item.get("keyword")).lower()
        excerpt = _coerce_string(item.get("excerpt")).lower()
        if any(token in keyword or token in excerpt for token in CONSTRAINED_COMPONENT_TOKENS):
            return True
    return False


def _is_bottleneck_candidate(review_row: Dict[str, Any]) -> bool:
    strong = int(review_row.get("support_strong_evidence_item_count", 0))
    component = int(review_row.get("support_component_specific_count", 0))
    pressure = int(review_row.get("support_pressure_or_capacity_count", 0))
    expansion = int(review_row.get("support_expansion_or_capex_count", 0))
    return (
        _coerce_string(review_row.get("role_lane")) == "equipment_supplier"
        and _has_constrained_component_context(review_row)
        and strong >= 8
        and component >= 3
        and (pressure >= 2 or expansion >= 2)
    )


def _classification_reason(review_row: Dict[str, Any], role_label: str) -> str:
    if role_label == "capacity_response_operator":
        return "operator_or_capacity_owner_with_pressure_and_response_evidence"
    if role_label == "bottleneck_candidate":
        return "supplier_in_constrained_component_layer_with_strong_component_pressure_and_expansion_evidence"
    return "supplier_or_adjacent_name_with_relevance_but_without_strict_bottleneck_evidence"


def build_bottleneck_role_classification_batch(
    route_review_surface_batch: Dict[str, Any],
    market_handoff_batch: Dict[str, Any],
) -> Dict[str, Any]:
    handoff_by_key = _handoff_index(market_handoff_batch)
    classification_rows: List[Dict[str, Any]] = []

    for review_row in route_review_surface_batch.get("rows", []):
        role_lane = _coerce_string(review_row.get("role_lane"))
        if role_lane == "utility_or_operator":
            role_label = "capacity_response_operator"
        elif _is_bottleneck_candidate(review_row):
            role_label = "bottleneck_candidate"
        else:
            role_label = "supply_chain_beneficiary"

        handoff_row = handoff_by_key.get(_row_key(review_row), {})

        classification_rows.append(
            {
                "system_label": _coerce_string(review_row.get("system_label")),
                "canonical_entity_name": _coerce_string(review_row.get("canonical_entity_name")),
                "resolved_issuer_name": _coerce_string(review_row.get("resolved_issuer_name")),
                "entity_role": _coerce_string(review_row.get("entity_role")),
                "role_lane": role_lane,
                "bottleneck_role_label": role_label,
                "classification_reason": _classification_reason(review_row, role_label),
                "market_handoff_status": _coerce_string(handoff_row.get("market_handoff_status")),
                "support_route_type": _coerce_string(review_row.get("support_route_type")),
                "support_status": _coerce_string(review_row.get("support_status")),
                "route_aware_priority_score": int(review_row.get("route_aware_priority_score", 0)),
                "support_strong_evidence_item_count": int(
                    review_row.get("support_strong_evidence_item_count", 0)
                ),
                "support_component_specific_count": int(
                    review_row.get("support_component_specific_count", 0)
                ),
                "support_pressure_or_capacity_count": int(
                    review_row.get("support_pressure_or_capacity_count", 0)
                ),
                "support_expansion_or_capex_count": int(
                    review_row.get("support_expansion_or_capex_count", 0)
                ),
                "source_classes": list(review_row.get("source_classes", [])),
            }
        )

    classification_rows.sort(
        key=lambda item: (
            item["system_label"],
            {
                "bottleneck_candidate": 0,
                "capacity_response_operator": 1,
                "supply_chain_beneficiary": 2,
            }.get(item["bottleneck_role_label"], 3),
            -item["route_aware_priority_score"],
            item["canonical_entity_name"],
        )
    )

    return {
        "name": "bottleneck_role_classification_batch_v1",
        "classification_rows": classification_rows,
        "metrics": {
            "input_review_row_count": len(route_review_surface_batch.get("rows", [])),
            "bottleneck_candidate_count": len(
                [row for row in classification_rows if row["bottleneck_role_label"] == "bottleneck_candidate"]
            ),
            "capacity_response_operator_count": len(
                [
                    row
                    for row in classification_rows
                    if row["bottleneck_role_label"] == "capacity_response_operator"
                ]
            ),
            "supply_chain_beneficiary_count": len(
                [row for row in classification_rows if row["bottleneck_role_label"] == "supply_chain_beneficiary"]
            ),
        },
    }
