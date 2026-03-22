"""
Deterministic formation of bounded-universe candidates from structural-pressure candidates.
"""

from __future__ import annotations

import hashlib
import re
from typing import Any, Dict, List


def _coerce_string(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def _bounded_universe_id(system_label: str, as_of_date: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "_", system_label.lower()).strip("_")
    suffix = as_of_date or "unknown_date"
    digest = hashlib.sha1(f"{slug}|{suffix}".encode("utf-8")).hexdigest()[:8]
    return f"buc_{slug}_{suffix}_{digest}"


def _suspected_stress_layers(system_label: str) -> List[str]:
    mapping = {
        "grid equipment and transformer buildout": [
            "transformers",
            "switchgear",
            "substation equipment",
            "grid equipment components",
        ],
        "grid equipment and transformer pressure": [
            "transformers",
            "switchgear",
            "substation equipment",
        ],
        "data center power demand buildout": [
            "utility interconnection",
            "substations",
            "transformers",
            "cooling and power-delivery infrastructure",
        ],
        "utility and large-load power buildout": [
            "utility interconnection",
            "substations",
            "transformers",
            "generation response",
            "large-load service infrastructure",
        ],
        "utility and large-load power demand pressure": [
            "utility interconnection",
            "substations",
            "transformers",
            "generation response",
        ],
    }
    return mapping.get(system_label, [system_label])


def _review_universe_definition(system_label: str) -> str:
    mapping = {
        "grid equipment and transformer buildout": "Companies, suppliers, facilities, inputs, and public artifacts tied to transformer, switchgear, substation, and adjacent grid-equipment expansion.",
        "grid equipment and transformer pressure": "Companies, suppliers, facilities, inputs, and public artifacts tied to transformer, switchgear, substation, and adjacent grid-equipment capacity pressure.",
        "data center power demand buildout": "Companies, utilities, suppliers, facilities, and public artifacts tied to data-center power delivery, interconnection, substations, transformers, and adjacent support infrastructure.",
        "utility and large-load power buildout": "Utilities, large-load operators, power-delivery suppliers, and public artifacts tied to interconnection, substations, transformers, generation response, and adjacent utility-system expansion.",
        "utility and large-load power demand pressure": "Utilities, suppliers, facilities, and public artifacts tied to large-load growth, interconnection, substations, transformers, and generation-response needs.",
    }
    return mapping.get(system_label, f"Public artifacts and entities tied to {system_label}.")


def _next_source_classes(system_label: str, source_classes: List[str]) -> List[str]:
    recommended = list(source_classes)
    for item in ("company_release", "trade_press", "company_filing"):
        if item not in recommended:
            recommended.append(item)
    if "government" not in recommended and "power" in system_label:
        recommended.append("government")
    return recommended


def _research_ready_exploratory_candidate(pressure_candidate: Dict[str, Any]) -> bool:
    system_label = _coerce_string(pressure_candidate.get("system_label")).lower()
    return (
        not bool(pressure_candidate.get("bounded_universe_promotion_ready"))
        and not bool(pressure_candidate.get("requires_system_narrowing"))
        and _coerce_string(pressure_candidate.get("boundedness_status")) == "bounded"
        and "buildout" in system_label
    )


def _candidate_status(pressure_candidate: Dict[str, Any]) -> str:
    if bool(pressure_candidate.get("bounded_universe_promotion_ready")):
        return "candidate"
    return "exploratory_candidate"


def build_bounded_universe_candidate_batch(
    structural_pressure_batch: Dict[str, Any],
) -> Dict[str, Any]:
    candidates: List[Dict[str, Any]] = []
    for pressure_candidate in structural_pressure_batch.get("candidates", []):
        promotion_ready = bool(pressure_candidate.get("bounded_universe_promotion_ready"))
        exploratory_ready = _research_ready_exploratory_candidate(pressure_candidate)
        if not promotion_ready and not exploratory_ready:
            continue
        system_label = _coerce_string(pressure_candidate.get("system_label"))
        as_of_date = _coerce_string(pressure_candidate.get("as_of_date"))
        source_classes = list(pressure_candidate.get("source_classes", []))
        candidates.append(
            {
                "bounded_universe_candidate_id": _bounded_universe_id(system_label, as_of_date),
                "as_of_date": as_of_date,
                "status": _candidate_status(pressure_candidate),
                "origin_pressure_candidate_id": _coerce_string(pressure_candidate.get("pressure_candidate_id")),
                "universe_label": f"{system_label} universe",
                "system_label": system_label,
                "bounding_basis": {
                    "source_diversity_corroborated": bool(
                        pressure_candidate.get("source_diversity_corroboration_satisfied")
                    ),
                    "system_bounded": not bool(pressure_candidate.get("requires_system_narrowing")),
                    "research_ready": promotion_ready or exploratory_ready,
                    "promotion_ready": promotion_ready,
                    "exploration_only": exploratory_ready and not promotion_ready,
                },
                "review_universe_definition": _review_universe_definition(system_label),
                "next_source_classes": _next_source_classes(system_label, source_classes),
                "suspected_stress_layers": _suspected_stress_layers(system_label),
                "visible_beneficiary_hints": list(pressure_candidate.get("likely_visible_beneficiaries", [])),
                "confidence": _coerce_string(pressure_candidate.get("confidence")) or "low",
                "supporting_pressure_candidate_ids": [_coerce_string(pressure_candidate.get("pressure_candidate_id"))],
            }
        )

    return {
        "name": "bounded_universe_candidate_batch_v1",
        "candidates": candidates,
        "metrics": {
            "input_pressure_candidate_count": len(structural_pressure_batch.get("candidates", [])),
            "bounded_universe_candidate_count": len(candidates),
            "promotion_ready_candidate_count": len(
                [item for item in candidates if item["bounding_basis"]["promotion_ready"]]
            ),
            "exploratory_candidate_count": len(
                [item for item in candidates if item["bounding_basis"]["exploration_only"]]
            ),
        },
    }
