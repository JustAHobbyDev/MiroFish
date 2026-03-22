"""
Deterministic attachment of filing evidence back to bounded entity expansions.
"""

from __future__ import annotations

from typing import Any, Dict, List


def _coerce_string(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def _index_evidence_by_entity(evidence_batch: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    index: Dict[str, Dict[str, Any]] = {}
    for collection in evidence_batch.get("evidence_collections", []):
        canonical_entity_name = _coerce_string(collection.get("canonical_entity_name"))
        if not canonical_entity_name:
            continue
        index[canonical_entity_name] = collection
    return index


def build_bounded_entity_filing_support_batch(
    entity_expansion_batch: Dict[str, Any],
    evidence_batch: Dict[str, Any],
) -> Dict[str, Any]:
    evidence_index = _index_evidence_by_entity(evidence_batch)
    support_rows: List[Dict[str, Any]] = []

    for expansion in entity_expansion_batch.get("expansions", []):
        canonical_entity_name = _coerce_string(expansion.get("canonical_entity_name"))
        evidence_collection = evidence_index.get(canonical_entity_name, {})
        summary = evidence_collection.get("summary", {})
        strong_count = int(summary.get("strong_evidence_item_count", 0))
        total_count = int(summary.get("evidence_item_count", 0))
        support_rows.append(
            {
                "canonical_entity_name": canonical_entity_name,
                "system_label": _coerce_string(expansion.get("system_label")),
                "priority_tier": _coerce_string(expansion.get("priority_tier")),
                "resolved_issuer_name": _coerce_string(evidence_collection.get("resolved_issuer_name")),
                "filing_route_assessment": _coerce_string(evidence_collection.get("filing_route_assessment")),
                "filing_evidence_item_count": total_count,
                "filing_strong_evidence_item_count": strong_count,
                "filing_component_specific_count": int(summary.get("family_counts", {}).get("component_specific", 0)),
                "filing_pressure_or_capacity_count": int(summary.get("family_counts", {}).get("pressure_or_capacity", 0)),
                "filing_expansion_or_capex_count": int(summary.get("family_counts", {}).get("expansion_or_capex", 0)),
                "filing_support_status": "supported" if strong_count > 0 else "not_yet_supported",
                "top_filing_evidence_items": list(evidence_collection.get("evidence_items", []))[:5],
            }
        )

    support_rows.sort(
        key=lambda item: (
            0 if item["filing_support_status"] == "supported" else 1,
            -item["filing_strong_evidence_item_count"],
            {"high": 0, "medium": 1, "low": 2}.get(item["priority_tier"], 3),
            item["canonical_entity_name"],
        )
    )
    return {
        "name": "bounded_entity_filing_support_batch_v1",
        "support_rows": support_rows,
        "metrics": {
            "input_entity_expansion_count": len(entity_expansion_batch.get("expansions", [])),
            "supported_entity_count": len([row for row in support_rows if row["filing_support_status"] == "supported"]),
        },
    }
