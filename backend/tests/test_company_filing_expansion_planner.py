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

full_name = "app.services.company_filing_expansion_planner"
spec = spec_from_file_location(full_name, SERVICES_ROOT / "company_filing_expansion_planner.py")
module = module_from_spec(spec)
sys.modules[full_name] = module
assert spec.loader is not None
spec.loader.exec_module(module)


def test_build_company_filing_expansion_batch_marks_resolution_gap():
    entity_expansion_batch = {
        "expansions": [
            {
                "canonical_entity_name": "Hitachi Energy",
                "system_label": "grid equipment and transformer buildout",
                "priority_tier": "high",
                "entity_role": "equipment_or_component_supplier",
                "origin_corporate_family_candidate_id": "cf_hitachi_energy",
                "origin_bounded_entity_candidate_ids": ["bec_hitachi", "bec_hitachi_energy"],
                "member_entities": ["Hitachi", "Hitachi Energy"],
                "supporting_artifact_ids": ["a1", "a2"],
                "supporting_titles": ["Hitachi Energy commits $250M", "Hitachi unveils $1B"],
                "local_source_classes": ["trade_press"],
                "local_coverage_status": "single_source_local",
                "next_priority_source_classes": ["company_filing", "company_release"],
                "ready_for_filing_expansion": True,
            }
        ]
    }

    result = module.build_company_filing_expansion_batch(entity_expansion_batch)

    assert result["metrics"]["company_filing_expansion_plan_count"] == 1
    plan = result["plans"][0]
    assert plan["issuer_resolution_status"] == "unresolved"
    assert plan["company_filing_status"] == "not_collected"
    assert plan["candidate_filing_form_sets"]["domestic_public"] == ["10-K", "10-Q", "8-K"]
    assert plan["collection_gate"] == "resolve_issuer_before_filing_fetch"

