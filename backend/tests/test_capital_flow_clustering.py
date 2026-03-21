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

full_name = "app.services.capital_flow_clustering"
spec = spec_from_file_location(full_name, SERVICES_ROOT / "capital_flow_clustering.py")
module = module_from_spec(spec)
sys.modules[full_name] = module
assert spec.loader is not None
spec.loader.exec_module(module)


def test_build_capital_flow_cluster_batch_groups_compatible_signals():
    prefilter_batch = {
        "kept_artifacts": [
            {
                "artifact_id": "a1",
                "published_at": "2026-01-10",
                "title": "Transformer maker invests in Ohio plant",
                "body_text": "A new transformer plant will serve utilities and data centers in the United States.",
            },
            {
                "artifact_id": "a2",
                "published_at": "2026-02-02",
                "title": "Switchgear factory expansion targets utility demand",
                "body_text": "The U.S. expansion responds to utility and data center power-product demand.",
            },
            {
                "artifact_id": "a3",
                "published_at": "2026-02-20",
                "title": "Biopharma company expands manufacturing in North Carolina",
                "body_text": "The company is building additional pharmaceutical manufacturing space.",
            },
        ],
        "review_artifacts": [],
    }
    signal_batch = {
        "name": "capital_batch",
        "source_class": "trade_press",
        "processed_results": [
            {
                "artifact_id": "a1",
                "source_class": "trade_press",
                "produced_candidates": True,
                "prefilter_triage": "keep",
                "candidates": [
                    {
                        "observable_statement": "The company will invest in a new transformer plant.",
                        "capital_flow_implication_type": "direct_capital_allocation",
                        "observation_directness": "direct",
                        "capital_flow_implication": "Capital is moving into transformer production.",
                        "system_hints": ["transformers", "grid equipment"],
                        "physical_implication": "A new plant will expand transformer output.",
                        "confidence": "high",
                    }
                ],
            },
            {
                "artifact_id": "a2",
                "source_class": "trade_press",
                "produced_candidates": True,
                "prefilter_triage": "keep",
                "candidates": [
                    {
                        "observable_statement": "The company is expanding its switchgear factory.",
                        "capital_flow_implication_type": "capacity_response",
                        "observation_directness": "direct",
                        "capital_flow_implication": "Capital is moving into switchgear capacity expansion.",
                        "system_hints": ["switchgear", "utility grid"],
                        "physical_implication": "Factory output for power equipment will rise.",
                        "confidence": "high",
                    }
                ],
            },
            {
                "artifact_id": "a3",
                "source_class": "trade_press",
                "produced_candidates": True,
                "prefilter_triage": "keep",
                "candidates": [
                    {
                        "observable_statement": "The company is building more pharmaceutical capacity.",
                        "capital_flow_implication_type": "direct_capital_allocation",
                        "observation_directness": "direct",
                        "capital_flow_implication": "Capital is moving into biopharma manufacturing expansion.",
                        "system_hints": ["biopharma manufacturing"],
                        "physical_implication": "More pharmaceutical plant capacity will be added.",
                        "confidence": "medium",
                    }
                ],
            },
        ],
    }

    result = module.build_capital_flow_cluster_batch(signal_batch, prefilter_batch)

    assert result["metrics"]["cluster_count"] == 1
    cluster = result["clusters"][0]
    assert cluster["system_label"] == "grid equipment and transformer buildout"
    assert cluster["artifact_count"] == 2
    assert cluster["signal_count"] == 2
    assert cluster["confidence"] in {"low", "medium", "high"}
