import json
import sys
import types
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path


SERVICES_ROOT = Path(__file__).resolve().parents[1] / "app" / "services"

app_pkg = types.ModuleType("app")
app_pkg.__path__ = []
services_pkg = types.ModuleType("app.services")
services_pkg.__path__ = [str(SERVICES_ROOT)]
sys.modules["app"] = app_pkg
sys.modules["app.services"] = services_pkg

prefilter_full_name = "app.services.capital_flow_prefilter"
prefilter_spec = spec_from_file_location(prefilter_full_name, SERVICES_ROOT / "capital_flow_prefilter.py")
prefilter_module = module_from_spec(prefilter_spec)
sys.modules[prefilter_full_name] = prefilter_module
assert prefilter_spec.loader is not None
prefilter_spec.loader.exec_module(prefilter_module)

full_name = "app.services.company_release_archive"
spec = spec_from_file_location(full_name, SERVICES_ROOT / "company_release_archive.py")
module = module_from_spec(spec)
sys.modules[full_name] = module
assert spec.loader is not None
spec.loader.exec_module(module)


def test_normalize_company_release_artifact_maps_expected_fields():
    raw = {
        "source_url": "https://example.com/release/1",
        "publisher": "Business Wire",
        "issuer_name": "Example Co",
        "published_at": "2026-01-10T00:00:00Z",
        "headline": "Example Co breaks ground on new manufacturing line",
        "categories": ["Manufacturing", "Expansion"],
        "body": "Body should be preserved but not used by the prefilter.",
    }

    artifact = module.normalize_company_release_artifact(raw)

    assert artifact["source_class"] == "company_release"
    assert artifact["publisher_or_author"] == "Business Wire"
    assert artifact["issuing_company_name"] == "Example Co"
    assert artifact["title"] == "Example Co breaks ground on new manufacturing line"
    assert artifact["category_tags"] == ["Manufacturing", "Expansion"]
    assert artifact["artifact_id"].startswith("company_release_")


def test_build_company_release_prefilter_batch_partitions_outputs():
    records = [
        {
            "source_url": "https://example.com/release/keep",
            "publisher": "Business Wire",
            "issuer_name": "Factory Co",
            "published_at": "2026-01-10T00:00:00Z",
            "title": "Factory Co wins contract and starts construction on new production line",
        },
        {
            "source_url": "https://example.com/release/review",
            "publisher": "PR Newswire",
            "issuer_name": "Network Co",
            "published_at": "2026-01-11T00:00:00Z",
            "title": "Network Co announces strategic partnership for next-generation networking",
        },
        {
            "source_url": "https://example.com/release/drop",
            "publisher": "GlobeNewswire",
            "issuer_name": "Brand Co",
            "published_at": "2026-01-12T00:00:00Z",
            "title": "Brand Co launches innovation initiative for growth",
        },
    ]

    payload = module.build_company_release_prefilter_batch(records)

    assert payload["metrics"]["processed_artifact_count"] == 3
    assert payload["metrics"]["kept_count"] == 1
    assert payload["metrics"]["review_count"] == 1
    assert payload["metrics"]["dropped_count"] == 1
    assert len(payload["kept_artifacts"]) == 1
    assert len(payload["review_artifacts"]) == 1
    assert len(payload["dropped_audit_records"]) == 1
    assert payload["dropped_audit_records"][0]["triage"] == "drop"


def test_build_company_release_prefilter_batch_attaches_prefilter_provenance():
    records = [
        {
            "source_url": "https://example.com/release/keep",
            "publisher": "Business Wire",
            "issuer_name": "Factory Co",
            "published_at": "2026-01-10T00:00:00Z",
            "title": "Factory Co breaks ground on new battery materials plant",
        }
    ]

    payload = module.build_company_release_prefilter_batch(records)
    artifact = payload["kept_artifacts"][0]

    assert artifact["_prefilter"]["triage"] == "keep"
    assert artifact["_prefilter"]["matched_families"]
