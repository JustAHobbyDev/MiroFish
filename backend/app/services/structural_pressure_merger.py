"""
Deterministic merge logic from pressure clusters to structural pressure candidates.
"""

from __future__ import annotations

import hashlib
import re
from datetime import date
from typing import Any, Dict, List, Optional


def _coerce_string(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def _parse_date(value: Any) -> Optional[date]:
    text = _coerce_string(value)
    if not text:
        return None
    try:
        return date.fromisoformat(text[:10])
    except ValueError:
        return None


def _cluster_window_overlap(left: Dict[str, Any], right: Dict[str, Any]) -> bool:
    left_start = _parse_date(left.get("time_window", {}).get("start_date"))
    left_end = _parse_date(left.get("time_window", {}).get("end_date"))
    right_start = _parse_date(right.get("time_window", {}).get("start_date"))
    right_end = _parse_date(right.get("time_window", {}).get("end_date"))
    if None in {left_start, left_end, right_start, right_end}:
        return False
    return not (left_end < right_start or right_end < left_start)


ADJACENT_SYSTEM_LABELS = {
    ("grid equipment and transformer buildout", "grid equipment and transformer pressure"),
    ("utility and large-load power buildout", "utility and large-load power demand pressure"),
    ("data center campus buildout", "data center power demand buildout"),
    ("power generation and backup equipment buildout", "utility and large-load power demand pressure"),
    ("power generation and backup equipment buildout", "power generation and backup equipment pressure"),
}


def _system_overlap(capital_label: str, energy_label: str) -> bool:
    if capital_label == energy_label:
        return True
    return (capital_label, energy_label) in ADJACENT_SYSTEM_LABELS


def _merge_system_label(capital_label: str, energy_label: Optional[str]) -> str:
    if not energy_label:
        return capital_label
    if capital_label == "grid equipment and transformer buildout" and energy_label == "grid equipment and transformer pressure":
        return "grid equipment and transformer pressure"
    if capital_label == "utility and large-load power buildout" and energy_label == "utility and large-load power demand pressure":
        return "utility and large-load power demand pressure"
    if capital_label == "data center campus buildout" and energy_label == "data center power demand buildout":
        return "data center power demand buildout"
    if capital_label == "power generation and backup equipment buildout" and energy_label == "power generation and backup equipment pressure":
        return "power generation and backup equipment pressure"
    return capital_label


def _merge_confidence(capital_confidence: str, energy_confidence: Optional[str]) -> str:
    if capital_confidence == "high" and energy_confidence in {"high", "medium"}:
        return "high"
    if capital_confidence in {"high", "medium"} and energy_confidence in {"high", "medium"}:
        return "medium"
    return capital_confidence or energy_confidence or "low"


def _apply_source_diversity_guardrail(
    confidence: str,
    source_classes: List[str],
) -> tuple[str, str, bool]:
    distinct_source_count = len({item for item in source_classes if _coerce_string(item)})
    if distinct_source_count <= 1:
        adjusted_confidence = "medium" if confidence == "high" else (confidence or "low")
        return adjusted_confidence, "single_source_class", True
    return confidence or "low", "multi_source_class", False


def _source_diversity_corroboration_satisfied(
    source_classes: List[str],
    supporting_capital_flow_cluster_ids: List[str],
) -> bool:
    distinct_source_count = len({item for item in source_classes if _coerce_string(item)})
    return distinct_source_count >= 2 and len([item for item in supporting_capital_flow_cluster_ids if _coerce_string(item)]) >= 1


def _pressure_statement(system_label: str, demand_driver_summary: str) -> str:
    return f"{demand_driver_summary} This is likely to create structural pressure in {system_label}."


def _id_for_structural_candidate(system_label: str, as_of_date: Optional[str]) -> str:
    slug = re.sub(r"[^a-z0-9]+", "_", system_label.lower()).strip("_")
    suffix = as_of_date or "unknown_date"
    digest = hashlib.sha1(f"{slug}|{suffix}".encode("utf-8")).hexdigest()[:8]
    return f"spc_{slug}_{suffix}_{digest}"


def build_structural_pressure_candidate_batch(
    capital_cluster_batch: Dict[str, Any],
    energy_cluster_batch: Dict[str, Any],
) -> Dict[str, Any]:
    capital_clusters = list(capital_cluster_batch.get("clusters", []))
    energy_clusters = list(energy_cluster_batch.get("clusters", []))
    used_energy_ids: set[str] = set()
    candidates: List[Dict[str, Any]] = []

    for capital_cluster in capital_clusters:
        capital_label = _coerce_string(capital_cluster.get("system_label"))
        matched_energy: Optional[Dict[str, Any]] = None
        for energy_cluster in energy_clusters:
            energy_id = _coerce_string(energy_cluster.get("energy_flow_pressure_cluster_id"))
            if energy_id in used_energy_ids:
                continue
            if not _system_overlap(capital_label, _coerce_string(energy_cluster.get("system_label"))):
                continue
            if not _cluster_window_overlap(capital_cluster, energy_cluster):
                continue
            matched_energy = energy_cluster
            used_energy_ids.add(energy_id)
            break

        system_label = _merge_system_label(
            capital_label,
            _coerce_string(matched_energy.get("system_label")) if matched_energy else None,
        )
        as_of_date = capital_cluster.get("as_of_date")
        demand_driver_summary = _coerce_string(capital_cluster.get("demand_driver_summary"))
        candidate = {
            "confidence": _merge_confidence(
                _coerce_string(capital_cluster.get("confidence")),
                _coerce_string(matched_energy.get("confidence")) if matched_energy else None,
            ),
            "pressure_candidate_id": _id_for_structural_candidate(system_label, as_of_date),
            "as_of_date": as_of_date,
            "status": "candidate",
            "pressure_type": "rising_demand",
            "system_label": system_label,
            "demand_driver_summary": demand_driver_summary,
            "pressure_statement": _pressure_statement(system_label, demand_driver_summary),
            "supporting_capital_flow_cluster_ids": [
                _coerce_string(capital_cluster.get("capital_flow_cluster_id"))
            ],
            "supporting_energy_flow_pressure_cluster_ids": (
                [_coerce_string(matched_energy.get("energy_flow_pressure_cluster_id"))]
                if matched_energy
                else []
            ),
            "merge_basis": {
                "system_overlap": bool(matched_energy),
                "time_overlap": bool(matched_energy),
                "direction_compatibility": True,
                "demand_story_overlap": demand_driver_summary if matched_energy else "capital_flow_only",
            },
            "signal_count": int(capital_cluster.get("signal_count", 0))
            + int(matched_energy.get("signal_count", 0) if matched_energy else 0),
            "source_classes": sorted(
                set(capital_cluster.get("source_classes", []))
                | set(matched_energy.get("source_classes", []) if matched_energy else [])
            ),
            "time_window": capital_cluster.get("time_window"),
            "suspected_stress_layers": [system_label],
            "formation_basis": {
                "capital_flow_cluster_present": True,
                "energy_flow_pressure_cluster_present": bool(matched_energy),
                "physical_system_grounded": True,
                "stress_rationale_present": True,
            },
        }
        (
            candidate["confidence"],
            candidate["source_diversity_status"],
            candidate["requires_source_diversity_corroboration"],
        ) = _apply_source_diversity_guardrail(
            candidate["confidence"],
            list(candidate["source_classes"]),
        )
        candidate["source_diversity_corroboration_satisfied"] = _source_diversity_corroboration_satisfied(
            list(candidate["source_classes"]),
            list(candidate["supporting_capital_flow_cluster_ids"]),
        )
        candidates.append(candidate)

    held_upstream_energy_clusters: List[str] = []
    for energy_cluster in energy_clusters:
        energy_id = _coerce_string(energy_cluster.get("energy_flow_pressure_cluster_id"))
        if energy_id in used_energy_ids:
            continue
        if _coerce_string(energy_cluster.get("system_label")) == "general energy-system pressure":
            held_upstream_energy_clusters.append(energy_id)
            used_energy_ids.add(energy_id)
            continue
        if energy_cluster.get("strong_infrastructure_response_evidence"):
            system_label = _coerce_string(energy_cluster.get("system_label"))
            as_of_date = energy_cluster.get("as_of_date")
            candidates.append(
                {
                    "confidence": _coerce_string(energy_cluster.get("confidence")) or "low",
                    "pressure_candidate_id": _id_for_structural_candidate(system_label, as_of_date),
                    "as_of_date": as_of_date,
                    "status": "candidate",
                    "pressure_type": "rising_demand",
                    "system_label": system_label,
                    "demand_driver_summary": _coerce_string(energy_cluster.get("cluster_statement")),
                    "pressure_statement": _coerce_string(energy_cluster.get("cluster_statement")),
                    "supporting_capital_flow_cluster_ids": [],
                    "supporting_energy_flow_pressure_cluster_ids": [energy_id],
                    "merge_basis": {
                        "system_overlap": False,
                        "time_overlap": False,
                        "direction_compatibility": True,
                        "demand_story_overlap": "energy_flow_only_with_infrastructure_response",
                    },
                    "signal_count": int(energy_cluster.get("signal_count", 0)),
                    "source_classes": list(energy_cluster.get("source_classes", [])),
                    "time_window": energy_cluster.get("time_window"),
                    "suspected_stress_layers": [system_label],
                    "formation_basis": {
                        "capital_flow_cluster_present": False,
                        "energy_flow_pressure_cluster_present": True,
                        "physical_system_grounded": True,
                        "stress_rationale_present": True,
                    },
                }
            )
            candidate = candidates[-1]
            (
                candidate["confidence"],
                candidate["source_diversity_status"],
                candidate["requires_source_diversity_corroboration"],
            ) = _apply_source_diversity_guardrail(
                candidate["confidence"],
                list(candidate["source_classes"]),
            )
            candidate["source_diversity_corroboration_satisfied"] = _source_diversity_corroboration_satisfied(
                list(candidate["source_classes"]),
                list(candidate["supporting_capital_flow_cluster_ids"]),
            )
        else:
            held_upstream_energy_clusters.append(energy_id)

    return {
        "name": "structural_pressure_candidate_batch_v1",
        "candidates": candidates,
        "held_upstream_energy_flow_pressure_cluster_ids": held_upstream_energy_clusters,
        "metrics": {
            "capital_cluster_count": len(capital_clusters),
            "energy_cluster_count": len(energy_clusters),
            "structural_pressure_candidate_count": len(candidates),
            "held_upstream_energy_cluster_count": len(held_upstream_energy_clusters),
        },
    }
