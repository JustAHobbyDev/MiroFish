#!/usr/bin/env python3
"""
Evaluate whether a structural parse should remain exploratory, move to a
watchlist candidate, or graduate to a pick candidate.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List, Tuple


HIGH_QUALITY_SOURCES = {"high"}
EVIDENCE_MODES = {"evidence"}
COMPANY_DRIVEN_CLASSES = {"company_release", "earnings_transcript"}


def _clamp(value: float, low: float = 0.0, high: float = 100.0) -> float:
    return max(low, min(high, value))


def _pct(numerator: float, denominator: float) -> float:
    if denominator <= 0:
        return 0.0
    return numerator / denominator


def _source_mix_score(source_bundle: Dict[str, Any]) -> Tuple[float, Dict[str, Any]]:
    sources = source_bundle.get("sources", [])
    total = len(sources)
    if total == 0:
        return 0.0, {"reason": "no sources"}

    evidence_count = sum(1 for source in sources if source.get("usage_mode") in EVIDENCE_MODES)
    high_quality_count = sum(
        1 for source in sources if source.get("source_quality") in HIGH_QUALITY_SOURCES
    )
    independent_count = sum(
        1
        for source in sources
        if source.get("source_class") not in COMPANY_DRIVEN_CLASSES
    )
    source_classes = {source.get("source_class", "unknown") for source in sources}

    score = (
        _pct(evidence_count, total) * 45.0
        + _pct(high_quality_count, total) * 30.0
        + _pct(independent_count, total) * 15.0
        + min(len(source_classes), 5) / 5.0 * 10.0
    )
    return round(_clamp(score), 2), {
        "total_sources": total,
        "evidence_count": evidence_count,
        "high_quality_count": high_quality_count,
        "independent_count": independent_count,
        "source_classes": sorted(source_classes),
    }


def _structure_score(structural_parse: Dict[str, Any]) -> Tuple[float, Dict[str, Any]]:
    entities = structural_parse.get("entities", [])
    relationships = structural_parse.get("relationships", [])
    claims = structural_parse.get("claims", [])
    evidence_links = structural_parse.get("evidence_links", [])
    inferences = structural_parse.get("inferences", [])

    entity_types = {entity.get("entity_type") for entity in entities}
    relationship_types = {relationship.get("relationship_type") for relationship in relationships}

    required_entity_hits = {
        "Theme",
        "ProcessLayer",
        "PublicCompany",
    } & entity_types
    required_relationship_hits = {
        "SUPPLIED_BY",
        "DEPENDS_ON",
    } & relationship_types

    score = (
        min(len(entities), 20) / 20.0 * 25.0
        + min(len(relationships), 15) / 15.0 * 25.0
        + min(len(claims), 7) / 7.0 * 20.0
        + min(len(evidence_links), 20) / 20.0 * 15.0
        + min(len(inferences), 1) * 10.0
        + (_pct(len(required_entity_hits), 3) * 3.0)
        + (_pct(len(required_relationship_hits), 2) * 2.0)
    )
    return round(_clamp(score), 2), {
        "entity_count": len(entities),
        "relationship_count": len(relationships),
        "claim_count": len(claims),
        "evidence_link_count": len(evidence_links),
        "inference_count": len(inferences),
        "entity_types": sorted(entity_types),
        "relationship_types": sorted(relationship_types),
    }


def _market_miss_score(structural_parse: Dict[str, Any]) -> Tuple[float, Dict[str, Any]]:
    inferences = structural_parse.get("inferences", [])
    market_miss = [
        inference for inference in inferences if inference.get("inference_type") == "market_miss"
    ]
    if not market_miss:
        return 0.0, {"reason": "no market_miss inference"}

    best = market_miss[0]
    confidence = best.get("confidence", "low")
    confidence_score = {"low": 18.0, "medium": 30.0, "high": 40.0}.get(confidence, 18.0)
    claim_support = min(len(best.get("derived_from_claim_ids", [])), 6) / 6.0 * 35.0
    relationship_support = min(len(best.get("derived_from_relationship_ids", [])), 10) / 10.0 * 25.0
    score = confidence_score + claim_support + relationship_support
    return round(_clamp(score), 2), {
        "statement": best.get("statement"),
        "confidence": confidence,
        "derived_claim_count": len(best.get("derived_from_claim_ids", [])),
        "derived_relationship_count": len(best.get("derived_from_relationship_ids", [])),
    }


def _expression_score(structural_parse: Dict[str, Any]) -> Tuple[float, Dict[str, Any]]:
    entities = structural_parse.get("entities", [])
    relationships = structural_parse.get("relationships", [])

    expression_entities = [
        entity for entity in entities if entity.get("entity_type") == "ExpressionCandidate"
    ]
    has_expression = bool(expression_entities)
    relationship_types = {relationship.get("relationship_type") for relationship in relationships}
    expression_links = {
        "CANDIDATE_EXPRESSION_FOR",
        "REPRICES_VIA",
    } & relationship_types

    score = (40.0 if has_expression else 0.0) + _pct(len(expression_links), 2) * 60.0
    return round(_clamp(score), 2), {
        "expression_count": len(expression_entities),
        "expression_names": [entity.get("canonical_name") for entity in expression_entities],
        "expression_relationships_present": sorted(expression_links),
    }


def evaluate_parse(
    source_bundle: Dict[str, Any], structural_parse: Dict[str, Any]
) -> Dict[str, Any]:
    source_mix_score, source_mix_detail = _source_mix_score(source_bundle)
    structure_score, structure_detail = _structure_score(structural_parse)
    market_miss_score, market_miss_detail = _market_miss_score(structural_parse)
    expression_score, expression_detail = _expression_score(structural_parse)

    weighted_score = round(
        source_mix_score * 0.30
        + structure_score * 0.25
        + market_miss_score * 0.30
        + expression_score * 0.15,
        2,
    )

    source_gate = source_mix_score >= 45
    structure_gate = structure_score >= 60
    market_miss_gate = market_miss_score >= 60
    expression_gate = expression_score >= 50
    high_conviction_source_gate = source_mix_score >= 70

    if source_gate and structure_gate and market_miss_gate and expression_gate and high_conviction_source_gate:
        status = "pick_candidate"
    elif source_gate and structure_gate and market_miss_gate:
        status = "watchlist_candidate"
    else:
        status = "exploratory_only"

    return {
        "graduation_status": status,
        "weighted_score_0_to_100": weighted_score,
        "gates": {
            "source_gate": source_gate,
            "structure_gate": structure_gate,
            "market_miss_gate": market_miss_gate,
            "expression_gate": expression_gate,
            "high_conviction_source_gate": high_conviction_source_gate,
        },
        "dimensions": {
            "source_mix": {
                "score_0_to_100": source_mix_score,
                "detail": source_mix_detail,
            },
            "structure_quality": {
                "score_0_to_100": structure_score,
                "detail": structure_detail,
            },
            "market_miss_quality": {
                "score_0_to_100": market_miss_score,
                "detail": market_miss_detail,
            },
            "expression_readiness": {
                "score_0_to_100": expression_score,
                "detail": expression_detail,
            },
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source_bundle", type=Path)
    parser.add_argument("structural_parse", type=Path)
    parser.add_argument("-o", "--output", type=Path)
    args = parser.parse_args()

    source_bundle = json.loads(args.source_bundle.read_text(encoding="utf-8"))
    structural_parse = json.loads(args.structural_parse.read_text(encoding="utf-8"))
    output = evaluate_parse(source_bundle, structural_parse)
    rendered = json.dumps(output, ensure_ascii=False, indent=2)

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered + "\n", encoding="utf-8")
    else:
        print(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
