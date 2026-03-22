"""
Deterministic follow-up queue selection from bounded entity candidates.
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
        canonical_entity_name = _coerce_string(row.get("canonical_entity_name"))
        if canonical_entity_name:
            index[canonical_entity_name] = row
    return index


def build_bounded_entity_followup_queue(
    bounded_entity_candidate_batch: Dict[str, Any],
    filing_support_batch: Dict[str, Any],
    *,
    system_label: str,
    allowed_entity_roles: List[str],
) -> Dict[str, Any]:
    support_index = _support_index(filing_support_batch)
    allowed_roles = {_coerce_string(item) for item in allowed_entity_roles if _coerce_string(item)}
    queue_rows: List[Dict[str, Any]] = []

    for candidate in bounded_entity_candidate_batch.get("candidates", []):
        if _coerce_string(candidate.get("system_label")) != system_label:
            continue
        if _coerce_string(candidate.get("support_provenance_status")) != "real_only":
            continue
        entity_role = _coerce_string(candidate.get("entity_role"))
        if entity_role not in allowed_roles:
            continue

        entity_name = _coerce_string(candidate.get("entity_name"))
        support_row = support_index.get(entity_name, {})
        already_supported = _coerce_string(support_row.get("filing_support_status")) == "supported"
        queue_rows.append(
            {
                "canonical_entity_name": entity_name,
                "system_label": system_label,
                "entity_role": entity_role,
                "priority_tier": _coerce_string(candidate.get("priority_tier")) or "low",
                "source_classes": list(candidate.get("source_classes", [])),
                "support_provenance_status": _coerce_string(candidate.get("support_provenance_status")),
                "filing_followup_status": "already_supported" if already_supported else "needs_live_resolution",
                "existing_resolved_issuer_name": _coerce_string(support_row.get("resolved_issuer_name")),
                "next_action": (
                    "reuse_existing_filing_support"
                    if already_supported
                    else "resolve_issuer_and_collect_filing_route"
                ),
            }
        )

    queue_rows.sort(
        key=lambda item: (
            0 if item["filing_followup_status"] == "needs_live_resolution" else 1,
            {"high": 0, "medium": 1, "low": 2}.get(item["priority_tier"], 3),
            item["canonical_entity_name"],
        )
    )
    return {
        "name": "bounded_entity_followup_queue_v1",
        "queue_rows": queue_rows,
        "metrics": {
            "input_candidate_count": len(bounded_entity_candidate_batch.get("candidates", [])),
            "selected_queue_count": len(queue_rows),
            "already_supported_count": len(
                [row for row in queue_rows if row["filing_followup_status"] == "already_supported"]
            ),
            "needs_live_resolution_count": len(
                [row for row in queue_rows if row["filing_followup_status"] == "needs_live_resolution"]
            ),
        },
    }
