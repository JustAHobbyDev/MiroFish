"""
Normalize policy-feed documents into capital-flow extraction artifacts.
"""

from __future__ import annotations

import hashlib
from typing import Any, Dict, Iterable, List

from .capital_flow_prefilter import (
    TRIAGE_KEEP,
    TRIAGE_REVIEW,
    build_prefilter_audit_record,
    triage_capital_flow_artifact,
)


def _coerce_string(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def _normalize_list(value: Any) -> List[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def _artifact_id(document: Dict[str, Any]) -> str:
    document_id = _coerce_string(document.get("document_id"))
    canonical_url = _coerce_string(document.get("canonical_url"))
    title = _coerce_string(document.get("title"))
    seed = "||".join(part for part in [document_id, canonical_url, title] if part)
    digest = hashlib.sha256(seed.encode("utf-8")).hexdigest()[:16]
    return f"policy_feed_{digest}"


def normalize_policy_feed_artifact(document: Dict[str, Any]) -> Dict[str, Any]:
    title = _coerce_string(document.get("title"))
    summary = _coerce_string(document.get("summary"))
    excerpt = _coerce_string(document.get("excerpt"))
    notes = [item for item in (_coerce_string(value) for value in _normalize_list(document.get("notes"))) if item]
    body_parts = [part for part in [summary, excerpt, *notes] if part]

    return {
        "artifact_id": _artifact_id(document),
        "source_class": _coerce_string(document.get("source_class")) or "government",
        "publisher_or_author": _coerce_string(document.get("publisher")) or _coerce_string(document.get("source_target_name")),
        "published_at": _coerce_string(document.get("published_at")),
        "title": title,
        "source_url": _coerce_string(document.get("canonical_url")),
        "body_text": "\n\n".join(body_parts),
        "artifact_metadata": {
            "document_id": _coerce_string(document.get("document_id")),
            "source_target_id": _coerce_string(document.get("source_target_id")),
            "source_target_name": _coerce_string(document.get("source_target_name")),
        },
    }


def build_policy_feed_prefilter_batch(
    documents: Iterable[Dict[str, Any]],
    *,
    batch_name: str = "policy_feed_prefilter_batch_v1",
) -> Dict[str, Any]:
    kept_artifacts: List[Dict[str, Any]] = []
    review_artifacts: List[Dict[str, Any]] = []
    dropped_audit_records: List[Dict[str, Any]] = []

    for raw_document in documents:
        artifact = normalize_policy_feed_artifact(raw_document)
        triage = triage_capital_flow_artifact(artifact)
        artifact_with_triage = {
            **artifact,
            "_prefilter": triage,
        }

        if triage["triage"] == TRIAGE_KEEP:
            kept_artifacts.append(artifact_with_triage)
        elif triage["triage"] == TRIAGE_REVIEW:
            review_artifacts.append(artifact_with_triage)
        else:
            dropped_audit_records.append(build_prefilter_audit_record(artifact, triage))

    return {
        "name": batch_name,
        "source_class": "policy_feed",
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
