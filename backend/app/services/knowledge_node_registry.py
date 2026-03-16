"""
Canonical knowledge-node registry for cross-parse aggregation.

v1 focuses on underlying-level aggregation so one public company can collect
multiple thesis pointers from separate promoted parses.
"""

from __future__ import annotations

from datetime import datetime, timezone
import re
from typing import Any, Dict, Iterable, List, Tuple


def _slugify(value: str) -> str:
    text = re.sub(r"[^a-zA-Z0-9]+", "_", value.strip().lower())
    return text.strip("_") or "unknown"


def _pointer_key(row: Dict[str, Any]) -> Tuple[str, str, str, str]:
    return (
        row.get("underlying", ""),
        row.get("market_theme", ""),
        row.get("bottleneck_layer", ""),
        row.get("value_capture_layer", ""),
    )


def _ensure_underlying_node(nodes: Dict[str, Dict[str, Any]], symbol: str) -> Dict[str, Any]:
    key = symbol.upper()
    existing = nodes.get(key)
    if existing:
        return existing

    knowledge_node_id = f"kn_underlying_{_slugify(key)}"
    node = {
        "knowledge_node_id": knowledge_node_id,
        "node_type": "Underlying",
        "canonical_key": f"ticker:{key}",
        "canonical_name": key,
        "aliases": [],
        "resolution_basis": {
            "ticker": key,
            "resolver_version": "v1",
        },
        "parse_entity_bindings": [],
        "thesis_pointers": [],
        "linked_themes": [],
        "linked_process_layers": [],
        "linked_components": [],
        "linked_materials": [],
        "expression_views": [],
        "aggregate_view": {},
    }
    nodes[key] = node
    return node


def _append_unique(items: List[Any], value: Any) -> None:
    if value not in items:
        items.append(value)


def _iter_public_company_bindings(parse_records: Iterable[Dict[str, Any]]) -> Iterable[Dict[str, Any]]:
    for record in parse_records:
        structural_parse = record.get("structural_parse", {})
        for entity in structural_parse.get("entities", []):
            if entity.get("entity_type") != "PublicCompany":
                continue
            yield {
                "parse_name": record.get("name"),
                "structural_parse_path": record.get("structural_parse_path"),
                "graduation_status": record.get("graduation_status"),
                "graduation_score_0_to_100": record.get("graduation_score_0_to_100"),
                "local_entity_id": entity.get("entity_id"),
                "local_entity_type": entity.get("entity_type"),
                "local_canonical_name": entity.get("canonical_name"),
                "local_attributes": entity.get("attributes", {}),
            }


def _ranked_index(rows: Iterable[Dict[str, Any]]) -> Dict[Tuple[str, str, str, str], Dict[str, Any]]:
    return {
        _pointer_key(row): row
        for row in rows
    }


def _pointer_from_rows(candidate_row: Dict[str, Any], ranked_row: Dict[str, Any] | None) -> Dict[str, Any]:
    decomposition = candidate_row.get("theme_equity_decomposition") or {}
    return {
        "pointer_id": f"ptr_{_slugify(candidate_row.get('underlying', 'unknown'))}_{_slugify(candidate_row.get('market_theme', 'theme'))}_{_slugify(candidate_row.get('bottleneck_layer', 'layer'))}",
        "candidate_name": candidate_row.get("name"),
        "market_theme": candidate_row.get("market_theme"),
        "thesis": candidate_row.get("thesis"),
        "bottleneck_layer": candidate_row.get("bottleneck_layer"),
        "value_capture_layer": candidate_row.get("value_capture_layer"),
        "promotion_status": candidate_row.get("promotion_status"),
        "promotion_score_0_to_100": candidate_row.get("promotion_score_0_to_100"),
        "company_role": decomposition.get("company_role"),
        "linked_process_layers": decomposition.get("linked_process_layers", []),
        "linked_components": decomposition.get("linked_components", []),
        "linked_materials": decomposition.get("linked_materials", []),
        "market_miss_alignment_score_0_to_100": decomposition.get("market_miss_alignment_score_0_to_100"),
        "value_capture_alignment_score_0_to_100": decomposition.get("value_capture_alignment_score_0_to_100"),
        "expression_readiness_score_0_to_100": decomposition.get("expression_readiness_score_0_to_100"),
        "decomposition_confidence": decomposition.get("decomposition_confidence"),
        "final_expression": (ranked_row or {}).get("final_expression"),
        "ranking_score": (ranked_row or {}).get("ranking_score"),
        "pick_score": (ranked_row or {}).get("pick_score"),
    }


