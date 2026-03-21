"""
Deterministic issuer-resolution planning from company-filing expansion plans.
"""

from __future__ import annotations

import hashlib
import re
from typing import Any, Dict, List


FOREIGN_BASED_PATTERN = re.compile(r"\b([A-Z][a-z]+)-based\b")
US_PATTERN = re.compile(r"\bU\.?S\.?\b|\bUS\b")


def _coerce_string(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def _plan_id(entity_name: str, system_label: str) -> str:
    entity_slug = re.sub(r"[^a-z0-9]+", "_", entity_name.lower()).strip("_")
    system_slug = re.sub(r"[^a-z0-9]+", "_", system_label.lower()).strip("_")
    digest = hashlib.sha1(f"{entity_slug}|{system_slug}".encode("utf-8")).hexdigest()[:8]
    return f"irp_{entity_slug}_{digest}"


def _evidence_text(plan: Dict[str, Any]) -> str:
    return " ".join(
        [
            _coerce_string(plan.get("canonical_entity_name")),
            *[_coerce_string(item) for item in plan.get("member_entities", [])],
            *[_coerce_string(item) for item in plan.get("supporting_titles", [])],
        ]
    )


def _foreign_geography_hints(text: str) -> List[str]:
    return sorted({match.group(1) for match in FOREIGN_BASED_PATTERN.finditer(text)})


def _route_hypothesis(text: str) -> str:
    foreign_hints = _foreign_geography_hints(text)
    if foreign_hints:
        return "foreign_route_hint"
    if US_PATTERN.search(text):
        return "domestic_route_hint"
    return "route_unknown"


def _candidate_resolution_paths(route_hypothesis: str) -> List[str]:
    if route_hypothesis == "foreign_route_hint":
        return [
            "corporate website or investor relations",
            "annual report or equivalent",
            "20-F if SEC-registered foreign issuer",
        ]
    if route_hypothesis == "domestic_route_hint":
        return [
            "corporate website or investor relations",
            "SEC EDGAR issuer search",
            "10-K / 10-Q / 8-K if public",
        ]
    return [
        "corporate website or investor relations",
        "SEC EDGAR issuer search",
        "annual report or equivalent",
    ]


def _query_terms(entity_name: str, route_hypothesis: str) -> List[str]:
    base = [
        entity_name,
        f"{entity_name} investor relations",
        f"{entity_name} annual report",
    ]
    if route_hypothesis == "foreign_route_hint":
        base.extend([f"{entity_name} 20-F", f"{entity_name} annual report pdf"])
    else:
        base.extend([f"{entity_name} SEC EDGAR", f"{entity_name} 10-K"])
    return base


def _resolution_queue_group(priority_tier: str) -> str:
    return "resolve_first" if _coerce_string(priority_tier) == "high" else "resolve_after_high"


def build_issuer_resolution_batch(
    company_filing_expansion_batch: Dict[str, Any],
) -> Dict[str, Any]:
    plans: List[Dict[str, Any]] = []

    for filing_plan in company_filing_expansion_batch.get("plans", []):
        canonical_entity_name = _coerce_string(filing_plan.get("canonical_entity_name"))
        system_label = _coerce_string(filing_plan.get("system_label"))
        priority_tier = _coerce_string(filing_plan.get("priority_tier")) or "low"
        evidence_text = _evidence_text(filing_plan)
        route_hypothesis = _route_hypothesis(evidence_text)
        plans.append(
            {
                "issuer_resolution_plan_id": _plan_id(canonical_entity_name, system_label),
                "origin_company_filing_expansion_plan_id": _coerce_string(
                    filing_plan.get("company_filing_expansion_plan_id")
                ),
                "canonical_entity_name": canonical_entity_name,
                "system_label": system_label,
                "priority_tier": priority_tier,
                "member_entities": list(filing_plan.get("member_entities", [])),
                "supporting_titles": list(filing_plan.get("supporting_titles", [])),
                "route_hypothesis": route_hypothesis,
                "foreign_geography_hints": _foreign_geography_hints(evidence_text),
                "candidate_resolution_paths": _candidate_resolution_paths(route_hypothesis),
                "issuer_resolution_query_terms": _query_terms(canonical_entity_name, route_hypothesis),
                "resolution_queue_group": _resolution_queue_group(priority_tier),
                "issuer_resolution_status": "planned_not_resolved",
                "resolution_note": "No live issuer-resolution performed in v1.",
            }
        )

    plans.sort(
        key=lambda item: (
            {"resolve_first": 0, "resolve_after_high": 1}.get(item["resolution_queue_group"], 2),
            {"high": 0, "medium": 1, "low": 2}.get(item["priority_tier"], 3),
            item["canonical_entity_name"],
        )
    )
    return {
        "name": "issuer_resolution_batch_v1",
        "plans": plans,
        "metrics": {
            "input_company_filing_expansion_plan_count": len(company_filing_expansion_batch.get("plans", [])),
            "issuer_resolution_plan_count": len(plans),
        },
    }
