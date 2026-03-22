"""
Deterministic company-filing evidence extraction from parsed filing batches.
"""

from __future__ import annotations

import hashlib
import re
from typing import Any, Dict, List


COMPONENT_KEYWORDS = {"transformer", "switchgear", "substation"}
PRESSURE_KEYWORDS = {"backlog", "shortage", "capacity"}
EXPANSION_KEYWORDS = {"manufacturing", "expansion", "capex"}
SYSTEM_KEYWORDS = {"power", "grid", "load", "hyperscale", "data center"}


def _coerce_string(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def _evidence_id(
    issuer_name: str,
    document_id: str,
    keyword: str,
    page_number: Any,
    index: int,
) -> str:
    basis = f"{issuer_name}|{document_id}|{keyword}|{page_number}|{index}"
    digest = hashlib.sha1(basis.encode("utf-8")).hexdigest()[:10]
    return f"cfe_{digest}"


def _keyword_family(keyword: str) -> str:
    normalized = _coerce_string(keyword).lower()
    if normalized in COMPONENT_KEYWORDS:
        return "component_specific"
    if normalized in PRESSURE_KEYWORDS:
        return "pressure_or_capacity"
    if normalized in EXPANSION_KEYWORDS:
        return "expansion_or_capex"
    if normalized in SYSTEM_KEYWORDS:
        return "system_context"
    return "other"


def _strength(keyword: str, excerpt: str) -> str:
    normalized = _coerce_string(keyword).lower()
    lowered_excerpt = _coerce_string(excerpt).lower()
    if normalized in COMPONENT_KEYWORDS | PRESSURE_KEYWORDS | EXPANSION_KEYWORDS:
        return "high"
    if normalized in SYSTEM_KEYWORDS:
        if re.search(r"\b(expan|capacity|backlog|shortage|manufacturing|transformer|switchgear)\b", lowered_excerpt):
            return "medium"
        return "low"
    return "low"


def _collection_summary(evidence_items: List[Dict[str, Any]]) -> Dict[str, Any]:
    by_family = {
        "component_specific": 0,
        "pressure_or_capacity": 0,
        "expansion_or_capex": 0,
        "system_context": 0,
        "other": 0,
    }
    for item in evidence_items:
        by_family[item["keyword_family"]] = by_family.get(item["keyword_family"], 0) + 1

    strong_count = len([item for item in evidence_items if item["evidence_strength"] in {"high", "medium"}])
    return {
        "evidence_item_count": len(evidence_items),
        "strong_evidence_item_count": strong_count,
        "family_counts": by_family,
    }


def build_company_filing_evidence_batch(parsed_batch: Dict[str, Any]) -> Dict[str, Any]:
    evidence_collections: List[Dict[str, Any]] = []
    total_evidence_count = 0

    for parsed_collection in parsed_batch.get("parsed_collections", []):
        evidence_items: List[Dict[str, Any]] = []
        for parsed_document in parsed_collection.get("parsed_documents", []):
            if _coerce_string(parsed_document.get("parse_status")) != "parsed":
                continue
            for index, snippet in enumerate(parsed_document.get("evidence_snippets", [])):
                keyword = _coerce_string(snippet.get("keyword"))
                excerpt = _coerce_string(snippet.get("excerpt"))
                page_number = snippet.get("page_number")
                evidence_items.append(
                    {
                        "company_filing_evidence_id": _evidence_id(
                            _coerce_string(parsed_collection.get("resolved_issuer_name")),
                            _coerce_string(parsed_document.get("document_id")),
                            keyword,
                            page_number,
                            index,
                        ),
                        "resolved_issuer_name": _coerce_string(parsed_collection.get("resolved_issuer_name")),
                        "canonical_entity_name": _coerce_string(parsed_collection.get("canonical_entity_name")),
                        "system_label": _coerce_string(parsed_collection.get("system_label")),
                        "document_id": _coerce_string(parsed_document.get("document_id")),
                        "document_title": _coerce_string(parsed_document.get("document_title")),
                        "filing_type": _coerce_string(parsed_document.get("filing_type")),
                        "keyword": keyword,
                        "keyword_family": _keyword_family(keyword),
                        "evidence_strength": _strength(keyword, excerpt),
                        "page_number": page_number,
                        "excerpt": excerpt,
                    }
                )

        evidence_items.sort(
            key=lambda item: (
                {"high": 0, "medium": 1, "low": 2}.get(item["evidence_strength"], 3),
                {"component_specific": 0, "pressure_or_capacity": 1, "expansion_or_capex": 2, "system_context": 3}.get(
                    item["keyword_family"], 4
                ),
                item["document_title"],
            )
        )
        total_evidence_count += len(evidence_items)
        evidence_collections.append(
            {
                "resolved_issuer_name": _coerce_string(parsed_collection.get("resolved_issuer_name")),
                "canonical_entity_name": _coerce_string(parsed_collection.get("canonical_entity_name")),
                "system_label": _coerce_string(parsed_collection.get("system_label")),
                "filing_route_assessment": _coerce_string(parsed_collection.get("filing_route_assessment")),
                "evidence_items": evidence_items,
                "summary": _collection_summary(evidence_items),
            }
        )

    return {
        "name": "company_filing_evidence_batch_v1",
        "origin_parse_batch": _coerce_string(parsed_batch.get("name")),
        "evidence_collections": evidence_collections,
        "metrics": {
            "input_parsed_collection_count": len(parsed_batch.get("parsed_collections", [])),
            "evidence_collection_count": len(evidence_collections),
            "total_evidence_item_count": total_evidence_count,
        },
    }