def _summarize_node(node: Dict[str, Any]) -> Dict[str, Any]:
    pointers = list(node.get("thesis_pointers", []))
    bindings = list(node.get("parse_entity_bindings", []))
    ranking_scores = [
        float(pointer.get("ranking_score"))
        for pointer in pointers
        if pointer.get("ranking_score") is not None
    ]
    promotion_scores = [
        float(pointer.get("promotion_score_0_to_100"))
        for pointer in pointers
        if pointer.get("promotion_score_0_to_100") is not None
    ]
    final_expressions = sorted({
        pointer.get("final_expression")
        for pointer in pointers
        if pointer.get("final_expression")
    })
    themes = sorted({
        pointer.get("market_theme")
        for pointer in pointers
        if pointer.get("market_theme")
    })
    top_pointer = None
    if pointers and ranking_scores:
        top_pointer = max(
            pointers,
            key=lambda pointer: float(pointer.get("ranking_score") or -1),
        ).get("pointer_id")

    return {
        "pointer_count": len(pointers),
        "parse_binding_count": len(bindings),
        "theme_count": len(themes),
        "themes": themes,
        "expression_views": final_expressions,
        "max_ranking_score": round(max(ranking_scores), 2) if ranking_scores else None,
        "max_promotion_score_0_to_100": round(max(promotion_scores), 2) if promotion_scores else None,
        "top_pointer_id": top_pointer,
    }


def build_knowledge_node_registry(
    parse_records: List[Dict[str, Any]],
    candidate_rows: List[Dict[str, Any]],
    ranked_rows: List[Dict[str, Any]],
) -> Dict[str, Any]:
    nodes: Dict[str, Dict[str, Any]] = {}
    ranked_by_key = _ranked_index(ranked_rows)

    for binding in _iter_public_company_bindings(parse_records):
        symbol = str(binding.get("local_canonical_name") or "").upper()
        if not symbol:
            continue
        node = _ensure_underlying_node(nodes, symbol)
        if binding not in node["parse_entity_bindings"]:
            node["parse_entity_bindings"].append(binding)

    for row in candidate_rows:
        symbol = str(row.get("underlying") or "").upper()
        if not symbol:
            continue
        node = _ensure_underlying_node(nodes, symbol)
        ranked_row = ranked_by_key.get(_pointer_key(row))
        pointer = _pointer_from_rows(row, ranked_row)
        if pointer not in node["thesis_pointers"]:
            node["thesis_pointers"].append(pointer)

        _append_unique(node["linked_themes"], row.get("market_theme"))
        _append_unique(node["linked_process_layers"], row.get("bottleneck_layer"))
        _append_unique(node["linked_process_layers"], row.get("value_capture_layer"))

        decomposition = row.get("theme_equity_decomposition") or {}
        for value in decomposition.get("linked_process_layers", []):
            _append_unique(node["linked_process_layers"], value)
        for value in decomposition.get("linked_components", []):
            _append_unique(node["linked_components"], value)
        for value in decomposition.get("linked_materials", []):
            _append_unique(node["linked_materials"], value)

        final_expression = (ranked_row or {}).get("final_expression")
        if final_expression:
            _append_unique(node["expression_views"], final_expression)

    rows = []
    for symbol in sorted(nodes):
        node = nodes[symbol]
        node["linked_themes"] = [value for value in node["linked_themes"] if value]
        node["linked_process_layers"] = [value for value in node["linked_process_layers"] if value]
        node["linked_components"] = [value for value in node["linked_components"] if value]
        node["linked_materials"] = [value for value in node["linked_materials"] if value]
        node["aggregate_view"] = _summarize_node(node)
        rows.append(node)

    rows.sort(
        key=lambda node: (
            node["aggregate_view"].get("max_ranking_score") or 0.0,
            node["aggregate_view"].get("pointer_count") or 0,
        ),
        reverse=True,
    )

    return {
        "registry_version": "v1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "node_type_scope": ["Underlying"],
        "row_count": len(rows),
        "rows": rows,
        "summary": {
            "underlying_count": len(rows),
            "multi_pointer_underlyings": [
                row["canonical_name"]
                for row in rows
                if row["aggregate_view"].get("pointer_count", 0) > 1
            ],
        },
    }

