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

full_name = "app.services.bounded_entity_candidate_builder"
spec = spec_from_file_location(full_name, SERVICES_ROOT / "bounded_entity_candidate_builder.py")
module = module_from_spec(spec)
sys.modules[full_name] = module
assert spec.loader is not None
spec.loader.exec_module(module)


def test_build_bounded_entity_candidate_batch_ranks_transformer_entities():
    research_set_batch = {
        "research_sets": [
            {
                "bounded_research_set_id": "brs_grid",
                "system_label": "grid equipment and transformer buildout",
                "as_of_date": "2025-12-17",
                "matched_artifacts": [
                    {
                        "artifact_id": "a1",
                        "source_class": "company_release",
                        "title": "GridCore Manufacturing breaks ground on new power transformer production plant",
                        "matched_terms": ["transformer production expansion", "transformers"],
                        "match_score": 7,
                    },
                    {
                        "artifact_id": "a2",
                        "source_class": "trade_press",
                        "title": "Hitachi Energy commits $250M to address transformer shortage",
                        "matched_terms": ["transformers"],
                        "match_score": 8,
                    },
                ],
                "entity_candidates": [
                    {
                        "entity_name": "GridCore Manufacturing",
                        "artifact_ids": ["a1"],
                    },
                    {
                        "entity_name": "Hitachi Energy",
                        "artifact_ids": ["a2"],
                    },
                ],
            }
        ]
    }

    result = module.build_bounded_entity_candidate_batch(research_set_batch)

    assert result["metrics"]["bounded_entity_candidate_count"] == 2
    assert result["candidates"][0]["priority_tier"] == "high"
    assert result["candidates"][0]["entity_role"] == "equipment_or_component_supplier"
    assert "company_filing" in result["candidates"][0]["recommended_next_source_classes"]
    assert result["candidates"][0]["support_provenance_status"] == "real_only"
