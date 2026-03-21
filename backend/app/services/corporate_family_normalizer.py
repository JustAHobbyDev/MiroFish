"""
Deterministic corporate-family normalization for bounded entity candidates.
"""

from __future__ import annotations

import hashlib
import re
from typing import Any, Dict, List


def _coerce_string(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def _normalized_tokens(name: str) -> List[str]:
    return re.findall(r"[a-z0-9]+", _coerce_string(name).lower())


def _is_prefix_family(left: str, right: str) -> bool:
    left_tokens = _normalized_tokens(left)
    right_tokens = _normalized_tokens(right)
    if not left_tokens or not right_tokens or left_tokens == right_tokens:
        return False
    if len(left_tokens) >= len(right_tokens):
        return False
    return right_tokens[: len(left_tokens)] == left_tokens


def _family_id(system_label: str, canonical_name: str, as_of_date: str) -> str:
    system_slug = re.sub(r"[^a-z0-9]+", "_", system_label.lower()).strip("_")
    name_slug = re.sub(r"[^a-z0-9]+", "_", canonical_name.lower()).strip("_")
    suffix = as_of_date or "unknown_date"
    digest = hashlib.sha1(f"{system_slug}|{name_slug}|{suffix}".encode("utf-8")).hexdigest()[:8]
    return f"cf_{system_slug}_{name_slug}_{suffix}_{digest}"


def _priority_rank(priority_tier: str) -> int:
    return {"high": 3, "medium": 2, "low": 1}.get(_coerce_string(priority_tier).lower(), 0)


def _choose_canonical_name(members: List[Dict[str, Any]]) -> str:
    names = [_coerce_string(item.get("entity_name")) for item in members if _coerce_string(item.get("entity_name"))]
    if not names:
        return ""
    return max(names, key=lambda value: (len(_normalized_tokens(value)), len(value), value))


def _merge_relation(members: List[Dict[str, Any]]) -> str:
    names = [_coerce_string(item.get("entity_name")) for item in members]
    unique_names = sorted({name for name in names if name})
    if len(unique_names) <= 1:
        return "identity_only"
    return "prefix_family_merge"


def build_corporate_family_batch(bounded_entity_batch: Dict[str, Any]) -> Dict[str, Any]:
    output: List[Dict[str, Any]] = []

    by_system: Dict[str, List[Dict[str, Any]]] = {}
    for candidate in bounded_entity_batch.get("candidates", []):
        by_system.setdefault(_coerce_string(candidate.get("system_label")), []).append(candidate)

    for system_label, candidates in by_system.items():
        consumed: set[int] = set()
        for index, candidate in enumerate(candidates):
            if index in consumed:
                continue
            members = [candidate]
            consumed.add(index)
            candidate_name = _coerce_string(candidate.get("entity_name"))
            for other_index, other in enumerate(candidates):
                if other_index in consumed:
                    continue
                other_name = _coerce_string(other.get("entity_name"))
                if _is_prefix_family(candidate_name, other_name) or _is_prefix_family(other_name, candidate_name):
                    members.append(other)
                    consumed.add(other_index)

            canonical_name = _choose_canonical_name(members)
            as_of_date = _coerce_string(candidate.get("as_of_date"))
            source_classes = sorted(
                {
                    _coerce_string(source_class)
                    for member in members
                    for source_class in member.get("source_classes", [])
                    if _coerce_string(source_class)
                }
            )
            supporting_artifact_ids = sorted(
                {
                    _coerce_string(artifact_id)
                    for member in members
                    for artifact_id in member.get("supporting_artifact_ids", [])
                    if _coerce_string(artifact_id)
                }
            )
            supporting_titles = sorted(
                {
                    _coerce_string(title)
                    for member in members
                    for title in member.get("supporting_titles", [])
                    if _coerce_string(title)
                }
            )
            recommended_next_source_classes = sorted(
                {
                    _coerce_string(source_class)
                    for member in members
                    for source_class in member.get("recommended_next_source_classes", [])
                    if _coerce_string(source_class)
                }
            )
            provenance_statuses = sorted(
                {
                    _coerce_string(member.get("support_provenance_status"))
                    for member in members
                    if _coerce_string(member.get("support_provenance_status"))
                }
            )
            if provenance_statuses == ["synthetic_only"]:
                support_provenance = "synthetic_only"
            elif "synthetic_only" in provenance_statuses or "mixed" in provenance_statuses:
                support_provenance = "mixed"
            else:
                support_provenance = "real_only"
            priority_tier = max(
                (_coerce_string(member.get("priority_tier")) for member in members),
                key=_priority_rank,
                default="low",
            )
            output.append(
                {
                    "corporate_family_candidate_id": _family_id(system_label, canonical_name, as_of_date),
                    "system_label": system_label,
                    "as_of_date": as_of_date,
                    "canonical_entity_name": canonical_name,
                    "member_entities": sorted(
                        {
                            _coerce_string(member.get("entity_name"))
                            for member in members
                            if _coerce_string(member.get("entity_name"))
                        }
                    ),
                    "origin_bounded_entity_candidate_ids": sorted(
                        {
                            _coerce_string(member.get("bounded_entity_candidate_id"))
                            for member in members
                            if _coerce_string(member.get("bounded_entity_candidate_id"))
                        }
                    ),
                    "merge_relation": _merge_relation(members),
                    "normalization_confidence": "medium" if len(members) > 1 else "high",
                    "entity_role": _coerce_string(candidate.get("entity_role")),
                    "priority_tier": priority_tier,
                    "source_classes": source_classes,
                    "supporting_artifact_ids": supporting_artifact_ids,
                    "supporting_titles": supporting_titles,
                    "support_provenance_status": support_provenance,
                    "recommended_next_source_classes": recommended_next_source_classes,
                }
            )

    output.sort(key=lambda item: (item["system_label"], {"high": 0, "medium": 1, "low": 2}.get(item["priority_tier"], 3), item["canonical_entity_name"]))
    return {
        "name": "corporate_family_batch_v1",
        "families": output,
        "metrics": {
            "input_bounded_entity_candidate_count": len(bounded_entity_batch.get("candidates", [])),
            "corporate_family_candidate_count": len(output),
        },
    }
