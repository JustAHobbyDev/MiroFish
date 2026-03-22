"""
Build a foreign-name review handoff from the foreign-access follow-up queue.
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


def _review_priority(row: Dict[str, Any]) -> str:
    followup_type = _coerce_string(row.get("followup_type"))
    final_expression = _coerce_string(row.get("final_expression"))
    if followup_type == "us_secondary_access_followup" and final_expression in {"shares", "leaps_call"}:
        return "highest"
    if final_expression in {"shares", "leaps_call"}:
        return "high"
    return "medium"


def build_public_market_foreign_review_handoff(
    foreign_access_followup_batch: Dict[str, Any],
    public_market_review_surface_batch: Dict[str, Any],
    public_market_pick_batch: Dict[str, Any],
) -> Dict[str, Any]:
    review_by_name = _index(public_market_review_surface_batch.get("rows", []))
    pick_by_name = _index(public_market_pick_batch.get("rows", []))
    handoff_rows: List[Dict[str, Any]] = []

    for row in foreign_access_followup_batch.get("followup_rows", []):
        name = _coerce_string(row.get("name"))
        review_row = review_by_name.get(name, {})
        pick_row = pick_by_name.get(name, {})
        priority = _review_priority(row)

        handoff_rows.append(
            {
                "name": name,
                "canonical_entity_name": _coerce_string(row.get("canonical_entity_name")),
                "underlying": _coerce_string(row.get("underlying")),
                "market_theme": _coerce_string(row.get("market_theme")),
                "role_label": _coerce_string(review_row.get("role_label")),
                "foreign_review_priority": priority,
                "followup_type": _coerce_string(row.get("followup_type")),
                "followup_action": _coerce_string(row.get("followup_action")),
                "exchange_scope": _coerce_string(row.get("exchange_scope")),
                "us_accessibility_status": _coerce_string(row.get("us_accessibility_status")),
                "us_reference_present": bool(row.get("us_reference_present", False)),
                "final_expression": _coerce_string(row.get("final_expression")),
                "ranking_score": float((review_row.get("ranking_score") or pick_row.get("ranking_score") or 0.0)),
                "thesis": _coerce_string(pick_row.get("thesis")),
                "bottleneck_layer": _coerce_string(pick_row.get("bottleneck_layer")),
                "value_capture_layer": _coerce_string(pick_row.get("value_capture_layer")),
                "top_catalysts": list((pick_row.get("catalysts") or [])[:3]),
                "top_invalidations": list((pick_row.get("invalidations") or [])[:3]),
                "why_missed": list((pick_row.get("why_missed") or [])[:3]),
                "symbol_mapping_basis": _coerce_string(row.get("symbol_mapping_basis")),
                "symbol_mapping_evidence": dict(row.get("symbol_mapping_evidence") or {}),
            }
        )

    handoff_rows.sort(
        key=lambda row: (
            {"highest": 0, "high": 1, "medium": 2}.get(row["foreign_review_priority"], 3),
            -row["ranking_score"],
            row["name"],
        )
    )

    return {
        "name": "public_market_foreign_review_handoff_v1",
        "handoff_rows": handoff_rows,
        "metrics": {
            "input_followup_row_count": len(foreign_access_followup_batch.get("followup_rows", [])),
            "handoff_count": len(handoff_rows),
            "highest_priority_count": len(
                [row for row in handoff_rows if row["foreign_review_priority"] == "highest"]
            ),
            "high_priority_count": len(
                [row for row in handoff_rows if row["foreign_review_priority"] == "high"]
            ),
        },
    }
