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

full_name = "app.services.issuer_resolution_planner"
spec = spec_from_file_location(full_name, SERVICES_ROOT / "issuer_resolution_planner.py")
module = module_from_spec(spec)
sys.modules[full_name] = module
assert spec.loader is not None
spec.loader.exec_module(module)


def test_build_issuer_resolution_batch_derives_foreign_hint():
    company_filing_expansion_batch = {
        "plans": [
            {
                "company_filing_expansion_plan_id": "cfep_westrafo",
                "canonical_entity_name": "Westrafo",
                "system_label": "grid equipment and transformer buildout",
                "priority_tier": "medium",
                "member_entities": ["Westrafo"],
                "supporting_titles": ["Italy-based Westrafo to build its first US transformer plant"],
            }
        ]
    }

    result = module.build_issuer_resolution_batch(company_filing_expansion_batch)

    assert result["metrics"]["issuer_resolution_plan_count"] == 1
    plan = result["plans"][0]
    assert plan["route_hypothesis"] == "foreign_route_hint"
    assert plan["foreign_geography_hints"] == ["Italy"]
    assert "20-F if SEC-registered foreign issuer" in plan["candidate_resolution_paths"]

