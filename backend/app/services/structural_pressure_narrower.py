"""
Deterministic narrowing of broad structural-pressure lanes into narrower bounded candidates.
"""

from __future__ import annotations

import re
from typing import Any, Dict, List, Set

from .artifact_provenance import (
    artifact_provenance_classes,
    support_provenance_status,
)


def _coerce_string(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def _artifact_index(*prefilter_batches: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    index: Dict[str, Dict[str, Any]] = {}
    for batch in prefilter_batches:
        for key in ("kept_artifacts", "review_artifacts"):
            for artifact in batch.get(key, []):
                artifact_id = _coerce_string(artifact.get("artifact_id"))
                if artifact_id:
                    index[artifact_id] = artifact
    return index


def _artifact_id_from_signal_id(signal_id: str) -> str:
    return _coerce_string(signal_id).split(":", 1)[0]


def _matches_backup_power_title(title: str) -> bool:
    title = title.lower()
    equipment = any(token in title for token in ("generator", "engine", "enclosure"))
    buildout = any(
        token in title
        for token in ("factory", "plant", "manufacturing", "production", "assembly", "expansion", "invests")
    )
    context = any(token in title for token in ("data center", "backup", "resilience", "power"))
    return equipment and (buildout or context)


def build_structural_pressure_narrowing_batch(
    structural_pressure_batch: Dict[str, Any],
    capital_cluster_batch: Dict[str, Any],
    mixed_prefilter_batch: Dict[str, Any],
) -> Dict[str, Any]:
    artifact_by_id = _artifact_index(mixed_prefilter_batch)
    cluster_index = {
        _coerce_string(cluster.get("capital_flow_cluster_id")): cluster
        for cluster in capital_cluster_batch.get("clusters", [])
        if _coerce_string(cluster.get("capital_flow_cluster_id"))
    }
    narrowed_candidates: List[Dict[str, Any]] = []

    for candidate in structural_pressure_batch.get("candidates", []):
        system_label = _coerce_string(candidate.get("system_label"))
        if system_label not in {
            "power generation and backup equipment pressure",
            "power generation and backup equipment buildout",
        }:
            continue
        cluster_ids = [
            _coerce_string(item)
            for item in candidate.get("supporting_capital_flow_cluster_ids", [])
            if _coerce_string(item)
        ]
        matched_artifact_ids: Set[str] = set()
        matched_titles: List[str] = []
        source_classes: Set[str] = set()
        matched_artifacts: List[Dict[str, Any]] = []
        for cluster_id in cluster_ids:
            cluster = cluster_index.get(cluster_id, {})
            for signal_id in cluster.get("supporting_capital_flow_signal_ids", []):
                artifact_id = _artifact_id_from_signal_id(signal_id)
                artifact = artifact_by_id.get(artifact_id, {})
                title = _coerce_string(artifact.get("title"))
                if not title or not _matches_backup_power_title(title):
                    continue
                matched_artifact_ids.add(artifact_id)
                matched_titles.append(title)
                matched_artifacts.append(artifact)
                source_class = _coerce_string(artifact.get("source_class"))
                if source_class:
                    source_classes.add(source_class)

        if len(matched_artifact_ids) < 2:
            continue
        provenance_status = support_provenance_status(matched_artifacts)
        if provenance_status != "real_only":
            continue

        narrowed_candidates.append(
            {
                "narrowed_pressure_candidate_id": re.sub(
                    r"[^a-z0-9_]+",
                    "_",
                    f"nsp_data_center_backup_power_equipment_buildout_{_coerce_string(candidate.get('as_of_date'))}",
                ).strip("_"),
                "origin_pressure_candidate_id": _coerce_string(candidate.get("pressure_candidate_id")),
                "status": "exploratory_candidate",
                "system_label": "data center backup-power equipment buildout",
                "narrowing_basis": {
                    "origin_system_label": system_label,
                    "matched_artifact_count": len(matched_artifact_ids),
                    "matched_titles": sorted(set(matched_titles)),
                    "source_classes": sorted(source_classes),
                    "support_provenance_status": provenance_status,
                    "artifact_provenance_classes": artifact_provenance_classes(matched_artifacts),
                    "boundedness_status": "bounded",
                    "research_ready": True,
                    "promotion_ready": False,
                },
                "suspected_stress_layers": [
                    "backup-power equipment manufacturing",
                    "generator packages",
                    "large-engine backup systems",
                    "power enclosures",
                ],
                "next_step": "form exploratory bounded-universe and entity follow-up from the narrowed lane",
            }
        )

    return {
        "name": "structural_pressure_narrowing_batch_v1",
        "narrowed_candidates": narrowed_candidates,
        "metrics": {
            "input_pressure_candidate_count": len(structural_pressure_batch.get("candidates", [])),
            "narrowed_candidate_count": len(narrowed_candidates),
        },
    }
