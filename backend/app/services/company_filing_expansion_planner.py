"""
Deterministic company-filing expansion planning from bounded entity expansions.
"""

from __future__ import annotations

import hashlib
import re
from typing import Any, Dict, List


def _coerce_string(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def _plan_id(entity_name: str, system_label: str) -> str:
    entity_slug = re.sub(r"[^a-z0-9]+", "_", entity_name.lower()).strip("_")
    system_slug = re.sub(r"[^a-z0-9]+", "_", system_label.lower()).strip("_")
    digest = hashlib.sha1(f"{entity_slug}|{system_slug}".encode("utf-8")).hexdigest()[:8]
    return f"cfep_{entity_slug}_{digest}"


def _filing_form_sets(priority_tier: str) -> Dict[str, List[str]]:
    base = {
        "domestic_public": ["10-K", "10-Q", "8-K"],
        "foreign_public": ["20-F"],
    }
    if _coerce_string(priority_tier) == "high":
        return base
    return base


def _resolution_tasks(canonical_entity_name: str) -> List[str]:
    return [
        f"Resolve the legal issuer identity for {canonical_entity_name}.",
        "Determine whether the issuer is public, private, or foreign-listed.",
        "If public, map the issuer to the appropriate filing route before collection.",
    ]


def build_company_filing_expansion_batch(
    entity_expansion_batch: Dict[str, Any],
) -> Dict[str, Any]:
    plans: List[Dict[str, Any]] = []

    for expansion in entity_expansion_batch.get("expansions", []):
        if not expansion.get("ready_for_filing_expansion"):
            continue
        canonical_entity_name = _coerce_string(expansion.get("canonical_entity_name"))
        system_label = _coerce_string(expansion.get("system_label"))
        priority_tier = _coerce_string(expansion.get("priority_tier")) or "low"
        local_source_classes = [
            _coerce_string(item)
            for item in expansion.get("local_source_classes", [])
            if _coerce_string(item)
        ]
        next_priority_source_classes = [
            _coerce_string(item)
            for item in expansion.get("next_priority_source_classes", [])
            if _coerce_string(item)
        ]
        plans.append(
            {
                "company_filing_expansion_plan_id": _plan_id(canonical_entity_name, system_label),
                "canonical_entity_name": canonical_entity_name,
                "system_label": system_label,
                "priority_tier": priority_tier,
                "entity_role": _coerce_string(expansion.get("entity_role")),
                "origin_corporate_family_candidate_id": _coerce_string(
                    expansion.get("origin_corporate_family_candidate_id")
                ),
                "origin_bounded_entity_candidate_ids": list(
                    expansion.get("origin_bounded_entity_candidate_ids", [])
                ),
                "member_entities": list(expansion.get("member_entities", [])),
                "supporting_artifact_ids": list(expansion.get("supporting_artifact_ids", [])),
                "supporting_titles": list(expansion.get("supporting_titles", [])),
                "local_source_classes": local_source_classes,
                "local_coverage_status": _coerce_string(expansion.get("local_coverage_status")),
                "issuer_resolution_status": "unresolved",
                "company_filing_status": "not_collected",
                "candidate_filing_form_sets": _filing_form_sets(priority_tier),
                "resolution_tasks": _resolution_tasks(canonical_entity_name),
                "next_priority_source_classes": next_priority_source_classes,
                "collection_gate": "resolve_issuer_before_filing_fetch",
                "ready_for_live_resolution": True,
                "blocking_reason": "issuer identity and listing status unresolved",
            }
        )

    plans.sort(
        key=lambda item: (
            {"high": 0, "medium": 1, "low": 2}.get(item["priority_tier"], 3),
            item["canonical_entity_name"],
        )
    )
    return {
        "name": "company_filing_expansion_batch_v1",
        "plans": plans,
        "metrics": {
            "input_entity_expansion_count": len(entity_expansion_batch.get("expansions", [])),
            "company_filing_expansion_plan_count": len(plans),
        },
    }
