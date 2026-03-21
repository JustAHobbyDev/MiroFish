"""
Deterministic expansion planning from bounded-universe candidates.
"""

from __future__ import annotations

import hashlib
import re
from typing import Any, Dict, List


def _coerce_string(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def _expansion_plan_id(system_label: str, as_of_date: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "_", system_label.lower()).strip("_")
    suffix = as_of_date or "unknown_date"
    digest = hashlib.sha1(f"{slug}|{suffix}".encode("utf-8")).hexdigest()[:8]
    return f"bue_{slug}_{suffix}_{digest}"


def _expansion_template(system_label: str) -> Dict[str, Any]:
    templates = {
        "grid equipment and transformer buildout": {
            "entity_lane_hints": [
                "transformer manufacturers",
                "switchgear manufacturers",
                "substation equipment suppliers",
                "grid equipment component suppliers",
                "core, coil, insulation, and conductor input suppliers",
            ],
            "query_seed_terms": [
                "transformer production expansion",
                "switchgear manufacturing expansion",
                "substation equipment capacity",
                "transformer backlog",
                "grid equipment lead times",
                "core and coil manufacturing",
            ],
            "negative_boundaries": [
                "generic industrial manufacturing",
                "consumer electrical products",
                "non-grid building wiring products",
            ],
            "first_actions": [
                "Confirm visible beneficiary manufacturers from mixed-source public evidence.",
                "Expand upstream from transformers, switchgear, and substation equipment into component and material layers.",
                "Pull company filings only for entities that appear inside the bounded system lane.",
            ],
        },
        "data center power demand buildout": {
            "entity_lane_hints": [
                "utilities serving hyperscale corridors",
                "substation and transformer suppliers",
                "power-delivery equipment providers",
                "cooling and power-distribution infrastructure suppliers",
            ],
            "query_seed_terms": [
                "data center campus power expansion",
                "substation buildout for data centers",
                "utility interconnection for hyperscale",
                "transformer demand for data centers",
            ],
            "negative_boundaries": [
                "generic cloud software demand",
                "enterprise IT without physical buildout",
            ],
            "first_actions": [
                "Confirm which utilities and equipment layers recur across the bounded power-delivery lane.",
                "Expand from visible beneficiaries into transformer, substation, and cooling-power layers.",
            ],
        },
    }
    return templates.get(
        system_label,
        {
            "entity_lane_hints": [system_label],
            "query_seed_terms": [system_label],
            "negative_boundaries": [],
            "first_actions": ["Expand only inside the bounded system label and named stress layers."],
        },
    )


def build_bounded_universe_expansion_batch(
    bounded_universe_batch: Dict[str, Any],
) -> Dict[str, Any]:
    plans: List[Dict[str, Any]] = []
    for candidate in bounded_universe_batch.get("candidates", []):
        system_label = _coerce_string(candidate.get("system_label"))
        as_of_date = _coerce_string(candidate.get("as_of_date"))
        template = _expansion_template(system_label)
        plans.append(
            {
                "bounded_universe_expansion_plan_id": _expansion_plan_id(system_label, as_of_date),
                "as_of_date": as_of_date,
                "status": "candidate",
                "origin_bounded_universe_candidate_id": _coerce_string(candidate.get("bounded_universe_candidate_id")),
                "system_label": system_label,
                "expansion_objective": f"Expand the {system_label} universe into a reviewable company and supplier set without leaving the bounded lane.",
                "entity_lane_hints": template["entity_lane_hints"],
                "query_seed_terms": template["query_seed_terms"],
                "negative_boundaries": template["negative_boundaries"],
                "first_actions": template["first_actions"],
                "source_classes_priority": list(candidate.get("next_source_classes", [])),
                "suspected_stress_layers": list(candidate.get("suspected_stress_layers", [])),
                "confidence": _coerce_string(candidate.get("confidence")) or "low",
            }
        )

    return {
        "name": "bounded_universe_expansion_batch_v1",
        "plans": plans,
        "metrics": {
            "input_bounded_universe_candidate_count": len(bounded_universe_batch.get("candidates", [])),
            "bounded_universe_expansion_plan_count": len(plans),
        },
    }
