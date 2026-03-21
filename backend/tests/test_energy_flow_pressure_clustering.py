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

full_name = "app.services.energy_flow_pressure_clustering"
spec = spec_from_file_location(full_name, SERVICES_ROOT / "energy_flow_pressure_clustering.py")
module = module_from_spec(spec)
sys.modules[full_name] = module
assert spec.loader is not None
spec.loader.exec_module(module)


def test_build_energy_flow_pressure_cluster_batch_groups_utility_pressure_signals():
    prefilter_batch = {
        "kept_artifacts": [],
        "review_artifacts": [
            {
                "artifact_id": "e1",
                "publisher_or_author": "Utility Dive",
                "published_at": "2026-01-05",
                "title": "PG&E data center pipeline swells to 10GW",
                "body_text": "The utility reported 10GW of data center load in the pipeline.",
            },
            {
                "artifact_id": "e2",
                "publisher_or_author": "Utility Dive",
                "published_at": "2026-02-01",
                "title": "Exelon data center pipeline jumps to 17GW",
                "body_text": "The utility expects load growth and new approaches to power supply.",
            },
            {
                "artifact_id": "e3",
                "publisher_or_author": "Utility Dive",
                "published_at": "2026-02-15",
                "title": "Hyundai boosts US investments to $26B through 2028",
                "body_text": "Vehicle and robotics manufacturing expansion.",
            },
        ],
    }
    signal_batch = {
        "name": "energy_batch",
        "source_class": "trade_press",
        "processed_results": [
            {
                "artifact_id": "e1",
                "source_class": "trade_press",
                "produced_candidates": True,
                "prefilter_triage": "review",
                "candidates": [
                    {
                        "observable_statement": "PG&E reported 10GW of data center capacity in its pipeline.",
                        "energy_pressure_type": "load_growth",
                        "relationship_to_capital_flow": "energy_flow_pressure_only",
                        "system_hints": ["utility grid", "data center load"],
                        "physical_implication": "More power infrastructure may be needed.",
                        "confidence": "medium",
                    }
                ],
            },
            {
                "artifact_id": "e2",
                "source_class": "trade_press",
                "produced_candidates": True,
                "prefilter_triage": "review",
                "candidates": [
                    {
                        "observable_statement": "Exelon expects positive load growth and new approaches to adequate power supply.",
                        "energy_pressure_type": "infrastructure_response_need",
                        "relationship_to_capital_flow": "energy_flow_pressure_and_capital_flow",
                        "system_hints": ["utility load growth", "generation response"],
                        "physical_implication": "New utility response may be needed.",
                        "confidence": "high",
                    }
                ],
            },
            {
                "artifact_id": "e3",
                "source_class": "trade_press",
                "produced_candidates": False,
                "prefilter_triage": "review",
                "candidates": [],
                "rejection_reason": "No candidate retained after energy-flow postfilter.",
            },
        ],
    }

    result = module.build_energy_flow_pressure_cluster_batch(signal_batch, prefilter_batch)

    assert result["metrics"]["cluster_count"] == 1
    cluster = result["clusters"][0]
    assert cluster["system_label"] == "utility and large-load power demand pressure"
    assert cluster["artifact_count"] == 2
    assert cluster["strong_infrastructure_response_evidence"] is True


def test_build_energy_flow_pressure_cluster_batch_single_publisher_trade_press_does_not_get_high_confidence():
    prefilter_batch = {
        "kept_artifacts": [],
        "review_artifacts": [
            {
                "artifact_id": "e1",
                "publisher_or_author": "Utility Dive",
                "published_at": "2026-01-05",
                "title": "Utility sees data center load growth surge",
                "body_text": "Large-load demand is accelerating and creating response needs.",
            },
            {
                "artifact_id": "e2",
                "publisher_or_author": "Utility Dive",
                "published_at": "2026-01-20",
                "title": "Utility pipeline pressure grows with interconnection backlog",
                "body_text": "The utility described more infrastructure response needs.",
            },
            {
                "artifact_id": "e3",
                "publisher_or_author": "Utility Dive",
                "published_at": "2026-02-01",
                "title": "Grid equipment strain follows utility load growth",
                "body_text": "Pressure is rising on transformers and substation equipment.",
            },
            {
                "artifact_id": "e4",
                "publisher_or_author": "Utility Dive",
                "published_at": "2026-02-15",
                "title": "Utility load growth drives infrastructure response",
                "body_text": "The system requires additional infrastructure to support demand.",
            },
        ],
    }
    signal_batch = {
        "name": "energy_batch",
        "source_class": "trade_press",
        "processed_results": [
            {
                "artifact_id": "e1",
                "source_class": "trade_press",
                "produced_candidates": True,
                "prefilter_triage": "review",
                "candidates": [
                    {
                        "observable_statement": "Load growth is accelerating.",
                        "energy_pressure_type": "load_growth",
                        "relationship_to_capital_flow": "energy_flow_pressure_only",
                        "system_hints": ["utility load"],
                        "physical_implication": "More load must be served.",
                        "confidence": "high",
                    }
                ],
            },
            {
                "artifact_id": "e2",
                "source_class": "trade_press",
                "produced_candidates": True,
                "prefilter_triage": "review",
                "candidates": [
                    {
                        "observable_statement": "Pipeline pressure is growing.",
                        "energy_pressure_type": "pipeline_pressure",
                        "relationship_to_capital_flow": "energy_flow_pressure_only",
                        "system_hints": ["utility pipeline"],
                        "physical_implication": "More interconnection demand must be served.",
                        "confidence": "high",
                    }
                ],
            },
            {
                "artifact_id": "e3",
                "source_class": "trade_press",
                "produced_candidates": True,
                "prefilter_triage": "review",
                "candidates": [
                    {
                        "observable_statement": "Equipment strain is rising.",
                        "energy_pressure_type": "capacity_tightness",
                        "relationship_to_capital_flow": "energy_flow_pressure_only",
                        "system_hints": ["transformers"],
                        "physical_implication": "More equipment response may be needed.",
                        "confidence": "high",
                    }
                ],
            },
            {
                "artifact_id": "e4",
                "source_class": "trade_press",
                "produced_candidates": True,
                "prefilter_triage": "review",
                "candidates": [
                    {
                        "observable_statement": "Infrastructure response is required.",
                        "energy_pressure_type": "infrastructure_response_need",
                        "relationship_to_capital_flow": "energy_flow_pressure_only",
                        "system_hints": ["utility load"],
                        "physical_implication": "The grid must expand to serve demand.",
                        "confidence": "high",
                    }
                ],
            },
        ],
    }

    result = module.build_energy_flow_pressure_cluster_batch(signal_batch, prefilter_batch)

    cluster = result["clusters"][0]
    assert cluster["publisher_diversity_status"] == "single_publisher"
    assert cluster["publisher_diversity_count"] == 1
    assert cluster["confidence"] == "medium"
