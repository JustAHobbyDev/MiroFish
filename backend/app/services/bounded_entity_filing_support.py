"""
Deterministic attachment of filing evidence back to bounded entity expansions.
"""

from __future__ import annotations

from typing import Any, Dict, List


def _coerce_string(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def _role_lane(expansion: Dict[str, Any]) -> str:
    entity_role = _coerce_string(expansion.get("entity_role"))
    title_text = " ".join(
        _coerce_string(item) for item in expansion.get("supporting_titles", []) if _coerce_string(item)
    ).lower()

    if any(token in title_text for token in ("factory", "factories", "manufacturing", "production", "plant", "equipment")):
        return "equipment_supplier"
    if any(token in title_text for token in ("load", "deal", "agreement", "pipeline", "utility", "interconnection", "generation")):
        return "utility_or_operator"

    if entity_role == "equipment_or_component_supplier":
        return "equipment_supplier"
    if entity_role in {"capacity_operator_or_owner", "power_or_utility_operator"}:
        return "utility_or_operator"
    return "general_beneficiary"


def _excerpt_contains(evidence_item: Dict[str, Any], tokens: List[str]) -> bool:
    excerpt = _coerce_string(evidence_item.get("excerpt")).lower()
    return any(token in excerpt for token in tokens)


def _utility_operator_summary(evidence_items: List[Dict[str, Any]]) -> Dict[str, int]:
    load_tokens = ["data center", "hyperscale", "large load", "load", "demand", "capacity"]
    grid_tokens = ["substation", "transformer", "switchgear", "generation", "interconnection", "grid investment"]

    load_and_demand_signal_count = 0
    grid_response_signal_count = 0
    capex_response_signal_count = 0

    for item in evidence_items:
        keyword = _coerce_string(item.get("keyword")).lower()
        family = _coerce_string(item.get("keyword_family")).lower()

        if keyword in {"data center", "hyperscale", "load", "capacity"} or (
            family in {"pressure_or_capacity", "system_context"} and _excerpt_contains(item, load_tokens)
        ):
            load_and_demand_signal_count += 1

        if keyword in {"substation", "transformer", "switchgear", "generation", "interconnection"} or (
            family in {"component_specific", "expansion_or_capex"} and _excerpt_contains(item, grid_tokens)
        ):
            grid_response_signal_count += 1

        if family == "expansion_or_capex":
            capex_response_signal_count += 1

    return {
        "load_and_demand_signal_count": load_and_demand_signal_count,
        "grid_response_signal_count": grid_response_signal_count,
        "capex_response_signal_count": capex_response_signal_count,
    }


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
        entity_role = _coerce_string(expansion.get("entity_role"))
        role_lane = _role_lane(expansion)
        evidence_collection = evidence_index.get(canonical_entity_name, {})
        summary = evidence_collection.get("summary", {})
        evidence_items = list(evidence_collection.get("evidence_items", []))
        strong_count = int(summary.get("strong_evidence_item_count", 0))
        total_count = int(summary.get("evidence_item_count", 0))
        support_rows.append(
            {
                "canonical_entity_name": canonical_entity_name,
                "system_label": _coerce_string(expansion.get("system_label")),
                "priority_tier": _coerce_string(expansion.get("priority_tier")),
                "entity_role": entity_role,
                "role_lane": role_lane,
                "resolved_issuer_name": _coerce_string(evidence_collection.get("resolved_issuer_name")),
                "filing_route_assessment": _coerce_string(evidence_collection.get("filing_route_assessment")),
                "filing_evidence_item_count": total_count,
                "filing_strong_evidence_item_count": strong_count,
                "filing_component_specific_count": int(summary.get("family_counts", {}).get("component_specific", 0)),
                "filing_pressure_or_capacity_count": int(summary.get("family_counts", {}).get("pressure_or_capacity", 0)),
                "filing_expansion_or_capex_count": int(summary.get("family_counts", {}).get("expansion_or_capex", 0)),
                "filing_support_status": "supported" if strong_count > 0 else "not_yet_supported",
                "role_specific_evidence_summary": (
                    _utility_operator_summary(evidence_items)
                    if role_lane == "utility_or_operator"
                    else {}
                ),
                "top_filing_evidence_items": evidence_items[:5],
            }
        )

    support_rows.sort(
        key=lambda item: (
            0 if item["filing_support_status"] == "supported" else 1,
            {"equipment_supplier": 0, "utility_or_operator": 1, "general_beneficiary": 2}.get(
                item["role_lane"], 3
            ),
            -item["filing_strong_evidence_item_count"],
            {"high": 0, "medium": 1, "low": 2}.get(item["priority_tier"], 3),
            item["canonical_entity_name"],
        )
    )
    support_rows_by_role_lane = {
        "equipment_supplier": [row for row in support_rows if row["role_lane"] == "equipment_supplier"],
        "utility_or_operator": [row for row in support_rows if row["role_lane"] == "utility_or_operator"],
        "general_beneficiary": [row for row in support_rows if row["role_lane"] == "general_beneficiary"],
    }
    return {
        "name": "bounded_entity_filing_support_batch_v1",
        "support_rows": support_rows,
        "support_rows_by_role_lane": support_rows_by_role_lane,
        "metrics": {
            "input_entity_expansion_count": len(entity_expansion_batch.get("expansions", [])),
            "supported_entity_count": len([row for row in support_rows if row["filing_support_status"] == "supported"]),
            "role_lane_counts": {
                lane: len(rows) for lane, rows in support_rows_by_role_lane.items()
            },
        },
    }
