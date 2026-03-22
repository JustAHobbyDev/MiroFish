"""
Build an assessment summary over deterministic public market pick output.
"""

from __future__ import annotations

from typing import Any, Dict, List


def _coerce_string(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def _role_label_from_candidate(candidate_row: Dict[str, Any]) -> str:
    mispricing_type = _coerce_string(candidate_row.get("mispricing_type"))
    if mispricing_type == "hidden_bottleneck":
        return "bottleneck_candidate"
    if mispricing_type == "capacity_response_operator":
        return "capacity_response_operator"
    return "supply_chain_beneficiary"


def _candidate_index(candidate_batch: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    return {
        _coerce_string(row.get("name")): row
        for row in candidate_batch.get("rows", [])
        if _coerce_string(row.get("name"))
    }


def _empty_expression_counts() -> Dict[str, int]:
    return {
        "shares": 0,
        "leaps_call": 0,
        "reject": 0,
    }


def build_public_market_pick_assessment_batch(
    public_market_pick_batch: Dict[str, Any],
    public_market_scan_candidate_batch: Dict[str, Any],
) -> Dict[str, Any]:
    candidate_by_name = _candidate_index(public_market_scan_candidate_batch)

    role_expression_counts: Dict[str, Dict[str, int]] = {}
    market_theme_expression_counts: Dict[str, Dict[str, int]] = {}
    exchange_scope_expression_counts: Dict[str, Dict[str, int]] = {}
    assessment_rows: List[Dict[str, Any]] = []

    for pick_row in public_market_pick_batch.get("rows", []):
        name = _coerce_string(pick_row.get("name"))
        candidate_row = candidate_by_name.get(name, {})
        role_label = _role_label_from_candidate(candidate_row)
        market_theme = _coerce_string(pick_row.get("market_theme"))
        final_expression = _coerce_string(pick_row.get("final_expression"))
        exchange_scope = _coerce_string(candidate_row.get("market_data_checks", {}).get("exchange_scope"))

        role_expression_counts.setdefault(role_label, _empty_expression_counts())[final_expression] += 1
        market_theme_expression_counts.setdefault(market_theme, _empty_expression_counts())[final_expression] += 1
        exchange_scope_expression_counts.setdefault(exchange_scope or "unknown", _empty_expression_counts())[
            final_expression
        ] += 1

        assessment_rows.append(
            {
                "name": name,
                "underlying": _coerce_string(pick_row.get("underlying")),
                "market_theme": market_theme,
                "role_label": role_label,
                "exchange_scope": exchange_scope,
                "promotion_status": _coerce_string(pick_row.get("promotion_status")),
                "final_expression": final_expression,
                "ranking_score": float(pick_row.get("ranking_score", 0.0)),
            }
        )

    assessment_rows.sort(
        key=lambda row: (
            {
                "shares": 0,
                "leaps_call": 1,
                "reject": 2,
            }.get(row["final_expression"], 3),
            {
                "bottleneck_candidate": 0,
                "supply_chain_beneficiary": 1,
                "capacity_response_operator": 2,
            }.get(row["role_label"], 3),
            -row["ranking_score"],
            row["name"],
        )
    )

    return {
        "name": "public_market_pick_assessment_batch_v1",
        "assessment_rows": assessment_rows,
        "metrics": {
            "input_pick_row_count": len(public_market_pick_batch.get("rows", [])),
            "shares_count": len([row for row in assessment_rows if row["final_expression"] == "shares"]),
            "leaps_call_count": len([row for row in assessment_rows if row["final_expression"] == "leaps_call"]),
            "reject_count": len([row for row in assessment_rows if row["final_expression"] == "reject"]),
            "foreign_home_market_expression_count": len(
                [
                    row
                    for row in assessment_rows
                    if row["exchange_scope"] in {"foreign_home_market_code", "foreign_home_market_symbol"}
                ]
            ),
        },
        "role_expression_counts": role_expression_counts,
        "market_theme_expression_counts": market_theme_expression_counts,
        "exchange_scope_expression_counts": exchange_scope_expression_counts,
    }
