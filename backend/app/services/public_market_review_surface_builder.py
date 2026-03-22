"""
Build a combined public market review surface from picks, assessment, accessibility,
and foreign-access follow-up.
"""

from __future__ import annotations

from typing import Any, Dict, List


def _coerce_string(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def _index(rows: List[Dict[str, Any]], key_field: str = "name") -> Dict[str, Dict[str, Any]]:
    return {
        _coerce_string(row.get(key_field)): row
        for row in rows
        if _coerce_string(row.get(key_field))
    }


def build_public_market_review_surface(
    public_market_pick_batch: Dict[str, Any],
    public_market_pick_assessment_batch: Dict[str, Any],
    public_market_us_accessibility_batch: Dict[str, Any],
    public_market_foreign_access_followup_batch: Dict[str, Any],
) -> Dict[str, Any]:
    assessment_by_name = _index(public_market_pick_assessment_batch.get("assessment_rows", []))
    accessibility_by_name = _index(public_market_us_accessibility_batch.get("accessibility_rows", []))
    followup_by_name = _index(public_market_foreign_access_followup_batch.get("followup_rows", []))

    rows: List[Dict[str, Any]] = []
    for pick_row in public_market_pick_batch.get("rows", []):
        name = _coerce_string(pick_row.get("name"))
        assessment_row = assessment_by_name.get(name, {})
        accessibility_row = accessibility_by_name.get(name, {})
        followup_row = followup_by_name.get(name, {})

        rows.append(
            {
                "name": name,
                "canonical_entity_name": _coerce_string(assessment_row.get("name") or accessibility_row.get("canonical_entity_name")),
                "underlying": _coerce_string(pick_row.get("underlying")),
                "market_theme": _coerce_string(pick_row.get("market_theme")),
                "role_label": _coerce_string(assessment_row.get("role_label")),
                "promotion_status": _coerce_string(pick_row.get("promotion_status")),
                "final_expression": _coerce_string(pick_row.get("final_expression")),
                "ranking_score": float(pick_row.get("ranking_score", 0.0)),
                "exchange_scope": _coerce_string(accessibility_row.get("exchange_scope")),
                "us_accessibility_status": _coerce_string(accessibility_row.get("us_accessibility_status")),
                "us_accessibility_action": _coerce_string(accessibility_row.get("us_accessibility_action")),
                "foreign_access_followup_type": _coerce_string(followup_row.get("followup_type")),
                "foreign_access_followup_action": _coerce_string(followup_row.get("followup_action")),
                "us_reference_present": bool(accessibility_row.get("us_reference_present", False)),
            }
        )

    rows.sort(
        key=lambda row: (
            {
                "shares": 0,
                "leaps_call": 1,
                "reject": 2,
            }.get(row["final_expression"], 3),
            {
                "us_direct_primary": 0,
                "foreign_home_with_us_reference": 1,
                "foreign_home_market_only": 2,
                "": 3,
            }.get(row["us_accessibility_status"], 4),
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
        "name": "public_market_review_surface_v1",
        "rows": rows,
        "metrics": {
            "input_pick_row_count": len(public_market_pick_batch.get("rows", [])),
            "review_row_count": len(rows),
            "actionable_expression_count": len(
                [row for row in rows if row["final_expression"] in {"shares", "leaps_call"}]
            ),
            "foreign_access_followup_count": len(
                [row for row in rows if row["foreign_access_followup_type"]]
            ),
        },
    }
