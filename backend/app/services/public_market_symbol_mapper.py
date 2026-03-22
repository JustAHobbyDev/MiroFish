"""
Deterministic public-market symbol mapping for bounded market handoff rows.
"""

from __future__ import annotations

import re
from typing import Any, Dict, Iterable, List, Tuple
from urllib.parse import parse_qs, urlparse


_EXCHANGE_NOTE_PATTERN = re.compile(
    r"\((?:NYSE|NASDAQ|Nasdaq|NYSE American|LSE|TSE|TYO)\s*:\s*([A-Z0-9.]+)\)"
)
_STOCK_CODE_PATTERN = re.compile(r"stock code\s+(\d{4,5})", re.IGNORECASE)
_SEC_FILENAME_SYMBOL_PATTERN = re.compile(r"/([a-z]{1,5})-\d{8}\.htm$", re.IGNORECASE)


def _coerce_string(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def _resolution_index(resolution_batches: Iterable[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    index: Dict[str, Dict[str, Any]] = {}
    for batch in resolution_batches:
        for row in batch.get("results", []):
            key = _coerce_string(row.get("canonical_entity_name"))
            if key:
                index[key] = row
    return index


def _collection_index(collection_batches: Iterable[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    index: Dict[str, Dict[str, Any]] = {}
    for batch in collection_batches:
        for row in batch.get("collections", []):
            key = _coerce_string(row.get("canonical_entity_name"))
            if key:
                index[key] = row
    return index


def _candidate_from_resolution_evidence(result: Dict[str, Any]) -> List[Tuple[str, str, Dict[str, Any]]]:
    candidates: List[Tuple[str, str, Dict[str, Any]]] = []
    for evidence in result.get("evidence", []):
        source_url = _coerce_string(evidence.get("source_url"))
        note = _coerce_string(evidence.get("note"))

        exchange_match = _EXCHANGE_NOTE_PATTERN.search(note)
        if exchange_match:
            candidates.append(
                (
                    exchange_match.group(1).upper(),
                    "official_company_or_ir_note",
                    {
                        "source_url": source_url,
                        "note": note,
                    },
                )
            )

        stock_code_match = _STOCK_CODE_PATTERN.search(note)
        if stock_code_match:
            candidates.append(
                (
                    stock_code_match.group(1),
                    "official_ir_stock_code_note",
                    {
                        "source_url": source_url,
                        "note": note,
                    },
                )
            )

        parsed = urlparse(source_url)
        query = parse_qs(parsed.query)
        cik_values = query.get("CIK", [])
        for cik in cik_values:
            cik_value = _coerce_string(cik).upper()
            if cik_value.isalpha() and 1 <= len(cik_value) <= 5:
                candidates.append(
                    (
                        cik_value,
                        "official_sec_lookup_url",
                        {
                            "source_url": source_url,
                            "note": note,
                        },
                    )
                )
    return candidates


def _candidate_from_collection_docs(collection: Dict[str, Any]) -> List[Tuple[str, str, Dict[str, Any]]]:
    candidates: List[Tuple[str, str, Dict[str, Any]]] = []
    for document in collection.get("collected_documents", []):
        source_url = _coerce_string(document.get("source_url"))
        match = _SEC_FILENAME_SYMBOL_PATTERN.search(source_url)
        if match:
            symbol = match.group(1).upper()
            candidates.append(
                (
                    symbol,
                    "official_filing_document_url",
                    {
                        "source_url": source_url,
                        "document_title": _coerce_string(document.get("document_title")),
                    },
                )
            )
    return candidates


def _mapping_status(symbol: str, result: Dict[str, Any]) -> str:
    live_resolution_status = _coerce_string(result.get("live_resolution_status"))
    if symbol and live_resolution_status == "resolved_direct_foreign_public_route" and symbol.isdigit():
        return "mapped_foreign_public_symbol"
    if symbol:
        return "mapped_public_symbol"
    if live_resolution_status == "resolved_direct_foreign_public_route":
        return "public_symbol_followup_required_foreign_route"
    return "public_symbol_followup_required"


def _exchange_scope(symbol: str, result: Dict[str, Any]) -> str:
    live_resolution_status = _coerce_string(result.get("live_resolution_status"))
    if symbol and live_resolution_status == "resolved_direct_foreign_public_route" and symbol.isdigit():
        return "foreign_home_market_code"
    if symbol:
        return "direct_public_market_symbol"
    if live_resolution_status == "resolved_direct_foreign_public_route":
        return "foreign_public_route_unmapped"
    return "public_route_unmapped"


def _mapping_action(status: str) -> str:
    if status in {"mapped_public_symbol", "mapped_foreign_public_symbol"}:
        return "build_market_research_row_from_mapped_public_symbol"
    return "resolve_primary_listing_or_market_symbol_before_market_research_row"


def build_public_market_symbol_mapping_batch(
    market_handoff_batch: Dict[str, Any],
    issuer_resolution_batches: List[Dict[str, Any]],
    filing_collection_batches: List[Dict[str, Any]],
) -> Dict[str, Any]:
    resolution_by_name = _resolution_index(issuer_resolution_batches)
    collection_by_name = _collection_index(filing_collection_batches)

    symbol_rows: List[Dict[str, Any]] = []

    for row in market_handoff_batch.get("handoff_rows", []):
        if _coerce_string(row.get("market_handoff_status")) != "public_investable_now":
            continue

        entity_name = _coerce_string(row.get("canonical_entity_name"))
        resolution_row = resolution_by_name.get(entity_name, {})
        collection_row = collection_by_name.get(entity_name, {})

        candidates = _candidate_from_resolution_evidence(resolution_row)
        if not candidates:
            candidates = _candidate_from_collection_docs(collection_row)

        mapped_symbol = ""
        mapping_basis = ""
        mapping_evidence: Dict[str, Any] = {}
        if candidates:
            mapped_symbol, mapping_basis, mapping_evidence = candidates[0]

        mapping_status = _mapping_status(mapped_symbol, resolution_row)

        symbol_rows.append(
            {
                "system_label": _coerce_string(row.get("system_label")),
                "canonical_entity_name": entity_name,
                "resolved_issuer_name": _coerce_string(row.get("resolved_issuer_name")),
                "market_handoff_status": _coerce_string(row.get("market_handoff_status")),
                "market_expression_scope": _coerce_string(row.get("market_expression_scope")),
                "route_aware_priority_score": int(row.get("route_aware_priority_score", 0)),
                "mapped_public_symbol": mapped_symbol,
                "symbol_mapping_status": mapping_status,
                "exchange_scope": _exchange_scope(mapped_symbol, resolution_row),
                "symbol_mapping_basis": mapping_basis,
                "symbol_mapping_evidence": mapping_evidence,
                "symbol_mapping_action": _mapping_action(mapping_status),
                "filing_route_assessment": _coerce_string(
                    resolution_row.get("filing_route_assessment") or row.get("route_assessment")
                ),
                "live_resolution_status": _coerce_string(resolution_row.get("live_resolution_status")),
            }
        )

    symbol_rows.sort(
        key=lambda item: (
            item["system_label"],
            0 if item["symbol_mapping_status"] == "mapped_public_symbol" else
            1 if item["symbol_mapping_status"] == "mapped_foreign_public_symbol" else 2,
            -item["route_aware_priority_score"],
            item["canonical_entity_name"],
        )
    )

    return {
        "name": "public_market_symbol_mapping_batch_v1",
        "symbol_rows": symbol_rows,
        "metrics": {
            "input_handoff_row_count": len(market_handoff_batch.get("handoff_rows", [])),
            "public_investable_input_count": len(symbol_rows),
            "mapped_public_symbol_count": len(
                [row for row in symbol_rows if row["symbol_mapping_status"] == "mapped_public_symbol"]
            ),
            "mapped_foreign_public_symbol_count": len(
                [row for row in symbol_rows if row["symbol_mapping_status"] == "mapped_foreign_public_symbol"]
            ),
            "followup_required_count": len(
                [
                    row
                    for row in symbol_rows
                    if row["symbol_mapping_status"]
                    in {"public_symbol_followup_required", "public_symbol_followup_required_foreign_route"}
                ]
            ),
        },
    }
