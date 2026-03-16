import json
import sys
import types
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SERVICES_ROOT = Path(__file__).resolve().parents[1] / "app" / "services"

app_pkg = types.ModuleType("app")
app_pkg.__path__ = []
services_pkg = types.ModuleType("app.services")
services_pkg.__path__ = [str(SERVICES_ROOT)]
sys.modules["app"] = app_pkg
sys.modules["app.services"] = services_pkg

full_name = "app.services.node_aware_ranking"
spec = spec_from_file_location(full_name, SERVICES_ROOT / "node_aware_ranking.py")
module = module_from_spec(spec)
sys.modules[full_name] = module
assert spec.loader is not None
spec.loader.exec_module(module)


def _load_json(path: str):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def test_build_node_aware_ranking_aggregates_mp_review_surface():
    payload = module.build_node_aware_ranking(
        _load_json("research/analysis/2026-03-16-knowledge-node-registry-v1.json")
    )

    assert payload["method"] == "canonical knowledge-node registry -> node-aware review ranking"
    rows = {row["underlying"]: row for row in payload["rows"]}
    mp = rows["MP"]
    assert mp["pointer_count"] == 2
    assert mp["expression_conflict"] is True
    assert mp["primary_expression_view"] == "shares"
    assert mp["alternate_expression_views"] == ["leaps_call"]
    assert set(mp["themes"]) == {
        "Rare Earth Magnet Sovereignty",
        "Robotics Supply Chain",
    }
    assert "Sintered NdFeB Magnet Manufacturing" in mp["strongest_supporting_process_layers"]
    assert len(mp["thesis_pointers"]) == 2

