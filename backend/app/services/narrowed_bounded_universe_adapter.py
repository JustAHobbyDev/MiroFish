"""
Adapt narrowed structural-pressure candidates into bounded-universe candidates.
"""

from __future__ import annotations

import hashlib
import re
from typing import Any, Dict, List


def _coerce_string(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def _candidate_id(system_label: str, narrowed_id: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "_", system_label.lower()).strip("_")
    digest = hashlib.sha1(f"{slug}|{narrowed_id}".encode("utf-8")).hexdigest()[:8]
    return f"buc_{slug}_{digest}"


def _extract_as_of_date(candidate: Dict[str, Any]) -> str:
    narrowed_id = _coerce_string(candidate.get("narrowed_pressure_candidate_id"))
    match = re.search(r"(20\d{2})_(\d{2})_(\d{2})$", narrowed_id)
    if not match:
        return ""
    return f"{match.group(1)}-{match.group(2)}-{match.group(3)}"


def _review_universe_definition(system_label: str) -> str:
    if system_label == "data center backup-power equipment buildout":
        return (
            "Manufacturers, suppliers, and public artifacts tied to backup-power "
            "engines, generator packages, generator enclosures, and adjacent data-center "
            "onsite-power equipment buildout."
        )
    return f"Public artifacts and entities tied to {system_label}."


def build_narrowed_bounded_universe_candidate_batch(
    narrowing_batch: Dict[str, Any],
) -> Dict[str, Any]:
    candidates: List[Dict[str, Any]] = []

    for narrowed in narrowing_batch.get("narrowed_candidates", []):
        system_label = _coerce_string(narrowed.get("system_label"))
        narrowed_id = _coerce_string(narrowed.get("narrowed_pressure_candidate_id"))
        as_of_date = _extract_as_of_date(narrowed)
        narrowing_basis = dict(narrowed.get("narrowing_basis", {}))
        source_classes = list(narrowing_basis.get("source_classes", []))

        candidates.append(
            {
                "bounded_universe_candidate_id": _candidate_id(system_label, narrowed_id),
                "as_of_date": as_of_date,
                "status": "exploratory_candidate",
                "origin_pressure_candidate_id": _coerce_string(narrowed.get("origin_pressure_candidate_id")),
                "origin_narrowed_pressure_candidate_id": narrowed_id,
                "universe_label": f"{system_label} universe",
                "system_label": system_label,
                "bounding_basis": {
                    "source_diversity_corroborated": False,
                    "system_bounded": _coerce_string(narrowing_basis.get("boundedness_status")) == "bounded",
                    "research_ready": bool(narrowing_basis.get("research_ready")),
                    "promotion_ready": False,
                    "exploration_only": True,
                    "support_provenance_status": _coerce_string(
                        narrowing_basis.get("support_provenance_status")
                    ),
                },
                "review_universe_definition": _review_universe_definition(system_label),
                # Keep this lane on real trade-press support until we have real multi-source corroboration.
                "next_source_classes": [item for item in source_classes if item == "trade_press"] or source_classes,
                "suspected_stress_layers": list(narrowed.get("suspected_stress_layers", [])),
                "visible_beneficiary_hints": [],
                "confidence": "medium",
                "supporting_pressure_candidate_ids": [_coerce_string(narrowed.get("origin_pressure_candidate_id"))],
                "supporting_narrowed_pressure_candidate_ids": [narrowed_id],
            }
        )

    return {
        "name": "narrowed_bounded_universe_candidate_batch_v1",
        "candidates": candidates,
        "metrics": {
            "input_narrowed_candidate_count": len(narrowing_batch.get("narrowed_candidates", [])),
            "bounded_universe_candidate_count": len(candidates),
        },
    }
