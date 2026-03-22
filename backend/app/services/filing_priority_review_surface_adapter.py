"""
Adapt filing-backed priority rows into the route-review surface shape.
"""

from __future__ import annotations

from typing import Any, Dict, List


def _coerce_string(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def build_filing_priority_review_surface_batch(
    filing_priority_batch: Dict[str, Any],
) -> Dict[str, Any]:
    rows: List[Dict[str, Any]] = []

    for row in filing_priority_batch.get("priority_rows", []):
        filing_support_status = _coerce_string(row.get("filing_support_status"))
        route_aware_tier = _coerce_string(row.get("filing_backed_priority_tier"))
        rows.append(
            {
                "origin_priority_batch": _coerce_string(filing_priority_batch.get("name")),
                "system_label": _coerce_string(row.get("system_label")),
                "canonical_entity_name": _coerce_string(row.get("canonical_entity_name")),
                "resolved_issuer_name": _coerce_string(row.get("resolved_issuer_name")),
                "entity_role": "equipment_or_component_supplier",
                "role_lane": "equipment_supplier",
                "base_priority_tier": _coerce_string(row.get("base_priority_tier")),
                "support_route_type": "public_filing" if filing_support_status == "supported" else "",
                "support_status": "supported_public_filing" if filing_support_status == "supported" else "not_yet_supported",
                "route_assessment": _coerce_string(row.get("filing_route_assessment")),
                "route_aware_priority_score": int(row.get("filing_backed_priority_score", 0)),
                "route_aware_priority_tier": route_aware_tier,
                "selection_action": "advance_with_public_filing_weight"
                if filing_support_status == "supported"
                else "hold_for_additional_source_coverage",
                "support_evidence_item_count": int(row.get("filing_evidence_item_count", 0)),
                "support_strong_evidence_item_count": int(row.get("filing_strong_evidence_item_count", 0)),
                "support_component_specific_count": int(row.get("filing_component_specific_count", 0)),
                "support_pressure_or_capacity_count": int(row.get("filing_pressure_or_capacity_count", 0)),
                "support_expansion_or_capex_count": int(row.get("filing_expansion_or_capex_count", 0)),
                "support_financing_or_capital_count": 0,
                "role_specific_evidence_summary": {},
                "source_classes": ["company_filing"],
                "top_support_evidence_items": list(row.get("top_filing_evidence_items", [])),
            }
        )

    rows.sort(
        key=lambda item: (
            item["system_label"],
            0 if item["support_status"] == "supported_public_filing" else 1,
            {"high": 0, "medium": 1, "low": 2}.get(item["route_aware_priority_tier"], 3),
            -item["route_aware_priority_score"],
            item["canonical_entity_name"],
        )
    )

    return {
        "name": "filing_priority_review_surface_batch_v1",
        "rows": rows,
        "rows_by_lane": {
            system_label: [row for row in rows if row["system_label"] == system_label]
            for system_label in sorted({row["system_label"] for row in rows})
        },
        "metrics": {
            "input_priority_row_count": len(filing_priority_batch.get("priority_rows", [])),
            "row_count": len(rows),
            "supported_public_count": len(
                [row for row in rows if row["support_status"] == "supported_public_filing"]
            ),
            "high_priority_count": len(
                [row for row in rows if row["route_aware_priority_tier"] == "high"]
            ),
        },
    }
