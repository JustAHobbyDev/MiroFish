from datetime import date

from app.services.archive_batch_window_filter import (
    artifact_ids_from_prefilter_batch,
    filter_prefilter_batch_by_window,
    filter_signal_batch_by_artifact_ids,
)


def test_filter_prefilter_batch_by_window_filters_all_sections():
    batch = {
        "name": "demo_prefilter",
        "source_class": "trade_press",
        "kept_artifacts": [
            {"artifact_id": "a", "published_at": "2025-09-05", "title": "A"},
            {"artifact_id": "b", "published_at": "2025-08-31", "title": "B"},
        ],
        "review_artifacts": [
            {"artifact_id": "c", "published_at": "2025-10-01", "title": "C"},
        ],
        "dropped_audit_records": [
            {"artifact_id": "d", "published_at": "2025-11-01", "title": "D"},
            {"artifact_id": "e", "published_at": "2026-03-01", "title": "E"},
        ],
    }

    filtered = filter_prefilter_batch_by_window(
        batch,
        start_date=date(2025, 9, 1),
        end_date=date(2026, 2, 28),
        name="filtered_prefilter",
    )

    assert filtered["name"] == "filtered_prefilter"
    assert [item["artifact_id"] for item in filtered["kept_artifacts"]] == ["a"]
    assert [item["artifact_id"] for item in filtered["review_artifacts"]] == ["c"]
    assert [item["artifact_id"] for item in filtered["dropped_audit_records"]] == ["d"]
    assert filtered["metrics"] == {
        "processed_artifact_count": 3,
        "kept_count": 1,
        "review_count": 1,
        "dropped_count": 1,
    }


def test_filter_signal_batch_by_artifact_ids_recomputes_metrics():
    prefilter_batch = {
        "kept_artifacts": [{"artifact_id": "a"}],
        "review_artifacts": [{"artifact_id": "c"}],
    }
    signal_batch = {
        "name": "demo_signal",
        "source_class": "mixed_source",
        "prompt_version": "v1",
        "model_name": "test-model",
        "processed_results": [
            {"artifact_id": "a", "produced_candidates": True, "candidates": [{"x": 1}], "prefilter_triage": "keep"},
            {"artifact_id": "b", "produced_candidates": False, "candidates": [], "prefilter_triage": "keep"},
            {"artifact_id": "c", "produced_candidates": True, "candidates": [{"x": 1}, {"x": 2}], "prefilter_triage": "review"},
        ],
        "schema_failures": [
            {"artifact_id": "d", "prefilter_triage": "review"},
        ],
        "extraction_failures": [
            {"artifact_id": "e", "prefilter_triage": "keep"},
        ],
    }

    filtered = filter_signal_batch_by_artifact_ids(
        signal_batch,
        allowed_artifact_ids=artifact_ids_from_prefilter_batch(prefilter_batch),
        name="filtered_signal",
    )

    assert filtered["name"] == "filtered_signal"
    assert [item["artifact_id"] for item in filtered["processed_results"]] == ["a", "c"]
    assert filtered["schema_failures"] == []
    assert filtered["extraction_failures"] == []
    assert filtered["metrics"] == {
        "artifacts_sent_to_llm": 2,
        "successful_extractions": 2,
        "schema_failure_count": 0,
        "extraction_failure_count": 0,
        "produced_candidate_artifact_count": 2,
        "no_candidate_artifact_count": 0,
        "total_candidate_count": 3,
        "review_artifact_count": 1,
        "review_candidate_artifact_count": 1,
    }
