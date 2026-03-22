"""
Deterministic route-aware support attachment for bounded entity follow-up queues.
"""

from __future__ import annotations

from typing import Any, Dict, List


PRIVATE_SUBSTANTIVE_DOCUMENT_TYPES = {
    "official_press_release",
    "official_financing_announcement",
    "official_solution_page",
}
PRIVATE_LOW_SIGNAL_EXCERPT_MARKERS = (
    "contact careers login",
    "this is a search field with an auto-suggest feature attached",
    "additional services",
    "simulation solutions",
    "powertrain testing solutions",
    "resources press releases",
)


def _coerce_string(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def _role_lane(entity_role: str) -> str:
    role = _coerce_string(entity_role)
    if role == "equipment_or_component_supplier":
        return "equipment_supplier"
    if role in {"capacity_operator_or_owner", "power_or_utility_operator"}:
        return "utility_or_operator"
    return "general_beneficiary"


def _excerpt_contains(evidence_item: Dict[str, Any], tokens: List[str]) -> bool:
    excerpt = _coerce_string(evidence_item.get("excerpt")).lower()
    return any(token in excerpt for token in tokens)


def _utility_operator_summary(evidence_items: List[Dict[str, Any]]) -> Dict[str, int]:
    load_tokens = ["data center", "hyperscale", "large load", "load", "demand", "capacity"]
    grid_tokens = ["substation", "transformer", "switchgear", "generation", "interconnection", "grid"]

    load_and_demand_signal_count = 0
    grid_response_signal_count = 0
    capex_response_signal_count = 0

    for item in evidence_items:
        keyword = _coerce_string(item.get("keyword")).lower()
        family = _coerce_string(item.get("keyword_family")).lower()

        if keyword in {"data center", "hyperscale", "load", "capacity", "megawatt", "power"} or (
            family in {"pressure_or_capacity", "system_context"} and _excerpt_contains(item, load_tokens)
        ):
            load_and_demand_signal_count += 1

        if keyword in {"substation", "transformer", "switchgear", "generation", "interconnection", "grid", "generator", "engine"} or (
            family in {"component_specific", "expansion_or_capex"} and _excerpt_contains(item, grid_tokens)
        ):
            grid_response_signal_count += 1

        if family in {"expansion_or_capex", "financing_or_capital"}:
            capex_response_signal_count += 1

    return {
        "load_and_demand_signal_count": load_and_demand_signal_count,
        "grid_response_signal_count": grid_response_signal_count,
        "capex_response_signal_count": capex_response_signal_count,
    }


def _index_by_name(rows: List[Dict[str, Any]], key: str) -> Dict[str, Dict[str, Any]]:
    index: Dict[str, Dict[str, Any]] = {}
    for row in rows:
        name = _coerce_string(row.get(key))
        if name:
            index[name] = row
    return index


def _support_counts_from_private(summary: Dict[str, Any]) -> Dict[str, int]:
    families = dict(summary.get("family_counts", {}))
    return {
        "support_evidence_item_count": int(summary.get("evidence_item_count", 0)),
        "support_strong_evidence_item_count": int(summary.get("strong_evidence_item_count", 0)),
        "support_component_specific_count": int(families.get("component_specific", 0)),
        "support_pressure_or_capacity_count": int(families.get("pressure_or_capacity", 0)),
        "support_expansion_or_capex_count": int(families.get("expansion_or_capex", 0)),
        "support_financing_or_capital_count": int(families.get("financing_or_capital", 0)),
    }


def _support_counts_from_public(row: Dict[str, Any]) -> Dict[str, int]:
    return {
        "support_evidence_item_count": int(row.get("filing_evidence_item_count", 0)),
        "support_strong_evidence_item_count": int(row.get("filing_strong_evidence_item_count", 0)),
        "support_component_specific_count": int(row.get("filing_component_specific_count", 0)),
        "support_pressure_or_capacity_count": int(row.get("filing_pressure_or_capacity_count", 0)),
        "support_expansion_or_capex_count": int(row.get("filing_expansion_or_capex_count", 0)),
        "support_financing_or_capital_count": 0,
    }


def _private_substantive_evidence_items(collection: Dict[str, Any]) -> List[Dict[str, Any]]:
    items: List[Dict[str, Any]] = []
    for item in collection.get("evidence_items", []):
        excerpt = _coerce_string(item.get("excerpt")).lower()
        if _coerce_string(item.get("document_type")) in PRIVATE_SUBSTANTIVE_DOCUMENT_TYPES and not any(
            marker in excerpt for marker in PRIVATE_LOW_SIGNAL_EXCERPT_MARKERS
        ):
            items.append(item)
    return items


def _private_summary_from_items(evidence_items: List[Dict[str, Any]]) -> Dict[str, Any]:
    family_counts = {
        "component_specific": 0,
        "pressure_or_capacity": 0,
        "expansion_or_capex": 0,
        "financing_or_capital": 0,
        "system_context": 0,
        "other": 0,
    }
    strong_count = 0
    for item in evidence_items:
        family = _coerce_string(item.get("keyword_family")) or "other"
        family_counts[family] = family_counts.get(family, 0) + 1
        if _coerce_string(item.get("evidence_strength")) in {"high", "medium"}:
            strong_count += 1
    return {
        "evidence_item_count": len(evidence_items),
        "strong_evidence_item_count": strong_count,
        "family_counts": family_counts,
    }


def build_bounded_entity_route_support_batch(
    followup_queue_batch: Dict[str, Any],
    public_support_batch: Dict[str, Any],
    private_plan_batch: Dict[str, Any],
    private_evidence_batch: Dict[str, Any],
) -> Dict[str, Any]:
    public_index = _index_by_name(list(public_support_batch.get("support_rows", [])), "canonical_entity_name")
    private_plan_index = _index_by_name(list(private_plan_batch.get("plans", [])), "canonical_entity_name")
    private_evidence_index = _index_by_name(
        list(private_evidence_batch.get("evidence_collections", [])), "canonical_entity_name"
    )

    support_rows: List[Dict[str, Any]] = []

    for row in followup_queue_batch.get("queue_rows", []):
        canonical_entity_name = _coerce_string(row.get("canonical_entity_name"))
        role_lane = _role_lane(_coerce_string(row.get("entity_role")))
        public_row = public_index.get(canonical_entity_name, {})
        private_plan = private_plan_index.get(canonical_entity_name, {})
        private_evidence = private_evidence_index.get(canonical_entity_name, {})

        public_supported = _coerce_string(public_row.get("filing_support_status")) == "supported"
        private_evidence_items = _private_substantive_evidence_items(private_evidence)
        private_summary = _private_summary_from_items(private_evidence_items)
        private_supported = int(private_summary.get("strong_evidence_item_count", 0)) > 0
        has_private_plan = bool(private_plan)

        support_route_type = ""
        support_status = "not_yet_supported"
        resolved_issuer_name = ""
        route_assessment = ""
        support_counts = {
            "support_evidence_item_count": 0,
            "support_strong_evidence_item_count": 0,
            "support_component_specific_count": 0,
            "support_pressure_or_capacity_count": 0,
            "support_expansion_or_capex_count": 0,
            "support_financing_or_capital_count": 0,
        }
        top_support_evidence_items: List[Dict[str, Any]] = []
        role_specific_evidence_summary: Dict[str, int] = {}

        if public_supported:
            support_route_type = "public_filing"
            support_status = "supported_public_filing"
            resolved_issuer_name = _coerce_string(public_row.get("resolved_issuer_name"))
            route_assessment = _coerce_string(public_row.get("filing_route_assessment"))
            support_counts = _support_counts_from_public(public_row)
            top_support_evidence_items = list(public_row.get("top_filing_evidence_items", []))[:5]
            role_specific_evidence_summary = dict(public_row.get("role_specific_evidence_summary", {}))
        elif private_supported:
            support_route_type = "private_company"
            support_status = "supported_private_company"
            resolved_issuer_name = _coerce_string(private_evidence.get("resolved_issuer_name")) or _coerce_string(
                private_plan.get("resolved_issuer_name")
            )
            route_assessment = _coerce_string(private_plan.get("route_type")) or "private_company_official_company_route"
            support_counts = _support_counts_from_private(private_summary)
            top_support_evidence_items = private_evidence_items[:5]
            role_specific_evidence_summary = (
                _utility_operator_summary(private_evidence_items) if role_lane == "utility_or_operator" else {}
            )
        elif has_private_plan:
            support_route_type = "private_company"
            support_status = "private_company_planned"
            resolved_issuer_name = _coerce_string(private_plan.get("resolved_issuer_name"))
            route_assessment = _coerce_string(private_plan.get("route_type")) or "private_company_official_company_route"
        elif _coerce_string(row.get("filing_followup_status")) == "already_supported":
            support_route_type = "public_filing"
            support_status = "needs_public_support_refresh"
            resolved_issuer_name = _coerce_string(row.get("existing_resolved_issuer_name"))
        elif _coerce_string(row.get("filing_followup_status")) == "needs_live_resolution":
            support_status = "needs_live_resolution"

        support_rows.append(
            {
                "canonical_entity_name": canonical_entity_name,
                "system_label": _coerce_string(row.get("system_label")),
                "priority_tier": _coerce_string(row.get("priority_tier")),
                "entity_role": _coerce_string(row.get("entity_role")),
                "role_lane": role_lane,
                "source_classes": list(row.get("source_classes", [])),
                "support_provenance_status": _coerce_string(row.get("support_provenance_status")),
                "followup_status": _coerce_string(row.get("filing_followup_status")),
                "support_route_type": support_route_type,
                "support_status": support_status,
                "resolved_issuer_name": resolved_issuer_name,
                "route_assessment": route_assessment,
                **support_counts,
                "role_specific_evidence_summary": role_specific_evidence_summary,
                "top_support_evidence_items": top_support_evidence_items,
            }
        )

    support_rows.sort(
        key=lambda item: (
            {
                "supported_public_filing": 0,
                "supported_private_company": 1,
                "private_company_planned": 2,
                "needs_public_support_refresh": 3,
                "needs_live_resolution": 4,
                "not_yet_supported": 5,
            }.get(item["support_status"], 6),
            {"equipment_supplier": 0, "utility_or_operator": 1, "general_beneficiary": 2}.get(
                item["role_lane"], 3
            ),
            -item["support_strong_evidence_item_count"],
            item["canonical_entity_name"],
        )
    )

    return {
        "name": "bounded_entity_route_support_batch_v1",
        "support_rows": support_rows,
        "metrics": {
            "input_queue_count": len(followup_queue_batch.get("queue_rows", [])),
            "supported_public_count": len(
                [row for row in support_rows if row["support_status"] == "supported_public_filing"]
            ),
            "supported_private_count": len(
                [row for row in support_rows if row["support_status"] == "supported_private_company"]
            ),
            "planned_private_count": len(
                [row for row in support_rows if row["support_status"] == "private_company_planned"]
            ),
            "needs_live_resolution_count": len(
                [row for row in support_rows if row["support_status"] == "needs_live_resolution"]
            ),
        },
    }
