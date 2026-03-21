"""
Deterministic bounded-entity expansion execution from selected family candidates.
"""

from __future__ import annotations

from typing import Any, Dict, List


def _coerce_string(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def build_bounded_entity_expansion_batch(
    family_batch: Dict[str, Any],
    expansion_assessment: Dict[str, Any],
) -> Dict[str, Any]:
    first_test = expansion_assessment.get("first_downstream_entity_expansion_test", {})
    target_system = _coerce_string(first_test.get("system_label"))
    initial_priority_entities = {
        _coerce_string(name)
        for name in first_test.get("initial_priority_entities", [])
        if _coerce_string(name)
    }

    expansions: List[Dict[str, Any]] = []
    for family in family_batch.get("families", []):
        if _coerce_string(family.get("system_label")) != target_system:
            continue
        canonical_name = _coerce_string(family.get("canonical_entity_name"))
        if canonical_name not in initial_priority_entities:
            continue

        source_classes = [_coerce_string(item) for item in family.get("source_classes", []) if _coerce_string(item)]
        next_source_classes = [
            _coerce_string(item)
            for item in family.get("recommended_next_source_classes", [])
            if _coerce_string(item) and _coerce_string(item) not in source_classes
        ]
        expansions.append(
            {
                "canonical_entity_name": canonical_name,
                "system_label": target_system,
                "priority_tier": _coerce_string(family.get("priority_tier")) or "low",
                "entity_role": _coerce_string(family.get("entity_role")),
                "origin_corporate_family_candidate_id": _coerce_string(
                    family.get("corporate_family_candidate_id")
                ),
                "origin_bounded_entity_candidate_ids": list(
                    family.get("origin_bounded_entity_candidate_ids", [])
                ),
                "member_entities": list(family.get("member_entities", [])),
                "supporting_artifact_ids": list(family.get("supporting_artifact_ids", [])),
                "supporting_titles": list(family.get("supporting_titles", [])),
                "local_source_classes": source_classes,
                "local_coverage_status": "cross_source_local" if len(source_classes) >= 2 else "single_source_local",
                "filing_gap": "company_filing" not in source_classes,
                "next_priority_source_classes": next_source_classes,
                "ready_for_filing_expansion": "company_filing" in next_source_classes,
            }
        )

    expansions.sort(key=lambda item: ({"high": 0, "medium": 1, "low": 2}.get(item["priority_tier"], 3), item["canonical_entity_name"]))
    return {
        "name": "bounded_entity_expansion_batch_v1",
        "expansions": expansions,
        "metrics": {
            "input_family_candidate_count": len(family_batch.get("families", [])),
            "selected_entity_expansion_count": len(expansions),
        },
    }
