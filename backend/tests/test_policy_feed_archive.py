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

full_name = "app.services.policy_feed_archive"
spec = spec_from_file_location(full_name, SERVICES_ROOT / "policy_feed_archive.py")
module = module_from_spec(spec)
sys.modules[full_name] = module
assert spec.loader is not None
spec.loader.exec_module(module)


def _sample_document(title: str, summary: str) -> dict:
    return {
        "document_id": f"doc_{title.lower().replace(' ', '_')}",
        "source_target_id": "src_target_federal_register_notices",
        "source_target_name": "Federal Register Notices",
        "source_class": "government",
        "publisher": "Federal Register",
        "title": title,
        "canonical_url": "https://example.com/doc",
        "published_at": "2025-10-01",
        "summary": summary,
        "excerpt": summary,
        "notes": ["Normalized from live Federal Register API response."],
    }


def test_normalize_policy_feed_artifact_maps_expected_fields():
    artifact = module.normalize_policy_feed_artifact(
        _sample_document(
            "DOE awards grant for transformer plant expansion",
            "Award supports construction of a new manufacturing line.",
        )
    )

    assert artifact["source_class"] == "government"
    assert artifact["publisher_or_author"] == "Federal Register"
    assert artifact["title"] == "DOE awards grant for transformer plant expansion"
    assert artifact["body_text"]
    assert artifact["artifact_id"].startswith("policy_feed_")


def test_build_policy_feed_prefilter_batch_partitions_outputs():
    documents = [
        _sample_document(
            "DOE awards grant for transformer plant expansion",
            "Award supports construction of a new manufacturing line.",
        ),
        _sample_document(
            "Agency issues broad innovation strategy update",
            "Long-term competitiveness and innovation priorities were discussed.",
        ),
    ]

    payload = module.build_policy_feed_prefilter_batch(documents)

    assert payload["metrics"]["processed_artifact_count"] == 2
    assert payload["metrics"]["kept_count"] == 1
    assert payload["metrics"]["dropped_count"] == 1
