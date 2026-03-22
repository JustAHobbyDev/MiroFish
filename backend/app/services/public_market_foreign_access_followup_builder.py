"""
Build a deterministic foreign-access follow-up queue for non-U.S.-primary public names.
"""

from __future__ import annotations

from typing import Any, Dict, List


def _coerce_string(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def _followup_type(status: str) -> str:
    if status == "foreign_home_with_us_reference":
        return "us_secondary_access_followup"
    return "home_market_or_proxy_followup"


def _followup_action(status: str) -> str:
    if status == "foreign_home_with_us_reference":
        return "confirm_adr_or_otc_symbol_and_check_basic_liquidity"
    return "decide_home_market_execution_or_find_us_proxy_expression"


def _priority_rank(final_expression: str, status: str) -> int:
    expression_rank = {
        "shares": 0,
        "leaps_call": 1,
        "reject": 2,
    }.get(final_expression, 3)
    status_rank = {
        "foreign_home_with_us_reference": 0,
        "foreign_home_market_only": 1,
        "accessibility_unknown": 2,
    }.get(status, 3)
    return expression_rank * 10 + status_rank


def build_public_market_foreign_access_followup_batch(
    public_market_us_accessibility_batch: Dict[str, Any],
) -> Dict[str, Any]:
    followup_rows: List[Dict[str, Any]] = []

    for row in public_market_us_accessibility_batch.get("accessibility_rows", []):
        status = _coerce_string(row.get("us_accessibility_status"))
        if status == "us_direct_primary":
            continue

        final_expression = _coerce_string(row.get("final_expression"))
        followup_rows.append(
            {
                "name": _coerce_string(row.get("name")),
                "canonical_entity_name": _coerce_string(row.get("canonical_entity_name")),
                "underlying": _coerce_string(row.get("underlying")),
                "market_theme": _coerce_string(row.get("market_theme")),
                "final_expression": final_expression,
                "exchange_scope": _coerce_string(row.get("exchange_scope")),
                "us_accessibility_status": status,
                "followup_type": _followup_type(status),
                "followup_action": _followup_action(status),
                "us_reference_present": bool(row.get("us_reference_present", False)),
                "symbol_mapping_basis": _coerce_string(row.get("symbol_mapping_basis")),
                "symbol_mapping_evidence": dict(row.get("symbol_mapping_evidence", {})),
            }
        )

    followup_rows.sort(
        key=lambda row: (
            _priority_rank(row["final_expression"], row["us_accessibility_status"]),
            row["market_theme"],
            row["canonical_entity_name"],
        )
    )

    return {
        "name": "public_market_foreign_access_followup_batch_v1",
        "followup_rows": followup_rows,
        "metrics": {
            "input_accessibility_row_count": len(public_market_us_accessibility_batch.get("accessibility_rows", [])),
            "followup_count": len(followup_rows),
            "us_secondary_access_followup_count": len(
                [row for row in followup_rows if row["followup_type"] == "us_secondary_access_followup"]
            ),
            "home_market_or_proxy_followup_count": len(
                [row for row in followup_rows if row["followup_type"] == "home_market_or_proxy_followup"]
            ),
        },
    }
