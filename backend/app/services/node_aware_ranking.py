"""
Node-aware ranking and review surface built from the canonical knowledge-node registry.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List


def _avg(values: Iterable[float], default: float = 0.0) -> float:
    values = [float(value) for value in values]
    if not values:
        return default
    return sum(values) / len(values)


def _frequency_sorted(values: Iterable[str]) -> List[str]:
    counts: Dict[str, int] = {}
    for value in values:
        if not value:
            continue
        counts[value] = counts.get(value, 0) + 1
    return [
        key for key, _ in sorted(
            counts.items(),
            key=lambda item: (item[1], item[0]),
            reverse=True,
        )
    ]


def _top_pointer(node: Dict[str, Any]) -> Dict[str, Any] | None:
    pointers = list(node.get("thesis_pointers", []))
    if not pointers:
        return None
    return max(
        pointers,
        key=lambda pointer: (
            float(pointer.get("ranking_score") or -1.0),
            float(pointer.get("promotion_score_0_to_100") or -1.0),
        ),
    )


def _expression_conflict(node: Dict[str, Any]) -> bool:
    expressions = sorted({
        pointer.get("final_expression")
        for pointer in node.get("thesis_pointers", [])
        if pointer.get("final_expression")
    })
    return len(expressions) > 1


def _node_score(node: Dict[str, Any]) -> float:
    aggregate = node.get("aggregate_view", {})
    pointers = list(node.get("thesis_pointers", []))
    top_ranking = float(aggregate.get("max_ranking_score") or 0.0)
    promotion_scores = [
        float(pointer.get("promotion_score_0_to_100") or 0.0)
        for pointer in pointers
    ]
    pointer_count = int(aggregate.get("pointer_count") or 0)
    theme_count = int(aggregate.get("theme_count") or 0)
    expression_conflict_penalty = 2.5 if _expression_conflict(node) else 0.0
    pointer_bonus = min(8.0, max(0.0, (pointer_count - 1) * 4.0))
    theme_bonus = min(4.0, max(0.0, (theme_count - 1) * 2.0))
    promotion_bonus = min(6.0, max(0.0, (_avg(promotion_scores, default=0.0) - 70.0) / 5.0))
    return round(top_ranking + pointer_bonus + theme_bonus + promotion_bonus - expression_conflict_penalty, 2)


def _pointer_summary(pointer: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "pointer_id": pointer.get("pointer_id"),
        "market_theme": pointer.get("market_theme"),
        "candidate_name": pointer.get("candidate_name"),
        "thesis": pointer.get("thesis"),
        "company_role": pointer.get("company_role"),
        "bottleneck_layer": pointer.get("bottleneck_layer"),
        "value_capture_layer": pointer.get("value_capture_layer"),
        "linked_process_layers": pointer.get("linked_process_layers", []),
        "linked_components": pointer.get("linked_components", []),
        "linked_materials": pointer.get("linked_materials", []),
        "final_expression": pointer.get("final_expression"),
        "ranking_score": pointer.get("ranking_score"),
        "promotion_status": pointer.get("promotion_status"),
        "promotion_score_0_to_100": pointer.get("promotion_score_0_to_100"),
    }


def build_node_aware_ranking(knowledge_node_registry: Dict[str, Any]) -> Dict[str, Any]:
    rows: List[Dict[str, Any]] = []

    for node in knowledge_node_registry.get("rows", []):
        pointers = list(node.get("thesis_pointers", []))
        if not pointers:
            continue

        top_pointer = _top_pointer(node)
        strongest_process_layers = _frequency_sorted(
            list(node.get("linked_process_layers", []))
            + [
                layer
                for pointer in pointers
                for layer in pointer.get("linked_process_layers", [])
            ]
        )[:5]
        strongest_components = _frequency_sorted(
            list(node.get("linked_components", []))
            + [
                component
                for pointer in pointers
                for component in pointer.get("linked_components", [])
            ]
        )[:5]
        strongest_materials = _frequency_sorted(
            list(node.get("linked_materials", []))
            + [
                material
                for pointer in pointers
                for material in pointer.get("linked_materials", [])
            ]
        )[:5]
        expression_views = sorted({
            pointer.get("final_expression")
            for pointer in pointers
            if pointer.get("final_expression")
        })
        rows.append(
            {
                "underlying": node.get("canonical_name"),
                "knowledge_node_id": node.get("knowledge_node_id"),
                "node_score": _node_score(node),
                "pointer_count": node.get("aggregate_view", {}).get("pointer_count", 0),
                "theme_count": node.get("aggregate_view", {}).get("theme_count", 0),
                "themes": node.get("aggregate_view", {}).get("themes", []),
                "primary_expression_view": (top_pointer or {}).get("final_expression"),
                "alternate_expression_views": [
                    expression
                    for expression in expression_views
                    if expression != (top_pointer or {}).get("final_expression")
                ],
                "expression_conflict": _expression_conflict(node),
                "strongest_supporting_process_layers": strongest_process_layers,
                "strongest_supporting_components": strongest_components,
                "strongest_supporting_materials": strongest_materials,
                "top_pointer": _pointer_summary(top_pointer) if top_pointer else None,
                "thesis_pointers": [
                    _pointer_summary(pointer)
                    for pointer in sorted(
                        pointers,
                        key=lambda pointer: (
                            float(pointer.get("ranking_score") or -1.0),
                            float(pointer.get("promotion_score_0_to_100") or -1.0),
                        ),
                        reverse=True,
                    )
                ],
                "parse_bindings": node.get("parse_entity_bindings", []),
            }
        )

    rows.sort(
        key=lambda row: (
            row["node_score"],
            row["pointer_count"],
            row["theme_count"],
        ),
        reverse=True,
    )

    return {
        "method": "canonical knowledge-node registry -> node-aware review ranking",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "row_count": len(rows),
        "rows": rows,
    }

