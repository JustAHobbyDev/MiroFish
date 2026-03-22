"""
Deterministic consolidation of utility-lane downstream state.
"""

from __future__ import annotations

from typing import Any, Dict

from .bounded_entity_downstream_state_builder import build_bounded_entity_downstream_state


def build_utility_lane_downstream_state(
    followup_queue_batch: Dict[str, Any],
    filing_support_batch: Dict[str, Any],
    private_diligence_batch: Dict[str, Any],
) -> Dict[str, Any]:
    return build_bounded_entity_downstream_state(
        followup_queue_batch,
        filing_support_batch,
        private_diligence_batch,
        output_name="utility_lane_downstream_state_v1",
    )
