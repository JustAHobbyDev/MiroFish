"""
Deterministic photonics dependency graph from AleaBito chronology roles.
"""

from __future__ import annotations

import hashlib
import re
from typing import Any, Dict, List


ENTITY_ALIAS_MAP = {
    "LITE": "Lumentum",
    "COHR": "Coherent",
    "AAOI": "Applied Optoelectronics",
    "AXTI": "AXT",
}


def _coerce_string(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def _node_id(name: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "_", name.lower()).strip("_")
    digest = hashlib.sha1(slug.encode("utf-8")).hexdigest()[:8]
    return f"pdg_node_{slug}_{digest}"


def _edge_id(source_name: str, target_name: str, relation_type: str) -> str:
    key = f"{source_name}|{target_name}|{relation_type}"
    digest = hashlib.sha1(key.encode("utf-8")).hexdigest()[:8]
    return f"pdg_edge_{digest}"


def build_photonics_dependency_graph(
    workflow_batch: Dict[str, Any],
) -> Dict[str, Any]:
    chronology = list(workflow_batch.get("chronology", []))
    role_by_expression = {
        _coerce_string(item.get("expression")): _coerce_string(item.get("role"))
        for item in chronology
        if _coerce_string(item.get("expression"))
    }

    ordered_expressions = ["LITE", "COHR", "AAOI", "AXTI"]
    nodes: List[Dict[str, Any]] = []
    for expression in ordered_expressions:
        canonical_name = ENTITY_ALIAS_MAP[expression]
        nodes.append(
            {
                "node_id": _node_id(canonical_name),
                "expression": expression,
                "canonical_entity_name": canonical_name,
                "chain_role": role_by_expression.get(expression, ""),
            }
        )

    edges = [
        {
            "edge_id": _edge_id("Lumentum", "Coherent", "adjacent_duopoly_context"),
            "source_entity_name": "Lumentum",
            "target_entity_name": "Coherent",
            "relation_type": "adjacent_duopoly_context",
            "evidence_basis": "archive_duopoly_framing",
        },
        {
            "edge_id": _edge_id("Lumentum", "Applied Optoelectronics", "levered_adjacent_expression"),
            "source_entity_name": "Lumentum",
            "target_entity_name": "Applied Optoelectronics",
            "relation_type": "levered_adjacent_expression",
            "evidence_basis": "archive_customer_leverage_framing",
        },
        {
            "edge_id": _edge_id("Lumentum", "AXT", "upstream_material_dependency"),
            "source_entity_name": "Lumentum",
            "target_entity_name": "AXT",
            "relation_type": "upstream_material_dependency",
            "evidence_basis": "archive_material_supplier_framing",
        },
        {
            "edge_id": _edge_id("Coherent", "AXT", "shared_inp_dependency"),
            "source_entity_name": "Coherent",
            "target_entity_name": "AXT",
            "relation_type": "shared_inp_dependency",
            "evidence_basis": "archive_shared_InP_constraint_framing",
        },
        {
            "edge_id": _edge_id("Applied Optoelectronics", "Lumentum", "compared_against_anchor"),
            "source_entity_name": "Applied Optoelectronics",
            "target_entity_name": "Lumentum",
            "relation_type": "compared_against_anchor",
            "evidence_basis": "archive_relative_expression_framing",
        },
    ]

    return {
        "name": "photonics_dependency_graph_v1",
        "source_workflow_artifact_id": _coerce_string(workflow_batch.get("artifact_id")),
        "nodes": nodes,
        "edges": edges,
        "metrics": {
            "node_count": len(nodes),
            "edge_count": len(edges),
        },
    }
