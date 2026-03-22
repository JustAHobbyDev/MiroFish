"""
Deterministic date-window filtering for archive prefilter and signal batches.
"""

from __future__ import annotations

from datetime import date
from typing import Any, Dict, Iterable, List, Optional, Set


def _coerce_string(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def _parse_date(value: Any) -> Optional[date]:
    text = _coerce_string(value)
    if not text:
        return None
    try:
        return date.fromisoformat(text[:10])
    except ValueError:
        return None


def _in_window(item: Dict[str, Any], start_date: date, end_date: date) -> bool:
    published = _parse_date(item.get("published_at"))
    if published is None:
        return False
    return start_date <= published <= end_date


def filter_prefilter_batch_by_window(
    batch: Dict[str, Any],
    *,
    start_date: date,
    end_date: date,
    name: Optional[str] = None,
) -> Dict[str, Any]:
    kept_artifacts = [item for item in batch.get("kept_artifacts", []) if _in_window(item, start_date, end_date)]
    review_artifacts = [item for item in batch.get("review_artifacts", []) if _in_window(item, start_date, end_date)]
    dropped_audit_records = [
        item for item in batch.get("dropped_audit_records", []) if _in_window(item, start_date, end_date)
    ]
    return {
        "name": name or _coerce_string(batch.get("name")),
        "source_class": batch.get("source_class"),
        "source_classes": batch.get("source_classes"),
        "kept_artifacts": kept_artifacts,
        "review_artifacts": review_artifacts,
        "dropped_audit_records": dropped_audit_records,
        "metrics": {
            "processed_artifact_count": len(kept_artifacts) + len(review_artifacts) + len(dropped_audit_records),
            "kept_count": len(kept_artifacts),
            "review_count": len(review_artifacts),
            "dropped_count": len(dropped_audit_records),
        },
        "window_filter": {
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
        },
    }


def artifact_ids_from_prefilter_batch(prefilter_batch: Dict[str, Any]) -> Set[str]:
    return {
        _coerce_string(item.get("artifact_id"))
        for key in ("kept_artifacts", "review_artifacts")
        for item in prefilter_batch.get(key, [])
        if _coerce_string(item.get("artifact_id"))
    }


def _count_review_candidates(rows: Iterable[Dict[str, Any]]) -> int:
    return sum(
        1
        for row in rows
        if _coerce_string(row.get("prefilter_triage")) == "review" and bool(row.get("produced_candidates"))
    )


def filter_signal_batch_by_artifact_ids(
    batch: Dict[str, Any],
    *,
    allowed_artifact_ids: Set[str],
    name: Optional[str] = None,
) -> Dict[str, Any]:
    processed_results = [
        item
        for item in batch.get("processed_results", [])
        if _coerce_string(item.get("artifact_id")) in allowed_artifact_ids
    ]
    schema_failures = [
        item
        for item in batch.get("schema_failures", [])
        if _coerce_string(item.get("artifact_id")) in allowed_artifact_ids
    ]
    extraction_failures = [
        item
        for item in batch.get("extraction_failures", [])
        if _coerce_string(item.get("artifact_id")) in allowed_artifact_ids
    ]

    artifacts_sent_to_llm = len(processed_results) + len(schema_failures) + len(extraction_failures)
    successful_extractions = len(processed_results)
    produced_candidate_artifact_count = sum(1 for row in processed_results if bool(row.get("produced_candidates")))
    no_candidate_artifact_count = successful_extractions - produced_candidate_artifact_count
    total_candidate_count = sum(len(row.get("candidates", [])) for row in processed_results)
    review_artifact_count = sum(
        1
        for row in [*processed_results, *schema_failures, *extraction_failures]
        if _coerce_string(row.get("prefilter_triage")) == "review"
    )

    return {
        "name": name or _coerce_string(batch.get("name")),
        "source_class": batch.get("source_class"),
        "source_classes": batch.get("source_classes"),
        "prompt_version": batch.get("prompt_version"),
        "model_name": batch.get("model_name"),
        "processed_results": processed_results,
        "schema_failures": schema_failures,
        "extraction_failures": extraction_failures,
        "metrics": {
            "artifacts_sent_to_llm": artifacts_sent_to_llm,
            "successful_extractions": successful_extractions,
            "schema_failure_count": len(schema_failures),
            "extraction_failure_count": len(extraction_failures),
            "produced_candidate_artifact_count": produced_candidate_artifact_count,
            "no_candidate_artifact_count": no_candidate_artifact_count,
            "total_candidate_count": total_candidate_count,
            "review_artifact_count": review_artifact_count,
            "review_candidate_artifact_count": _count_review_candidates(processed_results),
        },
        "artifact_window_filter_count": len(allowed_artifact_ids),
    }
