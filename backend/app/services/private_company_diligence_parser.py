"""
Deterministic parsing for collected private-company diligence documents.
"""

from __future__ import annotations

import hashlib
import html
import re
from pathlib import Path
from typing import Any, Dict, List


REPO_ROOT = Path(__file__).resolve().parents[3]


DEFAULT_KEYWORDS_BY_SYSTEM = {
    "utility and large-load power buildout": [
        "data center",
        "hyperscale",
        "power",
        "load",
        "capacity",
        "campus",
        "development",
        "grid",
        "transmission",
        "battery",
        "interconnection",
        "financing",
        "issuance",
        "abs",
        "megawatt",
    ],
    "data center backup-power equipment buildout": [
        "generator",
        "engine",
        "backup power",
        "data center",
        "capacity",
        "manufacturing",
        "expansion",
        "plant",
        "power",
        "enclosure",
    ],
}


def _coerce_string(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def _parse_batch_id(origin_name: str) -> str:
    digest = hashlib.sha1(origin_name.encode("utf-8")).hexdigest()[:8]
    return f"private_company_diligence_parse_batch_v1_{digest}"


def _document_parse_id(document_id: str) -> str:
    digest = hashlib.sha1(document_id.encode("utf-8")).hexdigest()[:8]
    return f"pcdp_{digest}"


def _keywords_for_system(system_label: str) -> List[str]:
    system_key = _coerce_string(system_label).lower()
    if system_key in DEFAULT_KEYWORDS_BY_SYSTEM:
        return list(DEFAULT_KEYWORDS_BY_SYSTEM[system_key])
    return ["capacity", "power", "development", "financing", "expansion"]


def _resolve_local_path(local_path_value: str) -> Path:
    local_path = Path(_coerce_string(local_path_value))
    if local_path.is_absolute():
        return local_path
    if local_path.exists():
        return local_path
    repo_root_candidate = REPO_ROOT / local_path
    if repo_root_candidate.exists():
        return repo_root_candidate
    return local_path


def _normalize_whitespace(text: str) -> str:
    return " ".join(text.split())


def _keyword_pattern(keyword: str) -> re.Pattern[str]:
    normalized = _coerce_string(keyword).lower()
    if " " in normalized:
        return re.compile(rf"\b{re.escape(normalized)}\b")
    if normalized.endswith("y") and len(normalized) > 2:
        return re.compile(rf"\b{re.escape(normalized[:-1])}(?:y|ies)\b")
    return re.compile(rf"\b{re.escape(normalized)}s?\b")


def _strip_html(text: str) -> str:
    text = re.sub(r"(?is)<script.*?>.*?</script>", " ", text)
    text = re.sub(r"(?is)<style.*?>.*?</style>", " ", text)
    text = re.sub(r"(?s)<[^>]+>", " ", text)
    return _normalize_whitespace(html.unescape(text))


def _snippet(text: str, start: int, keyword: str) -> str:
    radius = 180
    lo = max(0, start - radius)
    hi = min(len(text), start + len(keyword) + radius)
    return _normalize_whitespace(text[lo:hi])


def _extract_text_and_snippets(file_path: Path, keywords: List[str]) -> Dict[str, Any]:
    text = _strip_html(file_path.read_text(encoding="utf-8", errors="replace"))
    lowered = text.lower()
    keyword_counts = {keyword: 0 for keyword in keywords}
    evidence_snippets: List[Dict[str, Any]] = []

    for keyword in keywords:
        pattern = _keyword_pattern(keyword)
        matches = list(pattern.finditer(lowered))
        keyword_counts[keyword] = len(matches)
        for match in matches[:2]:
            evidence_snippets.append(
                {
                    "keyword": keyword,
                    "page_number": None,
                    "excerpt": _snippet(text, match.start(), keyword),
                }
            )

    return {
        "document_page_count": None,
        "keyword_counts": keyword_counts,
        "evidence_snippets": evidence_snippets,
    }


def parse_private_company_diligence_document(
    document: Dict[str, Any],
    system_label: str,
) -> Dict[str, Any]:
    local_path = _resolve_local_path(_coerce_string(document.get("local_path")))
    keywords = _keywords_for_system(system_label)
    suffix = local_path.suffix.lower()

    if not local_path.exists():
        return {
            "private_company_parse_document_id": _document_parse_id(
                _coerce_string(document.get("document_id"))
            ),
            "document_id": _coerce_string(document.get("document_id")),
            "parse_status": "local_file_missing",
            "local_path": str(local_path),
            "keywords": keywords,
            "keyword_counts": {},
            "evidence_snippets": [],
            "document_page_count": None,
        }

    if suffix not in {".html", ".htm"}:
        return {
            "private_company_parse_document_id": _document_parse_id(
                _coerce_string(document.get("document_id"))
            ),
            "document_id": _coerce_string(document.get("document_id")),
            "parse_status": "unsupported_file_type",
            "local_path": str(local_path),
            "keywords": keywords,
            "keyword_counts": {},
            "evidence_snippets": [],
            "document_page_count": None,
        }

    parsed = _extract_text_and_snippets(local_path, keywords)
    return {
        "private_company_parse_document_id": _document_parse_id(
            _coerce_string(document.get("document_id"))
        ),
        "document_id": _coerce_string(document.get("document_id")),
        "document_title": _coerce_string(document.get("document_title")),
        "document_type": _coerce_string(document.get("document_type")),
        "parse_status": "parsed",
        "local_path": str(local_path),
        "keywords": keywords,
        "keyword_counts": parsed["keyword_counts"],
        "evidence_snippets": parsed["evidence_snippets"],
        "document_page_count": parsed["document_page_count"],
    }


def build_private_company_diligence_parse_batch(
    collection_batch: Dict[str, Any],
) -> Dict[str, Any]:
    parsed_collections: List[Dict[str, Any]] = []
    parsed_document_count = 0

    for collection in collection_batch.get("collections", []):
        parsed_documents = [
            parse_private_company_diligence_document(
                document,
                _coerce_string(collection.get("system_label")),
            )
            for document in collection.get("collected_documents", [])
        ]
        parsed_document_count += len(
            [document for document in parsed_documents if document["parse_status"] == "parsed"]
        )
        parsed_collections.append(
            {
                "private_company_diligence_plan_id": _coerce_string(
                    collection.get("private_company_diligence_plan_id")
                ),
                "canonical_entity_name": _coerce_string(collection.get("canonical_entity_name")),
                "resolved_issuer_name": _coerce_string(collection.get("resolved_issuer_name")),
                "system_label": _coerce_string(collection.get("system_label")),
                "route_type": _coerce_string(collection.get("route_type")),
                "parsed_documents": parsed_documents,
            }
        )

    return {
        "name": _parse_batch_id(_coerce_string(collection_batch.get("name")) or "collection_batch"),
        "origin_collection_batch": _coerce_string(collection_batch.get("name")),
        "parsed_collections": parsed_collections,
        "metrics": {
            "input_collection_count": len(collection_batch.get("collections", [])),
            "parsed_collection_count": len(parsed_collections),
            "parsed_document_count": parsed_document_count,
        },
    }
