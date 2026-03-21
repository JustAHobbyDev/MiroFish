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

full_name = "app.services.bounded_universe_builder"
spec = spec_from_file_location(full_name, SERVICES_ROOT / "bounded_universe_builder.py")
module = module_from_spec(spec)
sys.modules[full_name] = module
assert spec.loader is not None
spec.loader.exec_module(module)


def test_build_bounded_universe_candidate_batch_promotes_only_ready_candidates():
    structural_pressure_batch = {
        "candidates": [
            {
                "pressure_candidate_id": "spc_grid",
                "as_of_date": "2025-11-19",
                "system_label": "grid equipment and transformer buildout",
                "source_diversity_corroboration_satisfied": True,
                "requires_system_narrowing": False,
                "bounded_universe_promotion_ready": True,
                "source_classes": ["company_release", "trade_press"],
                "confidence": "high",
            },
            {
                "pressure_candidate_id": "spc_industrial",
                "as_of_date": "2026-01-09",
                "system_label": "industrial manufacturing expansion",
                "source_diversity_corroboration_satisfied": True,
                "requires_system_narrowing": True,
                "bounded_universe_promotion_ready": False,
                "source_classes": ["company_release", "trade_press"],
                "confidence": "high",
            },
        ]
    }

    result = module.build_bounded_universe_candidate_batch(structural_pressure_batch)

    assert result["metrics"]["bounded_universe_candidate_count"] == 1
    candidate = result["candidates"][0]
    assert candidate["origin_pressure_candidate_id"] == "spc_grid"
    assert candidate["system_label"] == "grid equipment and transformer buildout"
    assert candidate["bounding_basis"]["promotion_ready"] is True
    assert "company_filing" in candidate["next_source_classes"]
