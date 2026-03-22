"""
Deterministic private-market follow-up planning for non-public handoff rows.
"""

from __future__ import annotations

from typing import Any, Dict, List


def _coerce_string(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def _followup_status(row: Dict[str, Any]) -> str:
    handoff_status = _coerce_string(row.get("market_handoff_status"))
    if handoff_status == "supplier_chain_followup":
        return "private_supplier_chain_followup"
    if handoff_status == "private_watchlist_only":
        return "private_capacity_watchlist_followup"
    return "out_of_scope"


def _followup_action(row: Dict[str, Any], status: str) -> str:
    if status == "private_supplier_chain_followup":
        return "map_public_customers_suppliers_and_parent_expressions"
    if status == "private_capacity_watchlist_followup":
        return "track_private_capacity_financing_and_public_counterparties"
    return "no_private_followup_action"


def _priority_sources(row: Dict[str, Any], status: str) -> List[str]:
    if status == "private_supplier_chain_followup":
        return [
            "official_company_site",
            "official_press_releases",
            "trade_press",
            "public_customer_filings",
            "public_supplier_filings",
        ]
    if status == "private_capacity_watchlist_followup":
        return [
            "official_company_site",
            "financing_announcements",
            "private_credit_or_abs_materials",
            "trade_press",
            "public_utility_counterparty_filings",
        ]
    return []


def build_private_market_followup_batch(
    market_handoff_batch: Dict[str, Any],
) -> Dict[str, Any]:
    followup_rows: List[Dict[str, Any]] = []

    for row in market_handoff_batch.get("handoff_rows", []):
        if _coerce_string(row.get("support_route_type")) != "private_company":
            continue

        status = _followup_status(row)
        if status == "out_of_scope":
            continue

        followup_rows.append(
            {
                "system_label": _coerce_string(row.get("system_label")),
                "canonical_entity_name": _coerce_string(row.get("canonical_entity_name")),
                "resolved_issuer_name": _coerce_string(row.get("resolved_issuer_name")),
                "entity_role": _coerce_string(row.get("entity_role")),
                "role_lane": _coerce_string(row.get("role_lane")),
                "market_handoff_status": _coerce_string(row.get("market_handoff_status")),
                "private_followup_status": status,
                "private_followup_action": _followup_action(row, status),
                "priority_source_classes": _priority_sources(row, status),
                "route_aware_priority_score": int(row.get("route_aware_priority_score", 0)),
                "route_aware_priority_tier": _coerce_string(row.get("route_aware_priority_tier")),
            }
        )

    followup_rows.sort(
        key=lambda item: (
            item["system_label"],
            0 if item["private_followup_status"] == "private_supplier_chain_followup" else 1,
            -item["route_aware_priority_score"],
            item["canonical_entity_name"],
        )
    )

    return {
        "name": "private_market_followup_batch_v1",
        "followup_rows": followup_rows,
        "metrics": {
            "input_handoff_row_count": len(market_handoff_batch.get("handoff_rows", [])),
            "private_followup_count": len(followup_rows),
            "private_supplier_chain_followup_count": len(
                [row for row in followup_rows if row["private_followup_status"] == "private_supplier_chain_followup"]
            ),
            "private_capacity_watchlist_followup_count": len(
                [row for row in followup_rows if row["private_followup_status"] == "private_capacity_watchlist_followup"]
            ),
        },
    }
