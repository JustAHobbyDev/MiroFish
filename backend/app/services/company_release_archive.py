"""
Normalize and triage company-release archive artifacts for capital-flow discovery.

This module does not fetch live wire data. It operates on pre-collected release
records so the first archive path can be tested offline and integrated later
with a real collector.
"""

from __future__ import annotations

import hashlib
from typing import Any, Dict, Iterable, List

from .capital_flow_prefilter import (
    TRIAGE_DROP,
    TRIAGE_KEEP,
    TRIAGE_REVIEW,
    build_prefilter_audit_record,
    triage_capital_flow_artifact,
)


def _normalize_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, (list, tuple, set)):
        return " ".join(_normalize_text(item) for item in value if item is not None).strip()
    if isinstance(value, dict):
        return " ".join(
            _normalize_text(item) for item in value.values() if item is not None
        ).strip()
    return str(value).strip()


def _normalize_category_tags(value: Any) -> List[str]:
    if value is None:
        return []
    if isinstance(value, str):
        cleaned = value.strip()
        return [cleaned] if cleaned else []
    if isinstance(value, (list, tuple, set)):
        return [item for item in (_normalize_text(v) for v in value) if item]
    if isinstance(value, dict):
        return [item for item in (_normalize_text(v) for v in value.values()) if item]
    cleaned = _normalize_text(value)
    return [cleaned] if cleaned else []


def _choose_first(record: Dict[str, Any], *keys: str) -> Any:
    for key in keys:
        value = record.get(key)
        if value not in (None, "", [], {}):
            return value
    return None


def _build_artifact_id(
    *,
    source_url: str,
    published_at: str,
    title: str,
    publisher_or_author: str,
) -> str:
    seed = "||".join(
        [
            source_url.strip(),
            published_at.strip(),
            title.strip(),
            publisher_or_author.strip(),
        ]
    )
    digest = hashlib.sha256(seed.encode("utf-8")).hexdigest()[:16]
    return f"company_release_{digest}"


def normalize_company_release_artifact(record: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normalize a raw release record into the company-release artifact contract.
    """
    source_url = _normalize_text(
        _choose_first(record, "source_url", "canonical_url", "url", "release_url")
    )
    title = _normalize_text(_choose_first(record, "title", "headline"))
    publisher = _normalize_text(
        _choose_first(record, "publisher_or_author", "publisher", "wire_service", "source")
    )
    published_at = _normalize_text(
        _choose_first(record, "published_at", "published_date", "date")
    )
    artifact_id = _normalize_text(record.get("artifact_id")) or _build_artifact_id(
        source_url=source_url,
        published_at=published_at,
        title=title,
        publisher_or_author=publisher,
    )

    return {
        "artifact_id": artifact_id,
        "source_class": "company_release",
        "publisher_or_author": publisher,
        "issuing_company_name": _normalize_text(
            _choose_first(record, "issuing_company_name", "company_name", "issuer", "issuer_name")
        ),
        "published_at": published_at,
        "title": title,
        "headline": _normalize_text(record.get("headline")),
        "subheadline": _normalize_text(_choose_first(record, "subheadline", "summary", "deck")),
        "deck": _normalize_text(record.get("deck")),
        "section_name": _normalize_text(_choose_first(record, "section_name", "category")),
        "category_tags": _normalize_category_tags(
            _choose_first(record, "category_tags", "tags", "categories")
        ),
        "publisher_metadata": {
            "raw_category": _normalize_text(record.get("category")),
            "raw_source": _normalize_text(record.get("source")),
        },
        "source_url": source_url,
        "body_text": _normalize_text(_choose_first(record, "body_text", "body", "content")),
    }


def build_company_release_prefilter_batch(
    records: Iterable[Dict[str, Any]],
    *,
    batch_name: str = "company_release_prefilter_batch_v1",
) -> Dict[str, Any]:
    """
    Normalize records, apply deterministic triage, and partition outputs.
    """
    normalized_artifacts: List[Dict[str, Any]] = []
    kept_artifacts: List[Dict[str, Any]] = []
    review_artifacts: List[Dict[str, Any]] = []
    dropped_audit_records: List[Dict[str, Any]] = []

    for raw_record in records:
        artifact = normalize_company_release_artifact(raw_record)
        normalized_artifacts.append(artifact)
        triage_result = triage_capital_flow_artifact(artifact)

        if triage_result["triage"] == TRIAGE_KEEP:
            kept_artifacts.append(
                {
                    **artifact,
                    "_prefilter": triage_result,
                }
            )
            continue

        if triage_result["triage"] == TRIAGE_REVIEW:
            review_artifacts.append(
                {
                    **artifact,
                    "_prefilter": triage_result,
                }
            )
            continue

        dropped_audit_records.append(build_prefilter_audit_record(artifact, triage_result))

    processed_count = len(normalized_artifacts)
    metrics = {
        "processed_artifact_count": processed_count,
        "kept_count": len(kept_artifacts),
        "review_count": len(review_artifacts),
        "dropped_count": len(dropped_audit_records),
    }

    return {
        "name": batch_name,
        "source_class": "company_release",
        "processed_artifact_count": processed_count,
        "kept_artifacts": kept_artifacts,
        "review_artifacts": review_artifacts,
        "dropped_audit_records": dropped_audit_records,
        "metrics": metrics,
    }
