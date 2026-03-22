"""
Build filing-backed public company research briefs from execution-ready handoff rows.
"""

from __future__ import annotations

from typing import Any, Dict, List


def _coerce_string(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def _base_entity_name(value: str) -> str:
    text = _coerce_string(value)
    if " on " in text:
        return _coerce_string(text.split(" on ", 1)[0])
    return text


def _support_index(rows: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    return {
        _base_entity_name(_coerce_string(row.get("canonical_entity_name"))).lower(): row
        for row in rows
        if _coerce_string(row.get("canonical_entity_name"))
    }


def _priority_note(role_label: str) -> str:
    if role_label == "bottleneck_candidate":
        return "Confirm whether constrained component evidence is converting into pricing power, backlog durability, and capacity leverage."
    if role_label == "supply_chain_beneficiary":
        return "Confirm whether supplier exposure is large enough to matter economically even without strict chokepoint status."
    return "Confirm whether operator response translates into durable economic value capture."


def _research_questions(role_label: str) -> List[str]:
    if role_label == "bottleneck_candidate":
        return [
            "How much of current demand is tied specifically to transformers, switchgear, or substation equipment?",
            "Is backlog or RPO converting into revenue without margin erosion?",
            "Are new capacity additions likely to relieve or reinforce the current constrained layer?",
        ]
    if role_label == "supply_chain_beneficiary":
        return [
            "Which business segments are most exposed to the theme and how material are they?",
            "Is capacity expansion targeted at the constrained layer or spread across unrelated end markets?",
            "What would need to happen for this name to graduate from beneficiary to bottleneck candidate?",
        ]
    return [
        "Is utility or operator capex translating into earnings power fast enough to matter?",
        "Are demand-response economics visible in upcoming reporting or only in planning language?",
        "Does regulatory structure cap upside despite the demand signal?",
    ]


def _evidence_summary(row: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "filing_support_status": _coerce_string(row.get("filing_support_status")),
        "filing_evidence_item_count": int(row.get("filing_evidence_item_count", 0)),
        "filing_strong_evidence_item_count": int(row.get("filing_strong_evidence_item_count", 0)),
        "filing_component_specific_count": int(row.get("filing_component_specific_count", 0)),
        "filing_pressure_or_capacity_count": int(row.get("filing_pressure_or_capacity_count", 0)),
        "filing_expansion_or_capex_count": int(row.get("filing_expansion_or_capex_count", 0)),
    }


def _top_excerpt_rows(row: Dict[str, Any]) -> List[Dict[str, Any]]:
    excerpts: List[Dict[str, Any]] = []
    for item in list(row.get("top_filing_evidence_items", []))[:3]:
        excerpts.append(
            {
                "document_title": _coerce_string(item.get("document_title")),
                "filing_type": _coerce_string(item.get("filing_type")),
                "keyword": _coerce_string(item.get("keyword")),
                "keyword_family": _coerce_string(item.get("keyword_family")),
                "page_number": item.get("page_number"),
                "excerpt": _coerce_string(item.get("excerpt")),
            }
        )
    return excerpts


def build_public_company_research_brief_batch(
    public_market_execution_handoff_batch: Dict[str, Any],
    bounded_entity_filing_support_batch: Dict[str, Any],
) -> Dict[str, Any]:
    support_by_entity = _support_index(bounded_entity_filing_support_batch.get("support_rows", []))

    brief_rows: List[Dict[str, Any]] = []
    for handoff_row in public_market_execution_handoff_batch.get("handoff_rows", []):
        canonical_entity_name = _base_entity_name(
            _coerce_string(handoff_row.get("canonical_entity_name") or handoff_row.get("name"))
        )
        support_row = support_by_entity.get(canonical_entity_name.lower(), {})
        role_label = _coerce_string(handoff_row.get("role_label"))
        evidence_summary = _evidence_summary(support_row)
        brief_rows.append(
            {
                "canonical_entity_name": canonical_entity_name,
                "resolved_issuer_name": _coerce_string(support_row.get("resolved_issuer_name")),
                "underlying": _coerce_string(handoff_row.get("underlying")),
                "market_theme": _coerce_string(handoff_row.get("market_theme")),
                "role_label": role_label,
                "execution_priority": _coerce_string(handoff_row.get("execution_priority")),
                "execution_expression": _coerce_string(handoff_row.get("execution_expression")),
                "thesis": _coerce_string(handoff_row.get("thesis")),
                "value_capture_layer": _coerce_string(handoff_row.get("value_capture_layer")),
                "evidence_summary": evidence_summary,
                "top_supporting_excerpts": _top_excerpt_rows(support_row),
                "research_priority_note": _priority_note(role_label),
                "research_questions": _research_questions(role_label),
                "top_catalysts": list(handoff_row.get("top_catalysts", [])),
                "top_invalidations": list(handoff_row.get("top_invalidations", [])),
                "why_missed": list(handoff_row.get("why_missed", [])),
                "brief_status": (
                    "ready_for_human_company_research"
                    if evidence_summary["filing_support_status"] == "supported"
                    else "needs_more_support_before_company_research"
                ),
            }
        )

    brief_rows.sort(
        key=lambda row: (
            {"highest": 0, "high": 1, "medium": 2}.get(row["execution_priority"], 3),
            {
                "bottleneck_candidate": 0,
                "supply_chain_beneficiary": 1,
                "capacity_response_operator": 2,
            }.get(row["role_label"], 3),
            row["canonical_entity_name"],
        )
    )

    return {
        "name": "public_company_research_brief_batch_v1",
        "brief_rows": brief_rows,
        "metrics": {
            "input_handoff_row_count": len(public_market_execution_handoff_batch.get("handoff_rows", [])),
            "brief_count": len(brief_rows),
            "ready_for_human_company_research_count": len(
                [row for row in brief_rows if row["brief_status"] == "ready_for_human_company_research"]
            ),
            "supported_brief_count": len(
                [row for row in brief_rows if row["evidence_summary"]["filing_support_status"] == "supported"]
            ),
        },
    }
