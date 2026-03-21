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

full_name = "app.services.bounded_universe_expander"
spec = spec_from_file_location(full_name, SERVICES_ROOT / "bounded_universe_expander.py")
module = module_from_spec(spec)
sys.modules[full_name] = module
assert spec.loader is not None
spec.loader.exec_module(module)


def test_build_bounded_universe_expansion_batch_uses_transformer_template():
    bounded_universe_batch = {
        "candidates": [
            {
                "bounded_universe_candidate_id": "buc_grid",
                "as_of_date": "2025-11-19",
                "system_label": "grid equipment and transformer buildout",
                "next_source_classes": ["company_release", "trade_press", "company_filing"],
                "suspected_stress_layers": ["transformers", "switchgear"],
                "confidence": "high",
            }
        ]
    }

    result = module.build_bounded_universe_expansion_batch(bounded_universe_batch)

    assert result["metrics"]["bounded_universe_expansion_plan_count"] == 1
    plan = result["plans"][0]
    assert plan["origin_bounded_universe_candidate_id"] == "buc_grid"
    assert "transformer manufacturers" in plan["entity_lane_hints"]
    assert "transformer production expansion" in plan["query_seed_terms"]
    assert "company_filing" in plan["source_classes_priority"]
