"""
Build a conservative execution policy layer from the combined public market review surface.
"""

from __future__ import annotations

from typing import Any, Dict, List


def _coerce_string(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def _execution_policy(row: Dict[str, Any]) -> str:
    final_expression = _coerce_string(row.get("final_expression"))
    accessibility = _coerce_string(row.get("us_accessibility_status"))
    if final_expression == "reject":
        return "blocked_by_pick_reject"
    if accessibility == "us_direct_primary":
        return "default_us_executable"
    if accessibility == "foreign_home_with_us_reference":
        return "requires_us_secondary_access_review"
    if accessibility == "foreign_home_market_only":
        return "requires_foreign_execution_review"
    return "execution_policy_unresolved"


def _execution_action(policy: str) -> str:
    return {
        "default_us_executable": "use_default_us_execution_path",
        "requires_us_secondary_access_review": "review_secondary_us_listing_before_execution",
        "requires_foreign_execution_review": "review_home_market_or_proxy_before_execution",
        "blocked_by_pick_reject": "do_not_forward_to_execution",
        "execution_policy_unresolved": "resolve_execution_path_before_forwarding",
    }.get(policy, "resolve_execution_path_before_forwarding")


def build_public_market_execution_policy_batch(
    public_market_review_surface_batch: Dict[str, Any],
) -> Dict[str, Any]:
    policy_rows: List[Dict[str, Any]] = []
    for row in public_market_review_surface_batch.get("rows", []):
        policy = _execution_policy(row)
        policy_rows.append(
            {
                "name": _coerce_string(row.get("name")),
                "canonical_entity_name": _coerce_string(row.get("canonical_entity_name")),
                "underlying": _coerce_string(row.get("underlying")),
                "market_theme": _coerce_string(row.get("market_theme")),
                "role_label": _coerce_string(row.get("role_label")),
                "final_expression": _coerce_string(row.get("final_expression")),
                "us_accessibility_status": _coerce_string(row.get("us_accessibility_status")),
                "execution_policy_status": policy,
                "execution_policy_action": _execution_action(policy),
                "foreign_access_followup_type": _coerce_string(row.get("foreign_access_followup_type")),
                "ranking_score": float(row.get("ranking_score", 0.0)),
            }
        )

    policy_rows.sort(
        key=lambda row: (
            {
                "default_us_executable": 0,
                "requires_us_secondary_access_review": 1,
                "requires_foreign_execution_review": 2,
                "blocked_by_pick_reject": 3,
                "execution_policy_unresolved": 4,
            }.get(row["execution_policy_status"], 5),
            -row["ranking_score"],
            row["name"],
        )
    )

    return {
        "name": "public_market_execution_policy_batch_v1",
        "policy_rows": policy_rows,
        "metrics": {
            "input_review_row_count": len(public_market_review_surface_batch.get("rows", [])),
            "default_us_executable_count": len(
                [row for row in policy_rows if row["execution_policy_status"] == "default_us_executable"]
            ),
            "requires_us_secondary_access_review_count": len(
                [
                    row
                    for row in policy_rows
                    if row["execution_policy_status"] == "requires_us_secondary_access_review"
                ]
            ),
            "requires_foreign_execution_review_count": len(
                [
                    row
                    for row in policy_rows
                    if row["execution_policy_status"] == "requires_foreign_execution_review"
                ]
            ),
            "blocked_by_pick_reject_count": len(
                [row for row in policy_rows if row["execution_policy_status"] == "blocked_by_pick_reject"]
            ),
        },
    }
