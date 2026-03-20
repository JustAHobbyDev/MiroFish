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

full_name = "app.services.capital_flow_prefilter"
spec = spec_from_file_location(full_name, SERVICES_ROOT / "capital_flow_prefilter.py")
module = module_from_spec(spec)
sys.modules[full_name] = module
assert spec.loader is not None
spec.loader.exec_module(module)


def test_keep_on_strong_field_capacity_expansion():
    artifact = {
        "artifact_id": "art_1",
        "source_class": "company_release",
        "title": "Company breaks ground on new battery materials plant",
        "published_at": "2026-01-10T00:00:00Z",
    }

    result = module.triage_capital_flow_artifact(artifact)

    assert result["triage"] == module.TRIAGE_KEEP
    assert "construction_and_deployment" in result["matched_families"]
    assert "facility_and_capacity_expansion" in result["matched_families"]


def test_review_when_only_partnership_language_is_present():
    artifact = {
        "artifact_id": "art_2",
        "source_class": "trade_press",
        "headline": "Company Y and Company Z announce strategic partnership for next-generation networking",
        "section_name": "Networking",
    }

    result = module.triage_capital_flow_artifact(artifact)

    assert result["triage"] == module.TRIAGE_REVIEW
    assert result["matched_families"] == ["partnerships_with_buildout_implications"]


def test_drop_when_only_generic_narrative_language_exists():
    artifact = {
        "artifact_id": "art_3",
        "source_class": "trade_press",
        "title": "Company Q launches AI innovation initiative for growth",
    }

    result = module.triage_capital_flow_artifact(artifact)

    assert result["triage"] == module.TRIAGE_DROP
    assert result["matched_families"] == []
    assert result["excluded_generic_hits"]


def test_keep_on_multiple_family_hits_even_without_strong_field_primary_family():
    artifact = {
        "artifact_id": "art_4",
        "source_class": "company_release",
        "headline": "Company wins contract and starts construction on new production line",
    }

    result = module.triage_capital_flow_artifact(artifact)

    assert result["triage"] == module.TRIAGE_KEEP
    assert "contracts_and_orders" in result["matched_families"]
    assert "construction_and_deployment" in result["matched_families"]


def test_body_text_is_not_used_by_prefilter():
    artifact = {
        "artifact_id": "art_5",
        "source_class": "company_release",
        "title": "Quarterly corporate update",
        "body_text": "The company was awarded a major contract and is building a new fab.",
    }

    result = module.triage_capital_flow_artifact(artifact)

    assert result["triage"] == module.TRIAGE_DROP
    assert result["matched_families"] == []


def test_audit_record_contains_drop_provenance():
    artifact = {
        "artifact_id": "art_6",
        "source_class": "company_release",
        "publisher_or_author": "Business Wire",
        "published_at": "2026-01-10T00:00:00Z",
        "title": "Brand refresh announced",
    }
    triage_result = module.triage_capital_flow_artifact(artifact)

    audit = module.build_prefilter_audit_record(artifact, triage_result)

    assert audit["artifact_id"] == "art_6"
    assert audit["triage"] == module.TRIAGE_DROP
    assert audit["fired_rules"] == []
    assert "title" in audit
