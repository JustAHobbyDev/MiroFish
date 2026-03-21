"""
Deterministic local company-filing parsing for collected filing documents.
"""

from __future__ import annotations

import hashlib
import html
import re
from pathlib import Path
from typing import Any, Dict, List

REPO_ROOT = Path(__file__).resolve().parents[3]


DEFAULT_KEYWORDS_BY_SYSTEM = {
    "grid equipment and transformer buildout": [
        "transformer",
        "grid",
        "substation",
        "switchgear",
        "backlog",
        "capacity",
        "capex",
        "power",
        "shortage",
        "expansion",
        "manufacturing",
    ],
    "data center power demand buildout": [
        "data center",
        "hyperscale",
        "power",
        "substation",
        "transformer",
        "switchgear",
        "load",
        "capacity",
        "backlog",
        "expansion",
    ],
}


def _coerce_string(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def _parse_batch_id(origin_name: str) -> str:
    digest = hashlib.sha1(origin_name.encode("utf-8")).hexdigest()[:8]
    return f"company_filing_parse_batch_v1_{digest}"


def _document_parse_id(document_id: str) -> str:
    digest = hashlib.sha1(document_id.encode("utf-8")).hexdigest()[:8]
    return f"cfp_{digest}"


def _keywords_for_system(system_label: str) -> List[str]:
    system_key = _coerce_string(system_label).lower()
    if system_key in DEFAULT_KEYWORDS_BY_SYSTEM:
        return list(DEFAULT_KEYWORDS_BY_SYSTEM[system_key])
    return [
        "capacity",
        "capex",
        "backlog",
        "expansion",
        "manufacturing",
        "power",
    ]


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


def _strip_html(text: str) -> str:
    text = re.sub(r"(?is)<script.*?>.*?</script>", " ", text)
    text = re.sub(r"(?is)<style.*?>.*?</style>", " ", text)
    text = re.sub(r"(?s)<[^>]+>", " ", text)
    return _normalize_whitespace(html.unescape(text))


def _keyword_counts(text: str, keywords: List[str]) -> Dict[str, int]:
    lowered = text.lower()
    counts: Dict[str, int] = {}
    for keyword in keywords:
        pattern = re.compile(rf"\b{re.escape(keyword.lower())}\b")
        counts[keyword] = len(pattern.findall(lowered))
    return counts


def _snippet(text: str, start: int, keyword: str) -> str:
    radius = 180
    lo = max(0, start - radius)
    hi = min(len(text), start + len(keyword) + radius)
    return _normalize_whitespace(text[lo:hi])


def _extract_pdf_text_and_snippets(file_path: Path, keywords: List[str]) -> Dict[str, Any]:
    import fitz

    keyword_counts = {keyword: 0 for keyword in keywords}
    evidence_snippets: List[Dict[str, Any]] = []

    with fitz.open(file_path) as doc:
        for page_index, page in enumerate(doc):
            page_text = page.get_text()
            lowered = page_text.lower()
            for keyword in keywords:
                pattern = re.compile(rf"\b{re.escape(keyword.lower())}\b")
                matches = list(pattern.finditer(lowered))
                keyword_counts[keyword] += len(matches)
                if matches and len([s for s in evidence_snippets if s["keyword"] == keyword]) < 2:
                    evidence_snippets.append(
                        {
                            "keyword": keyword,
                            "page_number": page_index + 1,
                            "excerpt": _snippet(page_text, matches[0].start(), keyword),
                        }
                    )

        return {
            "document_page_count": doc.page_count,
            "keyword_counts": keyword_counts,
            "evidence_snippets": evidence_snippets,
        }


def _extract_html_text_and_snippets(file_path: Path, keywords: List[str]) -> Dict[str, Any]:
    text = _strip_html(file_path.read_text(encoding="utf-8", errors="replace"))
    lowered = text.lower()
    keyword_counts = _keyword_counts(text, keywords)
    evidence_snippets: List[Dict[str, Any]] = []
    for keyword in keywords:
        if keyword_counts[keyword] == 0:
            continue
        pattern = re.compile(rf"\b{re.escape(keyword.lower())}\b")
        matches = list(pattern.finditer(lowered))
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


def parse_company_filing_document(document: Dict[str, Any], system_label: str) -> Dict[str, Any]:
    local_path = _resolve_local_path(_coerce_string(document.get("local_path")))
    keywords = _keywords_for_system(system_label)
    suffix = local_path.suffix.lower()

    if not local_path.exists():
        return {
            "company_filing_parse_document_id": _document_parse_id(_coerce_string(document.get("document_id"))),
            "document_id": _coerce_string(document.get("document_id")),
            "parse_status": "local_file_missing",
            "local_path": str(local_path),
            "keywords": keywords,
            "keyword_counts": {},
            "evidence_snippets": [],
            "document_page_count": None,
        }

    if suffix == ".pdf":
        parsed = _extract_pdf_text_and_snippets(local_path, keywords)
    elif suffix in {".html", ".htm"}:
        parsed = _extract_html_text_and_snippets(local_path, keywords)
    else:
        return {
            "company_filing_parse_document_id": _document_parse_id(_coerce_string(document.get("document_id"))),
            "document_id": _coerce_string(document.get("document_id")),
            "parse_status": "unsupported_file_type",
            "local_path": str(local_path),
            "keywords": keywords,
            "keyword_counts": {},
            "evidence_snippets": [],
            "document_page_count": None,
        }

    return {
        "company_filing_parse_document_id": _document_parse_id(_coerce_string(document.get("document_id"))),
        "document_id": _coerce_string(document.get("document_id")),
        "document_title": _coerce_string(document.get("document_title")),
        "filing_type": _coerce_string(document.get("filing_type")),
        "parse_status": "parsed",
        "local_path": str(local_path),
        "keywords": keywords,
        "keyword_counts": parsed["keyword_counts"],
        "evidence_snippets": parsed["evidence_snippets"],
        "document_page_count": parsed["document_page_count"],
    }


def build_company_filing_parse_batch(collection_batch: Dict[str, Any]) -> Dict[str, Any]:
    parsed_collections: List[Dict[str, Any]] = []
    parsed_document_count = 0

    for collection in collection_batch.get("collections", []):
        parsed_documents = [
            parse_company_filing_document(document, _coerce_string(collection.get("system_label")))
            for document in collection.get("collected_documents", [])
        ]
        parsed_document_count += len([doc for doc in parsed_documents if doc["parse_status"] == "parsed"])
        parsed_collections.append(
            {
                "company_filing_collection_id": _coerce_string(collection.get("company_filing_collection_id")),
                "canonical_entity_name": _coerce_string(collection.get("canonical_entity_name")),
                "resolved_issuer_name": _coerce_string(collection.get("resolved_issuer_name")),
                "system_label": _coerce_string(collection.get("system_label")),
                "filing_route_assessment": _coerce_string(collection.get("filing_route_assessment")),
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
