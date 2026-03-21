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

full_name = "app.services.corporate_family_normalizer"
spec = spec_from_file_location(full_name, SERVICES_ROOT / "corporate_family_normalizer.py")
module = module_from_spec(spec)
sys.modules[full_name] = module
assert spec.loader is not None
spec.loader.exec_module(module)


def test_build_corporate_family_batch_merges_prefix_family():
    bounded_entity_batch = {
        "candidates": [
            {
                "bounded_entity_candidate_id": "bec1",
                "system_label": "grid equipment and transformer buildout",
                "as_of_date": "2025-12-17",
                "entity_name": "Hitachi",
                "entity_role": "equipment_or_component_supplier",
                "priority_tier": "high",
                "source_classes": ["trade_press"],
                "supporting_artifact_ids": ["a1"],
                "supporting_titles": ["Hitachi unveils $1B grid manufacturing investment"],
                "recommended_next_source_classes": ["company_release", "trade_press", "company_filing"],
            },
            {
                "bounded_entity_candidate_id": "bec2",
                "system_label": "grid equipment and transformer buildout",
                "as_of_date": "2025-12-17",
                "entity_name": "Hitachi Energy",
                "entity_role": "equipment_or_component_supplier",
                "priority_tier": "high",
                "source_classes": ["trade_press"],
                "supporting_artifact_ids": ["a2"],
                "supporting_titles": ["Hitachi Energy commits $250M to address transformer shortage"],
                "recommended_next_source_classes": ["company_release", "trade_press", "company_filing"],
            },
        ]
    }

    result = module.build_corporate_family_batch(bounded_entity_batch)

    assert result["metrics"]["corporate_family_candidate_count"] == 1
    family = result["families"][0]
    assert family["canonical_entity_name"] == "Hitachi Energy"
    assert family["member_entities"] == ["Hitachi", "Hitachi Energy"]
    assert family["merge_relation"] == "prefix_family_merge"

