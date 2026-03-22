"""
Fetch and normalize retrospective historical web source packs.
"""

from __future__ import annotations

import hashlib
import json
import re
import urllib.request
from html import unescape
from typing import Any, Dict, Iterable, List, Optional

from .capital_flow_prefilter import (
    TRIAGE_DROP,
    TRIAGE_KEEP,
    TRIAGE_REVIEW,
    build_prefilter_audit_record,
    triage_capital_flow_artifact,
)

_FILING_KEEP_PATTERNS = (
    r"\badvanced packaging\b.*\b(expansion|facility|capacity|operations)\b",
    r"\bcapacity\b.*\b(expansion|increase|ramp|investment)\b",
    r"\b(ai|hbm|memory|packaging|photonics|indium phosphide|co-packaged optics|cpo)\b.*\b(demand|growth|expansion|investment|capacity)\b",
    r"\b(data center|ai)\b.*\b(connectivity|optics|photonics|memory|packaging)\b",
)

_FILING_REVIEW_PATTERNS = (
    r"\badvanced packaging\b",
    r"\bhbm\d*\b",
    r"\bcowos\b",
    r"\bphotonics\b",
    r"\bindium phosphide\b",
    r"\bsubstrate(?:s)?\b",
    r"\boptical\b",
)


_USER_AGENT = "Mozilla/5.0 (compatible; MiroFishHistoricalCorpus/1.0)"


