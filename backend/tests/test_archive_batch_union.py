import sys
import types
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path


APP_ROOT = Path(__file__).resolve().parents[1] / "app"
SERVICES_ROOT = APP_ROOT / "services"

app_pkg = types.ModuleType("app")
app_pkg.__path__ = [str(APP_ROOT)]
services_pkg = types.ModuleType("app.services")
services_pkg.__path__ = [str(SERVICES_ROOT)]
sys.modules["app"] = app_pkg
sys.modules["app.services"] = services_pkg

full_name = "app.services.archive_batch_union"
spec = spec_from_file_location(full_name, SERVICES_ROOT / "archive_batch_union.py")
module = module_from_spec(spec)
sys.modules[full_name] = module
assert spec.loader is not None
spec.loader.exec_module(module)


def test_union_prefilter_batches_combines_source_classes_and_metrics():
    result = module.union_prefilter_batches(
        [
            {
                "kept_artifacts": [{"artifact_id": "a1", "source_class": "trade_press"}],
                "review_artifacts": [{"artifact_id": "a2", "source_class": "trade_press"}],
                "dropped_audit_records": [{"artifact_id": "a3"}],
            },
            {
                "kept_artifacts": [{"artifact_id": "b1", "source_class": "company_release"}],
                "review_artifacts": [],
                "dropped_audit_records": [],
            },
        ],
        name="mixed_prefilter",
    )

    assert result["source_class"] == "mixed_source"
    assert result["source_classes"] == ["company_release", "trade_press"]
    assert result["metrics"]["processed_artifact_count"] == 4
    assert result["metrics"]["kept_count"] == 2
    assert result["metrics"]["review_count"] == 1
    assert result["metrics"]["dropped_count"] == 1


def test_union_signal_batches_combines_results_and_metrics():
    result = module.union_signal_batches(
        [
            {
                "prompt_version": "v1",
                "model_name": "gpt-4o-mini",
                "processed_results": [{"artifact_id": "a1", "source_class": "trade_press"}],
                "schema_failures": [{"artifact_id": "a2", "source_class": "trade_press"}],
                "extraction_failures": [],
                "metrics": {
                    "artifacts_sent_to_llm": 2,
                    "successful_extractions": 1,
                    "schema_failure_count": 1,
                    "extraction_failure_count": 0,
                    "produced_candidate_artifact_count": 1,
                    "no_candidate_artifact_count": 0,
                    "total_candidate_count": 2,
                    "review_artifact_count": 1,
                    "review_candidate_artifact_count": 1,
                },
            },
            {
                "prompt_version": "v1",
                "model_name": "gpt-4o-mini",
                "processed_results": [{"artifact_id": "b1", "source_class": "company_release"}],
                "schema_failures": [],
                "extraction_failures": [{"artifact_id": "b2", "source_class": "company_release"}],
                "metrics": {
                    "artifacts_sent_to_llm": 2,
                    "successful_extractions": 1,
                    "schema_failure_count": 0,
                    "extraction_failure_count": 1,
                    "produced_candidate_artifact_count": 1,
                    "no_candidate_artifact_count": 0,
                    "total_candidate_count": 3,
                    "review_artifact_count": 0,
                    "review_candidate_artifact_count": 0,
                },
            },
        ],
        name="mixed_signal",
    )

    assert result["source_class"] == "mixed_source"
    assert result["source_classes"] == ["company_release", "trade_press"]
    assert result["prompt_version"] == "v1"
    assert result["model_name"] == "gpt-4o-mini"
    assert result["metrics"]["artifacts_sent_to_llm"] == 4
    assert result["metrics"]["successful_extractions"] == 2
    assert result["metrics"]["schema_failure_count"] == 1
    assert result["metrics"]["extraction_failure_count"] == 1


def test_union_prefilter_batches_rejects_duplicate_artifact_ids():
    try:
        module.union_prefilter_batches(
            [
                {"kept_artifacts": [{"artifact_id": "dup", "source_class": "trade_press"}], "review_artifacts": [], "dropped_audit_records": []},
                {"kept_artifacts": [{"artifact_id": "dup", "source_class": "company_release"}], "review_artifacts": [], "dropped_audit_records": []},
            ],
            name="mixed_prefilter",
        )
    except ValueError as exc:
        assert "duplicate artifact_id" in str(exc)
    else:
        raise AssertionError("expected duplicate artifact_id check to fail")
