"""
Deterministic bounded-entity candidate formation from bounded research sets.
"""

from __future__ import annotations

import hashlib
import re
from typing import Any, Dict, List


def _coerce_string(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def _bounded_entity_id(system_label: str, entity_name: str, as_of_date: str) -> str:
    system_slug = re.sub(r"[^a-z0-9]+", "_", system_label.lower()).strip("_")
    entity_slug = re.sub(r"[^a-z0-9]+", "_", entity_name.lower()).strip("_")
    suffix = as_of_date or "unknown_date"
    digest = hashlib.sha1(f"{system_slug}|{entity_slug}|{suffix}".encode("utf-8")).hexdigest()[:8]
    return f"bec_{system_slug}_{entity_slug}_{suffix}_{digest}"


def _entity_role(system_label: str, matched_artifacts: List[Dict[str, Any]]) -> str:
    text = " ".join(
        [
            _coerce_string(system_label),
            *[_coerce_string(item.get("title")) for item in matched_artifacts],
            *[
                " ".join(_coerce_string(term) for term in item.get("matched_terms", []))
                for item in matched_artifacts
            ],
        ]
    ).lower()
    if any(token in text for token in ("transformer", "switchgear", "substation", "meter", "cable", "coil")):
        return "equipment_or_component_supplier"
    if any(token in text for token in ("data center", "campus", "hyperscale", "digital infrastructure")):
        return "capacity_operator_or_owner"
    if any(token in text for token in ("utility", "load", "generation", "interconnection")):
        return "power_or_utility_operator"
    return "general_beneficiary_candidate"


def _priority_tier(
    artifact_support_count: int,
    source_class_diversity_count: int,
    max_match_score: int,
) -> str:
    if artifact_support_count >= 2 or source_class_diversity_count >= 2 or max_match_score >= 8:
        return "high"
    if max_match_score >= 5:
        return "medium"
    return "low"


def _next_source_classes(entity_role: str, source_classes: List[str]) -> List[str]:
    ordered: List[str] = []
    for source_class in ["company_release", "trade_press", "company_filing", "government"]:
        if source_class not in ordered:
            ordered.append(source_class)
    if entity_role == "capacity_operator_or_owner":
        return [item for item in ordered if item in {"trade_press", "company_release", "company_filing", "government"}]
    return [item for item in ordered if item in {"company_release", "trade_press", "company_filing"}]


def build_bounded_entity_candidate_batch(research_set_batch: Dict[str, Any]) -> Dict[str, Any]:
    candidates: List[Dict[str, Any]] = []

    for research_set in research_set_batch.get("research_sets", []):
        system_label = _coerce_string(research_set.get("system_label"))
        as_of_date = _coerce_string(research_set.get("as_of_date"))
        matched_artifacts_by_id = {
            _coerce_string(item.get("artifact_id")): item for item in research_set.get("matched_artifacts", [])
        }

        for entity in research_set.get("entity_candidates", []):
            entity_name = _coerce_string(entity.get("entity_name"))
            if not entity_name:
                continue
            artifact_ids = [item for item in entity.get("artifact_ids", []) if _coerce_string(item)]
            supporting_artifacts = [
                matched_artifacts_by_id[item]
                for item in artifact_ids
                if item in matched_artifacts_by_id
            ]
            if not supporting_artifacts:
                continue

            source_classes = sorted(
                {
                    _coerce_string(item.get("source_class"))
                    for item in supporting_artifacts
                    if _coerce_string(item.get("source_class"))
                }
            )
            max_match_score = max(int(item.get("match_score", 0)) for item in supporting_artifacts)
            matched_terms = sorted(
                {
                    _coerce_string(term)
                    for item in supporting_artifacts
                    for term in item.get("matched_terms", [])
                    if _coerce_string(term)
                }
            )
            entity_role = _entity_role(system_label, supporting_artifacts)
            candidates.append(
                {
                    "bounded_entity_candidate_id": _bounded_entity_id(system_label, entity_name, as_of_date),
                    "origin_bounded_research_set_id": _coerce_string(research_set.get("bounded_research_set_id")),
                    "system_label": system_label,
                    "as_of_date": as_of_date,
                    "entity_name": entity_name,
                    "entity_role": entity_role,
                    "artifact_support_count": len(artifact_ids),
                    "source_classes": source_classes,
                    "source_class_diversity_count": len(source_classes),
                    "supporting_artifact_ids": artifact_ids,
                    "supporting_titles": [
                        _coerce_string(item.get("title")) for item in supporting_artifacts if _coerce_string(item.get("title"))
                    ],
                    "matched_terms": matched_terms,
                    "priority_tier": _priority_tier(
                        artifact_support_count=len(artifact_ids),
                        source_class_diversity_count=len(source_classes),
                        max_match_score=max_match_score,
                    ),
                    "max_match_score": max_match_score,
                    "recommended_next_source_classes": _next_source_classes(entity_role, source_classes),
                }
            )

    candidates.sort(
        key=lambda item: (
            item["system_label"],
            {"high": 0, "medium": 1, "low": 2}.get(item["priority_tier"], 3),
            -item["artifact_support_count"],
            -item["max_match_score"],
            item["entity_name"],
        )
    )
    return {
        "name": "bounded_entity_candidate_batch_v1",
        "candidates": candidates,
        "metrics": {
            "input_bounded_research_set_count": len(research_set_batch.get("research_sets", [])),
            "bounded_entity_candidate_count": len(candidates),
        },
    }