def _coerce_string(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def _normalize_list(value: Any) -> List[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [_coerce_string(item) for item in value if _coerce_string(item)]
    text = _coerce_string(value)
    return [text] if text else []


def _strip_html(html: str) -> str:
    cleaned = re.sub(r"(?is)<script.*?>.*?</script>", " ", html)
    cleaned = re.sub(r"(?is)<style.*?>.*?</style>", " ", cleaned)
    cleaned = re.sub(r"(?is)<!--.*?-->", " ", cleaned)
    cleaned = re.sub(r"(?is)<[^>]+>", " ", cleaned)
    cleaned = unescape(cleaned)
    return re.sub(r"\s+", " ", cleaned).strip()


def _extract_meta_map(html: str) -> Dict[str, str]:
    meta_map: Dict[str, str] = {}
    for match in re.finditer(
        r"""(?is)<meta\b([^>]+?)>""",
        html,
    ):
        attrs = match.group(1)
        key_match = re.search(r"""(?:name|property|itemprop)\s*=\s*["']([^"']+)["']""", attrs, re.I)
        value_match = re.search(r"""content\s*=\s*["']([^"']+)["']""", attrs, re.I)
        if not key_match or not value_match:
            continue
        key = _coerce_string(key_match.group(1)).lower()
        value = _coerce_string(value_match.group(1))
        if key and value and key not in meta_map:
            meta_map[key] = value
    return meta_map


def _extract_title(html: str, meta_map: Dict[str, str], fallback: str) -> str:
    for key in ("og:title", "twitter:title", "title"):
        if meta_map.get(key):
            return meta_map[key]
    match = re.search(r"(?is)<title>(.*?)</title>", html)
    if match:
        return _strip_html(match.group(1))
    return fallback


def _extract_published_at(html: str, meta_map: Dict[str, str], fallback: str) -> str:
    for key in (
        "article:published_time",
        "parsely-pub-date",
        "publish-date",
        "publication_date",
        "pubdate",
        "date",
        "dc.date",
        "dc.date.issued",
    ):
        if meta_map.get(key):
            return meta_map[key]
    match = re.search(r"""(?is)<time\b[^>]*datetime=["']([^"']+)["']""", html)
    if match:
        return _coerce_string(match.group(1))
    return fallback


def _extract_body_text(html: str) -> str:
    jsonld_match = re.search(r'"articleBody"\s*:\s*"(.+?)"', html, re.I | re.S)
    if jsonld_match:
        body = jsonld_match.group(1)
        body = body.replace("\\n", " ").replace('\\"', '"')
        body = body.replace("\\/", "/")
        return re.sub(r"\s+", " ", unescape(body)).strip()

    for tag in ("article", "main", "body"):
        match = re.search(rf"(?is)<{tag}\b.*?>(.*?)</{tag}>", html)
        if match:
            text = _strip_html(match.group(1))
            if text:
                return text
    return _strip_html(html)


def fetch_historical_web_record(entry: Dict[str, Any]) -> Dict[str, Any]:
    source_url = _coerce_string(entry.get("source_url"))
    request = urllib.request.Request(source_url, headers={"User-Agent": _USER_AGENT})
    with urllib.request.urlopen(request, timeout=30) as response:
        html = response.read().decode("utf-8", errors="ignore")

    meta_map = _extract_meta_map(html)
    title = _extract_title(html, meta_map, _coerce_string(entry.get("title_hint")))
    published_at = _extract_published_at(html, meta_map, _coerce_string(entry.get("published_at")))
    body_text = _extract_body_text(html)

    return {
        "source_class": _coerce_string(entry.get("source_class")),
        "source_type": _coerce_string(entry.get("source_type")),
        "publisher_or_author": _coerce_string(entry.get("publisher_or_author")),
        "issuing_company_name": _coerce_string(entry.get("issuing_company_name")),
        "published_at": published_at,
        "title": title,
        "source_url": source_url,
        "body_text": body_text,
        "section_name": _coerce_string(entry.get("section_name")),
        "category_tags": _normalize_list(entry.get("category_tags")),
        "corpus_entry_id": _coerce_string(entry.get("corpus_entry_id")),
        "fetched_via": "historical_web_archive_v1",
    }


def _artifact_id(record: Dict[str, Any]) -> str:
    seed = "||".join(
        [
            _coerce_string(record.get("source_class")),
            _coerce_string(record.get("source_url")),
            _coerce_string(record.get("published_at")),
            _coerce_string(record.get("title")),
        ]
    )
    digest = hashlib.sha256(seed.encode("utf-8")).hexdigest()[:16]
    return f"historical_web_{digest}"


def normalize_historical_web_artifact(record: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "artifact_id": _artifact_id(record),
        "source_class": _coerce_string(record.get("source_class")),
        "publisher_or_author": _coerce_string(record.get("publisher_or_author")),
        "issuing_company_name": _coerce_string(record.get("issuing_company_name")),
        "published_at": _coerce_string(record.get("published_at")),
        "title": _coerce_string(record.get("title")),
        "headline": _coerce_string(record.get("title")),
        "subheadline": _coerce_string(record.get("subheadline")),
        "deck": _coerce_string(record.get("deck")),
        "section_name": _coerce_string(record.get("section_name")),
        "category_tags": _normalize_list(record.get("category_tags")),
        "source_url": _coerce_string(record.get("source_url")),
        "body_text": _coerce_string(record.get("body_text")),
        "artifact_metadata": {
            "source_type": _coerce_string(record.get("source_type")),
            "corpus_entry_id": _coerce_string(record.get("corpus_entry_id")),
            "fetched_via": _coerce_string(record.get("fetched_via")),
        },
    }


def build_historical_web_prefilter_batch(
    records: Iterable[Dict[str, Any]],
    *,
    batch_name: str = "historical_web_prefilter_batch_v1",
    filing_aware: bool = False,
) -> Dict[str, Any]:
    kept_artifacts: List[Dict[str, Any]] = []
    review_artifacts: List[Dict[str, Any]] = []
    dropped_audit_records: List[Dict[str, Any]] = []

    for raw_record in records:
        artifact = normalize_historical_web_artifact(raw_record)
        triage = triage_capital_flow_artifact(artifact)
        if filing_aware:
            triage = _apply_filing_aware_override(artifact, triage)
        artifact_with_triage = {**artifact, "_prefilter": triage}
        if triage["triage"] == TRIAGE_KEEP:
            kept_artifacts.append(artifact_with_triage)
        elif triage["triage"] == TRIAGE_REVIEW:
            review_artifacts.append(artifact_with_triage)
        elif triage["triage"] == TRIAGE_DROP:
            dropped_audit_records.append(build_prefilter_audit_record(artifact, triage))

    return {
        "name": batch_name,
        "source_class": "mixed_source",
        "source_classes": sorted(
            {
                _coerce_string(item.get("source_class"))
                for item in [*kept_artifacts, *review_artifacts]
                if _coerce_string(item.get("source_class"))
            }
        ),
        "processed_artifact_count": len(kept_artifacts) + len(review_artifacts) + len(dropped_audit_records),
        "kept_artifacts": kept_artifacts,
        "review_artifacts": review_artifacts,
        "dropped_audit_records": dropped_audit_records,
        "metrics": {
            "processed_artifact_count": len(kept_artifacts) + len(review_artifacts) + len(dropped_audit_records),
            "kept_count": len(kept_artifacts),
            "review_count": len(review_artifacts),
            "dropped_count": len(dropped_audit_records),
        },
    }


def load_manifest_entries(path: str) -> List[Dict[str, Any]]:
    data = json.loads(open(path, "r", encoding="utf-8").read())
    return list(data.get("entries", []))


def _apply_filing_aware_override(
    artifact: Dict[str, Any],
    triage: Dict[str, Any],
) -> Dict[str, Any]:
    if _coerce_string(artifact.get("source_class")) != "company_filing":
        return triage

    text = " ".join(
        [
            _coerce_string(artifact.get("title")),
            _coerce_string(artifact.get("body_text")),
            _coerce_string(artifact.get("section_name")),
            " ".join(_normalize_list(artifact.get("category_tags"))),
        ]
    ).lower()

    if any(re.search(pattern, text) for pattern in _FILING_KEEP_PATTERNS):
        return {
            **triage,
            "triage": TRIAGE_KEEP,
            "reason": "Historical filing-aware override matched capacity, investment, or demand language in a filing artifact.",
            "matched_families": sorted(set(triage.get("matched_families", [])) | {"historical_filing_keep"}),
            "fired_rules": list(triage.get("fired_rules", []))
            + ["historical_filing_keep"],
        }

    if triage.get("triage") == TRIAGE_DROP and any(re.search(pattern, text) for pattern in _FILING_REVIEW_PATTERNS):
        return {
            **triage,
            "triage": TRIAGE_REVIEW,
            "reason": "Historical filing-aware override matched strategic system language in a filing artifact.",
            "matched_families": sorted(set(triage.get("matched_families", [])) | {"historical_filing_review"}),
            "fired_rules": list(triage.get("fired_rules", []))
            + ["historical_filing_review"],
        }

    return triage
