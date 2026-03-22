"""
Build a single review surface for the utility and large-load power lane.
"""

from __future__ import annotations

from typing import Any, Dict, List


def _coerce_string(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def _queue_index(queue_batch: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    return {
        _coerce_string(row.get("canonical_entity_name")): row
        for row in queue_batch.get("queue_rows", [])
        if _coerce_string(row.get("canonical_entity_name"))
    }


def _support_index(support_batch: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    return {
        _coerce_string(row.get("canonical_entity_name")): row
        for row in support_batch.get("support_rows", [])
        if _coerce_string(row.get("canonical_entity_name"))
    }


def _private_index(collection_batch: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    return {
        _coerce_string(row.get("canonical_entity_name")): row
        for row in collection_batch.get("collections", [])
        if _coerce_string(row.get("canonical_entity_name"))
    }


def build_utility_lane_review_surface(
    downstream_state_batch: Dict[str, Any],
    followup_queue_batch: Dict[str, Any],
    filing_support_batch: Dict[str, Any],
    private_collection_batch: Dict[str, Any],
) -> Dict[str, Any]:
    queue_index = _queue_index(followup_queue_batch)
    support_index = _support_index(filing_support_batch)
    private_index = _private_index(private_collection_batch)
    rows: List[Dict[str, Any]] = []

    for row in downstream_state_batch.get("rows", []):
        entity_name = _coerce_string(row.get("canonical_entity_name"))
        queue_row = queue_index.get(entity_name, {})
        support_row = support_index.get(entity_name, {})
        private_row = private_index.get(entity_name, {})
        private_summary = dict(private_row.get("collection_summary", {}))
        role_specific = dict(support_row.get("role_specific_evidence_summary", {}))

        rows.append(
            {
                "canonical_entity_name": entity_name,
                "system_label": _coerce_string(row.get("system_label")),
                "entity_role": _coerce_string(row.get("entity_role")),
                "priority_tier": _coerce_string(row.get("priority_tier")),
                "downstream_status": _coerce_string(row.get("downstream_status")),
                "resolved_issuer_name": _coerce_string(row.get("resolved_issuer_name")),
                "review_route": (
                    "private_company_diligence"
                    if _coerce_string(row.get("downstream_status")) == "private_company_diligence_required"
                    else "public_filing_reuse"
                ),
                "supporting_source_classes": list(queue_row.get("source_classes", [])),
                "followup_status": _coerce_string(row.get("followup_status")),
                "filing_strong_evidence_item_count": int(
                    row.get("filing_strong_evidence_item_count", 0)
                ),
                "load_and_demand_signal_count": int(
                    role_specific.get("load_and_demand_signal_count", 0)
                ),
                "grid_response_signal_count": int(
                    role_specific.get("grid_response_signal_count", 0)
                ),
                "capex_response_signal_count": int(
                    role_specific.get("capex_response_signal_count", 0)
                ),
                "private_document_count": int(private_summary.get("document_count", 0)),
                "private_existing_document_count": int(
                    private_summary.get("existing_document_count", 0)
                ),
                "next_action": _coerce_string(row.get("next_action")),
            }
        )

    rows.sort(
        key=lambda item: (
            0 if item["review_route"] == "public_filing_reuse" else 1,
            {"high": 0, "medium": 1, "low": 2}.get(item["priority_tier"], 3),
            -item["filing_strong_evidence_item_count"],
            -item["private_existing_document_count"],
            item["canonical_entity_name"],
        )
    )

    return {
        "name": "utility_lane_review_surface_v1",
        "rows": rows,
        "metrics": {
            "input_downstream_row_count": len(downstream_state_batch.get("rows", [])),
            "public_filing_reuse_count": len(
                [row for row in rows if row["review_route"] == "public_filing_reuse"]
            ),
            "private_company_diligence_count": len(
                [row for row in rows if row["review_route"] == "private_company_diligence"]
            ),
        },
    }
