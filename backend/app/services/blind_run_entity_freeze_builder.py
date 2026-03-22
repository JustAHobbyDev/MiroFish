"""
Deterministic entity-freeze extension for blind runs.
"""

from __future__ import annotations

from typing import Any, Dict, List

from .bounded_entity_candidate_builder import build_bounded_entity_candidate_batch
from .bounded_research_set_builder import build_bounded_research_set_batch
from .bounded_universe_expander import build_bounded_universe_expansion_batch


def build_blind_run_entity_freeze_batch(
    bounded_universe_batch: Dict[str, Any],
    prefilter_batches: List[Dict[str, Any]],
) -> Dict[str, Any]:
    expansion_batch = build_bounded_universe_expansion_batch(bounded_universe_batch)
    research_set_batch = build_bounded_research_set_batch(expansion_batch, prefilter_batches)
    entity_candidate_batch = build_bounded_entity_candidate_batch(research_set_batch)

    return {
        "name": "blind_run_entity_freeze_batch_v1",
        "expansion_plans": expansion_batch.get("plans", []),
        "research_sets": research_set_batch.get("research_sets", []),
        "entity_candidates": entity_candidate_batch.get("candidates", []),
        "metrics": {
            "input_bounded_universe_candidate_count": len(bounded_universe_batch.get("candidates", [])),
            "expansion_plan_count": len(expansion_batch.get("plans", [])),
            "bounded_research_set_count": len(research_set_batch.get("research_sets", [])),
            "bounded_entity_candidate_count": len(entity_candidate_batch.get("candidates", [])),
        },
    }
