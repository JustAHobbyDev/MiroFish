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

full_name = "app.services.trade_press_archive"
spec = spec_from_file_location(full_name, SERVICES_ROOT / "trade_press_archive.py")
module = module_from_spec(spec)
sys.modules[full_name] = module
assert spec.loader is not None
spec.loader.exec_module(module)


def test_normalize_trade_press_artifact_maps_expected_fields():
    raw = {
        "source_url": "https://example.com/article/1",
        "publication": "Manufacturing Dive",
        "author": "A Reporter",
        "published_at": "2026-03-01T00:00:00Z",
        "headline": "Grid supplier breaks ground on new transformer factory",
        "section": "Operations",
        "tags": ["manufacturing", "capacity"],
        "body": "Body should be preserved but not used by the prefilter.",
    }

    artifact = module.normalize_trade_press_artifact(raw)

    assert artifact["source_class"] == "trade_press"
    assert artifact["publisher_or_author"] == "Manufacturing Dive"
    assert artifact["author_name"] == "A Reporter"
    assert artifact["title"] == "Grid supplier breaks ground on new transformer factory"
    assert artifact["category_tags"] == ["manufacturing", "capacity"]
    assert artifact["artifact_id"].startswith("trade_press_")


def test_build_trade_press_prefilter_batch_partitions_outputs():
    records = [
        {
            "source_url": "https://example.com/article/keep",
            "publication": "Data Center Dynamics",
            "published_at": "2026-03-01T00:00:00Z",
            "title": "Developer starts construction on AI data center campus with 500MW of power",
        },
        {
            "source_url": "https://example.com/article/review",
            "publication": "EE Times",
            "published_at": "2026-03-02T00:00:00Z",
            "title": "Networking vendors announce strategic partnership for optical AI clusters",
        },
        {
            "source_url": "https://example.com/article/drop",
            "publication": "IndustryWeek",
            "published_at": "2026-03-03T00:00:00Z",
            "title": "Why leaders are rethinking innovation culture",
        },
    ]

    payload = module.build_trade_press_prefilter_batch(records)

    assert payload["metrics"]["processed_artifact_count"] == 3
    assert payload["metrics"]["kept_count"] == 1
    assert payload["metrics"]["review_count"] == 1
    assert payload["metrics"]["dropped_count"] == 1
    assert len(payload["kept_artifacts"]) == 1
    assert len(payload["review_artifacts"]) == 1
    assert len(payload["dropped_audit_records"]) == 1


def test_build_trade_press_prefilter_batch_attaches_prefilter_provenance():
    records = [
        {
            "source_url": "https://example.com/article/keep",
            "publication": "Utility Dive",
            "published_at": "2026-03-01T00:00:00Z",
            "title": "Hitachi Energy expands transformer capacity with new U.S. plant",
        }
    ]

    payload = module.build_trade_press_prefilter_batch(records)
    artifact = payload["kept_artifacts"][0]

    assert artifact["_prefilter"]["triage"] == "keep"
    assert artifact["_prefilter"]["matched_families"]
