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

full_name = "app.services.blind_run_entity_freeze_builder"
spec = spec_from_file_location(full_name, SERVICES_ROOT / "blind_run_entity_freeze_builder.py")
module = module_from_spec(spec)
sys.modules[full_name] = module
assert spec.loader is not None
spec.loader.exec_module(module)


def test_build_blind_run_entity_freeze_batch_returns_expansions_research_sets_and_entities() -> None:
    bounded_universe_batch = {
        "candidates": [
            {
                "bounded_universe_candidate_id": "buc_grid",
                "as_of_date": "2025-12-17",
                "system_label": "grid equipment and transformer buildout",
                "next_source_classes": ["company_release", "trade_press", "company_filing"],
                "suspected_stress_layers": ["transformers", "switchgear"],
                "confidence": "high",
            }
        ]
    }
    prefilter_batches = [
        {
            "kept_artifacts": [
                {
                    "artifact_id": "a1",
                    "source_class": "company_release",
                    "issuing_company_name": "GridCore Manufacturing",
                    "title": "GridCore Manufacturing breaks ground on new power transformer production plant",
                    "body_text": "The new site will increase transformer output for utility projects.",
                    "source_url": "https://example.com/a1",
                }
            ],
            "review_artifacts": [],
        }
    ]

    result = module.build_blind_run_entity_freeze_batch(bounded_universe_batch, prefilter_batches)

    assert result["metrics"] == {
        "input_bounded_universe_candidate_count": 1,
        "expansion_plan_count": 1,
        "bounded_research_set_count": 1,
        "bounded_entity_candidate_count": 1,
    }
    assert result["expansion_plans"][0]["system_label"] == "grid equipment and transformer buildout"
    assert result["research_sets"][0]["matched_artifact_ids"] == ["a1"]
    assert result["entity_candidates"][0]["entity_name"] == "GridCore Manufacturing"
