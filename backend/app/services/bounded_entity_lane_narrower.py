"""
Deterministic narrowing of exploratory bounded-entity lanes into tighter follow-up queues.
"""

from __future__ import annotations

import re
from typing import Any, Dict, List, Set


ORIGIN_SYSTEM_LABEL = "utility and large-load power buildout"
NARROWED_SYSTEM_LABEL = "data center utility response buildout"


def _coerce_string(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def _title_matches_data_center_utility_response(title: str) -> bool:
    lowered = _coerce_string(title).lower()
    has_data_center = "data center" in lowered
    has_response_signal = any(
        token in lowered
        for token in (
            "deal",
            "load",
            "pipeline",
            "spending plan",
            "spending",
            "peak load",
            "campus",
            "breaks ground",
        )
    )
    return has_data_center and has_response_signal


def _candidate_index(entity_candidate_batch: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    index: Dict[str, Dict[str, Any]] = {}
    for candidate in entity_candidate_batch.get("candidates", []):
        entity_name = _coerce_string(candidate.get("entity_name"))
        if entity_name:
            index[entity_name] = candidate
    return index


def build_bounded_entity_lane_narrowing_batch(
    entity_candidate_batch: Dict[str, Any],
    followup_queue_batch: Dict[str, Any],
) -> Dict[str, Any]:
    candidate_index = _candidate_index(entity_candidate_batch)
    narrowed_queue_rows: List[Dict[str, Any]] = []
    matched_titles: List[str] = []
    matched_entities: List[str] = []
    source_classes: Set[str] = set()

    for row in followup_queue_batch.get("queue_rows", []):
        entity_name = _coerce_string(row.get("canonical_entity_name"))
        if not entity_name:
            continue
        candidate = candidate_index.get(entity_name, {})
        if _coerce_string(candidate.get("system_label")) != ORIGIN_SYSTEM_LABEL:
            continue
        if _coerce_string(candidate.get("support_provenance_status")) != "real_only":
            continue

        supporting_titles = [
            _coerce_string(item)
            for item in candidate.get("supporting_titles", [])
            if _coerce_string(item)
        ]
        if not any(_title_matches_data_center_utility_response(title) for title in supporting_titles):
            continue

        narrowed_queue_rows.append(
            {
                **row,
                "system_label": NARROWED_SYSTEM_LABEL,
            }
        )
        matched_entities.append(entity_name)
        matched_titles.extend(supporting_titles)
        for source_class in row.get("source_classes", []):
            if _coerce_string(source_class):
                source_classes.add(_coerce_string(source_class))

    narrowed_lanes: List[Dict[str, Any]] = []
    if narrowed_queue_rows:
        narrowed_lanes.append(
            {
                "narrowed_lane_id": re.sub(
                    r"[^a-z0-9_]+",
                    "_",
                    f"beln_{NARROWED_SYSTEM_LABEL}",
                ).strip("_"),
                "origin_system_label": ORIGIN_SYSTEM_LABEL,
                "system_label": NARROWED_SYSTEM_LABEL,
                "status": "exploratory_candidate",
                "supporting_entity_names": sorted(set(matched_entities)),
                "matched_title_count": len(matched_titles),
                "matched_titles": sorted(set(matched_titles)),
                "source_classes": sorted(source_classes),
                "support_provenance_status": "real_only",
                "next_step": "reuse route-aware support, priority, and review-surface builders on the narrowed queue",
            }
        )

    return {
        "name": "bounded_entity_lane_narrowing_batch_v1",
        "narrowed_lanes": narrowed_lanes,
        "queue_rows": narrowed_queue_rows,
        "metrics": {
            "input_candidate_count": len(entity_candidate_batch.get("candidates", [])),
            "input_queue_count": len(followup_queue_batch.get("queue_rows", [])),
            "narrowed_lane_count": len(narrowed_lanes),
            "narrowed_queue_count": len(narrowed_queue_rows),
        },
    }
