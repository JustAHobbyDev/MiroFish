"""
Build a broker-agnostic execution handoff object from the final public execution queue.
"""

from __future__ import annotations

from typing import Any, Dict, List


def _coerce_string(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def _execution_priority(role_label: str, ranking_score: float) -> str:
    if role_label == "bottleneck_candidate" and ranking_score >= 80.0:
        return "highest"
    if ranking_score >= 65.0:
        return "high"
    return "medium"


def _execution_note(row: Dict[str, Any]) -> str:
    role_label = _coerce_string(row.get("role_label"))
    if role_label == "bottleneck_candidate":
        return "Upstream constrained-layer exposure with direct U.S. execution path."
    if role_label == "supply_chain_beneficiary":
        return "Supplier exposure is actionable, but bottleneck proof is weaker than the top queue name."
    return "Actionable under current policy, but role evidence is not top-tier."


def build_public_market_execution_handoff(
    public_market_execution_queue_batch: Dict[str, Any],
) -> Dict[str, Any]:
    handoff_rows: List[Dict[str, Any]] = []

    for row in public_market_execution_queue_batch.get("queue_rows", []):
        ranking_score = float(row.get("ranking_score", 0.0))
        handoff_rows.append(
            {
                "name": _coerce_string(row.get("name")),
                "canonical_entity_name": _coerce_string(row.get("canonical_entity_name")),
                "underlying": _coerce_string(row.get("underlying")),
                "execution_expression": _coerce_string(row.get("final_expression")),
                "execution_policy_action": _coerce_string(row.get("execution_policy_action")),
                "execution_priority": _execution_priority(
                    _coerce_string(row.get("role_label")),
                    ranking_score,
                ),
                "market_theme": _coerce_string(row.get("market_theme")),
                "role_label": _coerce_string(row.get("role_label")),
                "ranking_score": ranking_score,
                "promotion_status": _coerce_string(row.get("promotion_status")),
                "mispricing_score_0_to_100": float(row.get("mispricing_score_0_to_100", 0.0)),
                "stock_fit_score_0_to_100": float(row.get("stock_fit_score_0_to_100", 0.0)),
                "thesis": _coerce_string(row.get("thesis")),
                "bottleneck_layer": _coerce_string(row.get("bottleneck_layer")),
                "value_capture_layer": _coerce_string(row.get("value_capture_layer")),
                "top_catalysts": list(row.get("top_catalysts", [])),
                "top_invalidations": list(row.get("top_invalidations", [])),
                "why_missed": list(row.get("why_missed", [])),
                "execution_readiness_note": _execution_note(row),
            }
        )

    handoff_rows.sort(
        key=lambda row: (
            {"highest": 0, "high": 1, "medium": 2}.get(row["execution_priority"], 3),
            -row["ranking_score"],
            row["name"],
        )
    )

    return {
        "name": "public_market_execution_handoff_v1",
        "handoff_rows": handoff_rows,
        "metrics": {
            "input_queue_row_count": len(public_market_execution_queue_batch.get("queue_rows", [])),
            "handoff_count": len(handoff_rows),
            "highest_priority_count": len(
                [row for row in handoff_rows if row["execution_priority"] == "highest"]
            ),
            "high_priority_count": len(
                [row for row in handoff_rows if row["execution_priority"] == "high"]
            ),
        },
    }
