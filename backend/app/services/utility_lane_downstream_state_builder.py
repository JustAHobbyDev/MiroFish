"""
Deterministic consolidation of utility-lane downstream state.
"""

from __future__ import annotations

from typing import Any, Dict, List


def _coerce_string(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def _support_index(filing_support_batch: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    index: Dict[str, Dict[str, Any]] = {}
    for row in filing_support_batch.get("support_rows", []):
        entity_name = _coerce_string(row.get("canonical_entity_name"))
        if entity_name:
            index[entity_name] = row
    return index


def _private_index(private_diligence_batch: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    index: Dict[str, Dict[str, Any]] = {}
    for plan in private_diligence_batch.get("plans", []):
        entity_name = _coerce_string(plan.get("canonical_entity_name"))
        if entity_name:
            index[entity_name] = plan
    return index


def build_utility_lane_downstream_state(
    followup_queue_batch: Dict[str, Any],
    filing_support_batch: Dict[str, Any],
    private_diligence_batch: Dict[str, Any],
) -> Dict[str, Any]:
    support_index = _support_index(filing_support_batch)
    private_index = _private_index(private_diligence_batch)
    rows: List[Dict[str, Any]] = []

    for row in followup_queue_batch.get("queue_rows", []):
        entity_name = _coerce_string(row.get("canonical_entity_name"))
        support = support_index.get(entity_name, {})
        private_plan = private_index.get(entity_name, {})
        downstream_status = "public_filing_supported"
        if private_plan:
            downstream_status = "private_company_diligence_required"
        rows.append(
            {
                "canonical_entity_name": entity_name,
                "system_label": _coerce_string(row.get("system_label")),
                "entity_role": _coerce_string(row.get("entity_role")),
                "priority_tier": _coerce_string(row.get("priority_tier")),
                "followup_status": _coerce_string(row.get("filing_followup_status")),
                "downstream_status": downstream_status,
                "resolved_issuer_name": (
                    _coerce_string(private_plan.get("resolved_issuer_name"))
                    or _coerce_string(row.get("existing_resolved_issuer_name"))
                    or _coerce_string(support.get("resolved_issuer_name"))
                ),
                "filing_route_assessment": (
                    _coerce_string(private_plan.get("origin_live_resolution_result", {}).get("filing_route_assessment"))
                    or _coerce_string(support.get("filing_route_assessment"))
                ),
                "filing_support_status": _coerce_string(support.get("filing_support_status")),
                "filing_strong_evidence_item_count": int(
                    support.get("filing_strong_evidence_item_count", 0)
                ),
                "private_diligence_plan_id": _coerce_string(
                    private_plan.get("private_company_diligence_plan_id")
                ),
                "next_action": (
                    "run_private_company_diligence"
                    if private_plan
                    else "reuse_existing_filing_support"
                ),
            }
        )

    rows.sort(
        key=lambda item: (
            0 if item["downstream_status"] == "public_filing_supported" else 1,
            {"high": 0, "medium": 1, "low": 2}.get(item["priority_tier"], 3),
            -item["filing_strong_evidence_item_count"],
            item["canonical_entity_name"],
        )
    )
    return {
        "name": "utility_lane_downstream_state_v1",
        "rows": rows,
        "metrics": {
            "input_queue_count": len(followup_queue_batch.get("queue_rows", [])),
            "public_filing_supported_count": len(
                [item for item in rows if item["downstream_status"] == "public_filing_supported"]
            ),
            "private_company_diligence_required_count": len(
                [item for item in rows if item["downstream_status"] == "private_company_diligence_required"]
            ),
        },
    }
