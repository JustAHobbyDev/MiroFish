"""
Deterministic private-company diligence planning from live issuer-resolution results.
"""

from __future__ import annotations

from typing import Any, Dict, List


def _coerce_string(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def _query_terms(entity_name: str) -> List[str]:
    return [
        entity_name,
        f"{entity_name} financing",
        f"{entity_name} debt issuance",
        f"{entity_name} private placement",
        f"{entity_name} investor",
        f"{entity_name} press release",
        f"{entity_name} capacity expansion",
    ]


def build_private_company_diligence_plan_batch(
    issuer_resolution_live_batch: Dict[str, Any],
) -> Dict[str, Any]:
    plans: List[Dict[str, Any]] = []

    for result in issuer_resolution_live_batch.get("results", []):
        if _coerce_string(result.get("live_resolution_status")) != "resolved_private_company_route":
            continue
        entity_name = _coerce_string(result.get("canonical_entity_name"))
        resolved_issuer_name = _coerce_string(result.get("resolved_issuer_name")) or entity_name
        plans.append(
            {
                "private_company_diligence_plan_id": f"pcd_{entity_name.lower().replace(' ', '_')}",
                "canonical_entity_name": entity_name,
                "resolved_issuer_name": resolved_issuer_name,
                "system_label": "utility and large-load power buildout",
                "diligence_status": "planned",
                "route_type": "private_company",
                "priority_tier": "targeted",
                "source_priorities": [
                    "official_company_site",
                    "official_press_releases",
                    "financing_announcements",
                    "private_credit_or_abs_materials",
                    "trade_press",
                ],
                "query_terms": _query_terms(resolved_issuer_name),
                "next_actions": [
                    "Collect official company press releases and financing announcements.",
                    "Look for debt, ABS, private placement, and campus-capacity materials.",
                    "Do not route this issuer into public-company filing collection.",
                ],
                "origin_live_resolution_result": {
                    "canonical_entity_name": entity_name,
                    "live_resolution_status": _coerce_string(result.get("live_resolution_status")),
                    "filing_route_assessment": _coerce_string(result.get("filing_route_assessment")),
                },
                "evidence": list(result.get("evidence", [])),
            }
        )

    return {
        "name": "private_company_diligence_plan_batch_v1",
        "plans": plans,
        "metrics": {
            "input_live_resolution_count": len(issuer_resolution_live_batch.get("results", [])),
            "private_company_plan_count": len(plans),
        },
    }
