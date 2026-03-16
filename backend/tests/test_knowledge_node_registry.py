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

full_name = "app.services.knowledge_node_registry"
spec = spec_from_file_location(full_name, SERVICES_ROOT / "knowledge_node_registry.py")
module = module_from_spec(spec)
sys.modules[full_name] = module
assert spec.loader is not None
spec.loader.exec_module(module)


def _load_json(path: str):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def test_build_knowledge_node_registry_aggregates_mp():
    manifest = _load_json("research/analysis/2026-03-16-promoted-parse-manifest-v2.json")["rows"]
    parse_records = []
    for row in manifest:
        graduation = _load_json(row["graduation"])
        parse_records.append(
            {
                "name": row["name"],
                "structural_parse_path": row["structural_parse"],
                "structural_parse": _load_json(row["structural_parse"]),
                "graduation_status": graduation["graduation_status"],
                "graduation_score_0_to_100": graduation["weighted_score_0_to_100"],
            }
        )

    payload = module.build_knowledge_node_registry(
        parse_records,
        _load_json("research/analysis/2026-03-16-promoted-parse-candidates-v2.json")["rows"],
        _load_json("research/analysis/2026-03-16-promoted-parse-picks-v2.json")["rows"],
    )

    assert payload["registry_version"] == "v1"
    assert payload["summary"]["multi_pointer_underlyings"] == ["MP"]

    rows = {row["canonical_name"]: row for row in payload["rows"]}
    mp = rows["MP"]
    assert mp["aggregate_view"]["pointer_count"] == 2
    assert {pointer["market_theme"] for pointer in mp["thesis_pointers"]} == {
        "Rare Earth Magnet Sovereignty",
        "Robotics Supply Chain",
    }
    assert len(mp["parse_entity_bindings"]) == 2
    assert set(mp["expression_views"]) == {"leaps_call", "shares"}

