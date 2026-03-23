"""
Anchor-first replay builder for retrospective historical corpora.
"""

from __future__ import annotations

from typing import Any, Dict, List

from .anchor_expression_builder import build_anchor_expression_batch


def _coerce_string(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def build_anchor_first_blind_replay_batch(
    prefilter_batches: List[Dict[str, Any]],
    *,
    profile_name: str = "photonics",
    corpus_label: str = "",
    include_review: bool = True,
    include_synthetic: bool = False,
) -> Dict[str, Any]:
    anchor_batch = build_anchor_expression_batch(
        prefilter_batches,
        profile_name=profile_name,
        include_review=include_review,
        include_synthetic=include_synthetic,
    )

    anchors = list(anchor_batch.get("anchors", []))
    surfaced_names = {item.get("canonical_entity_name") for item in anchors}
    role_counts = anchor_batch.get("metrics", {}).get("anchor_expression_role_counts", {})
    hidden_chokepoint_surfaced = "AXT" in surfaced_names and any(
        item.get("anchor_role") == "upstream_dependency" and item.get("canonical_entity_name") == "AXT"
        for item in anchors
    )

    result = {
        "name": "anchor_first_blind_replay_batch_v1",
        "corpus_label": corpus_label,
        "profile_name": profile_name,
        "coverage_status": "retrospective_seeded_not_blind_ready",
        "anchors": anchors,
        "judgment": {
            "anchor_clue_detection": "pass" if "Lumentum" in surfaced_names else "fail",
            "adjacent_expression_surfacing": "pass" if "Coherent" in surfaced_names else "fail",
            "upstream_dependency_surfacing": (
                "pass" if any(item.get("anchor_role") == "upstream_dependency" for item in anchors) else "fail"
            ),
            "hidden_chokepoint_recovery": "pass" if hidden_chokepoint_surfaced else "fail",
        },
        "limitations": [
            "This replay uses a retrospective-seeded corpus, not a true blind source universe.",
            "A pass on hidden chokepoint recovery here means the named upstream chokepoint surfaced inside the seeded corpus, not that blind discovery is proven.",
            "The result tests anchor-first surfacing only; it does not prove final-expression discovery in a true blind corpus.",
        ],
        "metrics": {
            "anchor_expression_count": len(anchors),
            "anchor_expression_role_counts": role_counts,
            "anchor_expression_names": [item.get("canonical_entity_name") for item in anchors],
        },
    }
    return result
