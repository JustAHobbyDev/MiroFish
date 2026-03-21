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

full_name = "app.services.bounded_entity_expander"
spec = spec_from_file_location(full_name, SERVICES_ROOT / "bounded_entity_expander.py")
module = module_from_spec(spec)
sys.modules[full_name] = module
assert spec.loader is not None
spec.loader.exec_module(module)


def test_build_bounded_entity_expansion_batch_uses_priority_entity_list():
    family_batch = {
        "families": [
            {
                "canonical_entity_name": "Hitachi Energy",
                "system_label": "grid equipment and transformer buildout",
                "priority_tier": "high",
                "entity_role": "equipment_or_component_supplier",
                "member_entities": ["Hitachi", "Hitachi Energy"],
                "supporting_artifact_ids": ["a1", "a2"],
                "supporting_titles": ["Hitachi Energy commits $250M", "Hitachi unveils $1B"],
                "source_classes": ["trade_press"],
                "recommended_next_source_classes": ["company_release", "trade_press", "company_filing"],
            },
            {
                "canonical_entity_name": "ConductorWorks",
                "system_label": "grid equipment and transformer buildout",
                "priority_tier": "medium",
                "entity_role": "equipment_or_component_supplier",
                "member_entities": ["ConductorWorks"],
                "supporting_artifact_ids": ["a3"],
                "supporting_titles": ["ConductorWorks invests in cable factory"],
                "source_classes": ["company_release"],
                "recommended_next_source_classes": ["company_release", "trade_press", "company_filing"],
            },
        ]
    }
    assessment = {
        "first_downstream_entity_expansion_test": {
            "system_label": "grid equipment and transformer buildout",
            "initial_priority_entities": ["Hitachi Energy"],
        }
    }

    result = module.build_bounded_entity_expansion_batch(family_batch, assessment)

    assert result["metrics"]["selected_entity_expansion_count"] == 1
    expansion = result["expansions"][0]
    assert expansion["canonical_entity_name"] == "Hitachi Energy"
    assert expansion["filing_gap"] is True
    assert expansion["ready_for_filing_expansion"] is True

