"""
Deterministic union helpers for archive prefilter and signal batches.
"""

from __future__ import annotations

from typing import Any, Dict, Iterable, List


def _coerce_string(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def _require_unique_artifact_ids(items: Iterable[Dict[str, Any]], label: str) -> None:
    seen: set[str] = set()
    duplicates: set[str] = set()
    for item in items:
        artifact_id = _coerce_string(item.get("artifact_id"))
        if not artifact_id:
            continue
        if artifact_id in seen:
            duplicates.add(artifact_id)
        seen.add(artifact_id)
    if duplicates:
        joined = ", ".join(sorted(duplicates))
        raise ValueError(f"duplicate artifact_id values found in {label}: {joined}")


def union_prefilter_batches(
    batches: List[Dict[str, Any]],
    *,
    name: str,
) -> Dict[str, Any]:
    kept_artifacts = [artifact for batch in batches for artifact in batch.get("kept_artifacts", [])]
    review_artifacts = [artifact for batch in batches for artifact in batch.get("review_artifacts", [])]
    dropped_audit_records = [record for batch in batches for record in batch.get("dropped_audit_records", [])]

    _require_unique_artifact_ids(kept_artifacts + review_artifacts, "prefilter union")

    return {
        "name": name,
        "source_class": "mixed_source",
        "source_classes": sorted(
            {
                _coerce_string(artifact.get("source_class"))
                for artifact in kept_artifacts + review_artifacts
                if _coerce_string(artifact.get("source_class"))
            }
        ),
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


def union_signal_batches(
    batches: List[Dict[str, Any]],
    *,
    name: str,
) -> Dict[str, Any]:
    processed_results = [result for batch in batches for result in batch.get("processed_results", [])]
    schema_failures = [failure for batch in batches for failure in batch.get("schema_failures", [])]
    extraction_failures = [failure for batch in batches for failure in batch.get("extraction_failures", [])]

    _require_unique_artifact_ids(processed_results + schema_failures + extraction_failures, "signal union")

    metric_keys = (
        "artifacts_sent_to_llm",
        "successful_extractions",
        "schema_failure_count",
        "extraction_failure_count",
        "produced_candidate_artifact_count",
        "no_candidate_artifact_count",
        "total_candidate_count",
        "review_artifact_count",
        "review_candidate_artifact_count",
    )
    combined_metrics = {
        key: sum(int(batch.get("metrics", {}).get(key, 0)) for batch in batches)
        for key in metric_keys
    }

    prompt_versions = sorted(
        {
            _coerce_string(batch.get("prompt_version"))
            for batch in batches
            if _coerce_string(batch.get("prompt_version"))
        }
    )
    model_names = sorted(
        {
            _coerce_string(batch.get("model_name"))
            for batch in batches
            if _coerce_string(batch.get("model_name"))
        }
    )

    return {
        "name": name,
        "source_class": "mixed_source",
        "source_classes": sorted(
            {
                _coerce_string(result.get("source_class"))
                for result in processed_results
                if _coerce_string(result.get("source_class"))
            }
        ),
        "prompt_version": prompt_versions[0] if len(prompt_versions) == 1 else "mixed",
        "model_name": model_names[0] if len(model_names) == 1 else "mixed",
        "processed_results": processed_results,
        "schema_failures": schema_failures,
        "extraction_failures": extraction_failures,
        "metrics": combined_metrics,
    }
