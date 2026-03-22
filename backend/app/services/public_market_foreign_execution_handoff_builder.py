"""
Build a final broker-agnostic foreign review handoff from the foreign review queue.
"""

from __future__ import annotations

from typing import Any, Dict, List


def _coerce_string(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def build_public_market_foreign_execution_handoff(
    public_market_foreign_review_handoff_batch: Dict[str, Any],
) -> Dict[str, Any]:
    handoff_rows: List[Dict[str, Any]] = []

    for row in public_market_foreign_review_handoff_batch.get("handoff_rows", []):
        handoff_rows.append(
            {
                "name": _coerce_string(row.get("name")),
                "canonical_entity_name": _coerce_string(row.get("canonical_entity_name")),
                "underlying": _coerce_string(row.get("underlying")),
                "market_theme": _coerce_string(row.get("market_theme")),
                "role_label": _coerce_string(row.get("role_label")),
                "foreign_review_priority": _coerce_string(row.get("foreign_review_priority")),
                "followup_type": _coerce_string(row.get("followup_type")),
                "followup_action": _coerce_string(row.get("followup_action")),
                "exchange_scope": _coerce_string(row.get("exchange_scope")),
                "us_accessibility_status": _coerce_string(row.get("us_accessibility_status")),
                "final_expression": _coerce_string(row.get("final_expression")),
                "ranking_score": float(row.get("ranking_score", 0.0)),
                "thesis": _coerce_string(row.get("thesis")),
                "bottleneck_layer": _coerce_string(row.get("bottleneck_layer")),
                "value_capture_layer": _coerce_string(row.get("value_capture_layer")),
                "top_catalysts": list(row.get("top_catalysts", [])),
                "top_invalidations": list(row.get("top_invalidations", [])),
                "why_missed": list(row.get("why_missed", [])),
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
        "name": "public_market_foreign_execution_handoff_v1",
        "handoff_rows": handoff_rows,
        "metrics": {
            "input_review_row_count": len(public_market_foreign_review_handoff_batch.get("handoff_rows", [])),
            "handoff_count": len(handoff_rows),
            "highest_priority_count": len(
                [row for row in handoff_rows if row["foreign_review_priority"] == "highest"]
            ),
            "high_priority_count": len(
                [row for row in handoff_rows if row["foreign_review_priority"] == "high"]
            ),
        },
    }
