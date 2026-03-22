"""
Build a final public execution queue from conservative execution policy output.
"""

from __future__ import annotations

from typing import Any, Dict, List


def _coerce_string(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def _index(rows: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    return {
        _coerce_string(row.get("name")): row
        for row in rows
        if _coerce_string(row.get("name"))
    }


def build_public_market_execution_queue(
    execution_policy_batch: Dict[str, Any],
    public_market_review_surface_batch: Dict[str, Any],
    public_market_pick_batch: Dict[str, Any],
) -> Dict[str, Any]:
    review_by_name = _index(public_market_review_surface_batch.get("rows", []))
    pick_by_name = _index(public_market_pick_batch.get("rows", []))

    queue_rows: List[Dict[str, Any]] = []
    for policy_row in execution_policy_batch.get("policy_rows", []):
        if _coerce_string(policy_row.get("execution_policy_status")) != "default_us_executable":
            continue

        name = _coerce_string(policy_row.get("name"))
        review_row = review_by_name.get(name, {})
        pick_row = pick_by_name.get(name, {})

        queue_rows.append(
            {
                "name": name,
                "canonical_entity_name": _coerce_string(policy_row.get("canonical_entity_name")),
                "underlying": _coerce_string(policy_row.get("underlying")),
                "market_theme": _coerce_string(policy_row.get("market_theme")),
                "role_label": _coerce_string(policy_row.get("role_label")),
                "final_expression": _coerce_string(policy_row.get("final_expression")),
                "execution_policy_status": _coerce_string(policy_row.get("execution_policy_status")),
                "execution_policy_action": _coerce_string(policy_row.get("execution_policy_action")),
                "ranking_score": float(policy_row.get("ranking_score", 0.0)),
                "promotion_status": _coerce_string(pick_row.get("promotion_status")),
                "promotion_score_0_to_100": float(pick_row.get("promotion_score_0_to_100", 0.0)),
                "pick_score": float(pick_row.get("pick_score", 0.0)),
                "mispricing_score_0_to_100": float(
                    (pick_row.get("mispricing") or {}).get("score_0_to_100", 0.0)
                ),
                "stock_fit_score_0_to_100": float(
                    (pick_row.get("stock_fit") or {}).get("score_0_to_100", 0.0)
                ),
                "exchange_scope": _coerce_string(review_row.get("exchange_scope")),
                "us_accessibility_status": _coerce_string(review_row.get("us_accessibility_status")),
                "thesis": _coerce_string(pick_row.get("thesis")),
                "bottleneck_layer": _coerce_string(pick_row.get("bottleneck_layer")),
                "value_capture_layer": _coerce_string(pick_row.get("value_capture_layer")),
                "top_catalysts": list((pick_row.get("catalysts") or [])[:3]),
                "top_invalidations": list((pick_row.get("invalidations") or [])[:3]),
                "why_missed": list((pick_row.get("why_missed") or [])[:3]),
                "market_data_checks": dict(pick_row.get("market_data_checks") or {}),
            }
        )

    queue_rows.sort(
        key=lambda row: (
            {
                "bottleneck_candidate": 0,
                "supply_chain_beneficiary": 1,
                "capacity_response_operator": 2,
                "": 3,
            }.get(row["role_label"], 4),
            -row["ranking_score"],
            row["name"],
        )
    )

    return {
        "name": "public_market_execution_queue_v1",
        "queue_rows": queue_rows,
        "metrics": {
            "input_policy_row_count": len(execution_policy_batch.get("policy_rows", [])),
            "execution_queue_count": len(queue_rows),
            "bottleneck_candidate_count": len(
                [row for row in queue_rows if row["role_label"] == "bottleneck_candidate"]
            ),
            "supply_chain_beneficiary_count": len(
                [row for row in queue_rows if row["role_label"] == "supply_chain_beneficiary"]
            ),
        },
    }
