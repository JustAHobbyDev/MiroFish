"""
Build a consolidated multi-lane review surface from route-aware priority batches.
"""

from __future__ import annotations

from typing import Any, Dict, List


def _coerce_string(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def _normalized_rows(route_priority_batches: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for batch in route_priority_batches:
        origin_name = _coerce_string(batch.get("name"))
        for row in batch.get("priority_rows", []):
            rows.append(
                {
                    "origin_priority_batch": origin_name,
                    "system_label": _coerce_string(row.get("system_label")),
                    "canonical_entity_name": _coerce_string(row.get("canonical_entity_name")),
                    "resolved_issuer_name": _coerce_string(row.get("resolved_issuer_name")),
                    "entity_role": _coerce_string(row.get("entity_role")),
                    "role_lane": _coerce_string(row.get("role_lane")),
                    "base_priority_tier": _coerce_string(row.get("priority_tier")),
                    "support_route_type": _coerce_string(row.get("support_route_type")),
                    "support_status": _coerce_string(row.get("support_status")),
                    "route_assessment": _coerce_string(row.get("route_assessment")),
                    "route_aware_priority_score": int(row.get("route_aware_priority_score", 0)),
                    "route_aware_priority_tier": _coerce_string(row.get("route_aware_priority_tier")),
                    "selection_action": _coerce_string(row.get("selection_action")),
                    "support_evidence_item_count": int(row.get("support_evidence_item_count", 0)),
                    "support_strong_evidence_item_count": int(
                        row.get("support_strong_evidence_item_count", 0)
                    ),
                    "support_component_specific_count": int(
                        row.get("support_component_specific_count", 0)
                    ),
                    "support_pressure_or_capacity_count": int(
                        row.get("support_pressure_or_capacity_count", 0)
                    ),
                    "support_expansion_or_capex_count": int(
                        row.get("support_expansion_or_capex_count", 0)
                    ),
                    "support_financing_or_capital_count": int(
                        row.get("support_financing_or_capital_count", 0)
                    ),
                    "role_specific_evidence_summary": dict(
                        row.get("role_specific_evidence_summary", {})
                    ),
                    "source_classes": list(row.get("source_classes", [])),
                    "top_support_evidence_items": list(row.get("top_support_evidence_items", [])),
                }
            )
    return rows


def _lane_metrics(rows: List[Dict[str, Any]]) -> Dict[str, Dict[str, int]]:
    metrics: Dict[str, Dict[str, int]] = {}
    for row in rows:
        system_label = _coerce_string(row.get("system_label"))
        lane = metrics.setdefault(
            system_label,
            {
                "row_count": 0,
                "supported_public_count": 0,
                "supported_private_count": 0,
                "high_priority_count": 0,
            },
        )
        lane["row_count"] += 1
        if _coerce_string(row.get("support_status")) == "supported_public_filing":
            lane["supported_public_count"] += 1
        if _coerce_string(row.get("support_status")) == "supported_private_company":
            lane["supported_private_count"] += 1
        if _coerce_string(row.get("route_aware_priority_tier")) == "high":
            lane["high_priority_count"] += 1
    return metrics


def build_bounded_entity_route_review_surface(
    route_priority_batches: List[Dict[str, Any]],
) -> Dict[str, Any]:
    rows = _normalized_rows(route_priority_batches)
    rows.sort(
        key=lambda item: (
            item["system_label"],
            0 if item["support_status"] == "supported_public_filing" else 1,
            {"high": 0, "medium": 1, "low": 2}.get(item["route_aware_priority_tier"], 3),
            -item["route_aware_priority_score"],
            item["canonical_entity_name"],
        )
    )

    rows_by_lane: Dict[str, List[Dict[str, Any]]] = {}
    for row in rows:
        rows_by_lane.setdefault(row["system_label"], []).append(row)

    return {
        "name": "bounded_entity_route_review_surface_v1",
        "rows": rows,
        "rows_by_lane": rows_by_lane,
        "metrics": {
            "input_priority_batch_count": len(route_priority_batches),
            "row_count": len(rows),
            "supported_public_count": len(
                [row for row in rows if row["support_status"] == "supported_public_filing"]
            ),
            "supported_private_count": len(
                [row for row in rows if row["support_status"] == "supported_private_company"]
            ),
            "lane_metrics": _lane_metrics(rows),
        },
    }
