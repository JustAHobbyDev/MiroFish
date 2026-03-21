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

full_name = "app.services.bounded_research_set_builder"
spec = spec_from_file_location(full_name, SERVICES_ROOT / "bounded_research_set_builder.py")
module = module_from_spec(spec)
sys.modules[full_name] = module
assert spec.loader is not None
spec.loader.exec_module(module)


def test_build_bounded_research_set_batch_matches_transformer_artifacts_and_entities():
    expansion_batch = {
        "plans": [
            {
                "bounded_universe_expansion_plan_id": "bue_grid",
                "as_of_date": "2025-12-17",
                "system_label": "grid equipment and transformer buildout",
                "query_seed_terms": [
                    "transformer production expansion",
                    "switchgear manufacturing expansion",
                    "substation equipment capacity",
                ],
                "negative_boundaries": ["consumer electrical products"],
                "source_classes_priority": ["company_release", "trade_press"],
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
                },
                {
                    "artifact_id": "a2",
                    "source_class": "trade_press",
                    "title": "Eaton invests $340M in US transformer production",
                    "body_text": "Transformer production expansion targets utility and data center demand.",
                    "source_url": "https://example.com/a2",
                },
                {
                    "artifact_id": "a3",
                    "source_class": "trade_press",
                    "title": "Consumer appliance maker opens showroom",
                    "body_text": "Generic consumer electrical products.",
                    "source_url": "https://example.com/a3",
                },
            ],
            "review_artifacts": [],
        }
    ]

    result = module.build_bounded_research_set_batch(expansion_batch, prefilter_batches)

    assert result["metrics"]["bounded_research_set_count"] == 1
    research_set = result["research_sets"][0]
    assert research_set["coverage_metrics"]["matched_artifact_count"] == 2
    assert research_set["coverage_metrics"]["entity_candidate_count"] >= 1
    assert research_set["entity_candidates"][0]["entity_name"] in {"GridCore Manufacturing", "Eaton"}


def test_build_bounded_research_set_batch_requires_lane_anchor_keywords():
    expansion_batch = {
        "plans": [
            {
                "bounded_universe_expansion_plan_id": "bue_dc_power",
                "as_of_date": "2025-11-21",
                "system_label": "data center power demand buildout",
                "query_seed_terms": [
                    "data center campus power expansion",
                    "substation buildout for data centers",
                    "utility interconnection for hyperscale",
                    "transformer demand for data centers",
                ],
                "negative_boundaries": ["generic cloud software demand"],
                "source_classes_priority": ["company_release", "trade_press"],
                "suspected_stress_layers": ["transformers", "substations"],
                "confidence": "high",
            }
        ]
    }
    prefilter_batches = [
        {
            "kept_artifacts": [
                {
                    "artifact_id": "dc1",
                    "source_class": "trade_press",
                    "title": "EdgeCore expands Mesa data center campus in Arizona",
                    "body_text": "The campus will require new substation capacity and power delivery upgrades.",
                    "source_url": "https://example.com/dc1",
                },
                {
                    "artifact_id": "grid1",
                    "source_class": "trade_press",
                    "title": "Eaton invests $340M in US transformer production",
                    "body_text": "The expansion targets grid modernization and utility demand.",
                    "source_url": "https://example.com/grid1",
                },
            ],
            "review_artifacts": [],
        }
    ]

    result = module.build_bounded_research_set_batch(expansion_batch, prefilter_batches)

    research_set = result["research_sets"][0]
    assert research_set["matched_artifact_ids"] == ["dc1"]
