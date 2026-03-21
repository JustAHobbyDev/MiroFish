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

full_name = "app.services.structural_pressure_merger"
spec = spec_from_file_location(full_name, SERVICES_ROOT / "structural_pressure_merger.py")
module = module_from_spec(spec)
sys.modules[full_name] = module
assert spec.loader is not None
spec.loader.exec_module(module)


def test_build_structural_pressure_candidate_batch_merges_adjacent_clusters():
    capital_cluster_batch = {
        "clusters": [
            {
                "capital_flow_cluster_id": "cfc_1",
                "as_of_date": "2026-02-28",
                "system_label": "utility and large-load power buildout",
                "demand_driver_summary": "Utility load and large-load infrastructure spend are rising.",
                "signal_count": 3,
                "source_classes": ["trade_press"],
                "time_window": {
                    "start_date": "2026-01-01",
                    "end_date": "2026-02-28",
                },
                "confidence": "medium",
            }
        ]
    }
    energy_cluster_batch = {
        "clusters": [
            {
                "energy_flow_pressure_cluster_id": "efpc_1",
                "as_of_date": "2026-02-28",
                "system_label": "utility and large-load power demand pressure",
                "signal_count": 4,
                "source_classes": ["trade_press"],
                "time_window": {
                    "start_date": "2026-01-05",
                    "end_date": "2026-02-28",
                },
                "confidence": "high",
                "strong_infrastructure_response_evidence": True,
            }
        ]
    }

    result = module.build_structural_pressure_candidate_batch(
        capital_cluster_batch,
        energy_cluster_batch,
    )

    assert result["metrics"]["structural_pressure_candidate_count"] == 1
    candidate = result["candidates"][0]
    assert candidate["supporting_capital_flow_cluster_ids"] == ["cfc_1"]
    assert candidate["supporting_energy_flow_pressure_cluster_ids"] == ["efpc_1"]
    assert candidate["system_label"] == "utility and large-load power demand pressure"
    assert candidate["source_diversity_status"] == "single_source_class"
    assert candidate["requires_source_diversity_corroboration"] is True
    assert candidate["source_diversity_corroboration_satisfied"] is False
    assert candidate["boundedness_status"] == "bounded"
    assert candidate["requires_system_narrowing"] is False
    assert candidate["bounded_universe_promotion_ready"] is False


def test_build_structural_pressure_candidate_batch_holds_weak_energy_only_clusters_upstream():
    capital_cluster_batch = {"clusters": []}
    energy_cluster_batch = {
        "clusters": [
            {
                "energy_flow_pressure_cluster_id": "efpc_weak",
                "as_of_date": "2026-02-28",
                "system_label": "utility and large-load power demand pressure",
                "signal_count": 2,
                "source_classes": ["trade_press"],
                "time_window": {
                    "start_date": "2026-01-05",
                    "end_date": "2026-02-28",
                },
                "confidence": "medium",
                "strong_infrastructure_response_evidence": False,
            }
        ]
    }

    result = module.build_structural_pressure_candidate_batch(
        capital_cluster_batch,
        energy_cluster_batch,
    )

    assert result["metrics"]["structural_pressure_candidate_count"] == 0
    assert result["held_upstream_energy_flow_pressure_cluster_ids"] == ["efpc_weak"]


def test_build_structural_pressure_candidate_batch_caps_high_confidence_single_source_candidates():
    capital_cluster_batch = {
        "clusters": [
            {
                "capital_flow_cluster_id": "cfc_1",
                "as_of_date": "2026-02-28",
                "system_label": "grid equipment and transformer buildout",
                "demand_driver_summary": "Grid equipment spend is accelerating.",
                "signal_count": 5,
                "source_classes": ["trade_press"],
                "time_window": {
                    "start_date": "2026-01-01",
                    "end_date": "2026-02-28",
                },
                "confidence": "high",
            }
        ]
    }
    energy_cluster_batch = {
        "clusters": [
            {
                "energy_flow_pressure_cluster_id": "efpc_1",
                "as_of_date": "2026-02-28",
                "system_label": "grid equipment and transformer pressure",
                "signal_count": 4,
                "source_classes": ["trade_press"],
                "time_window": {
                    "start_date": "2026-01-05",
                    "end_date": "2026-02-28",
                },
                "confidence": "high",
                "strong_infrastructure_response_evidence": True,
            }
        ]
    }

    result = module.build_structural_pressure_candidate_batch(
        capital_cluster_batch,
        energy_cluster_batch,
    )

    candidate = result["candidates"][0]
    assert candidate["confidence"] == "medium"
    assert candidate["source_diversity_status"] == "single_source_class"
    assert candidate["requires_source_diversity_corroboration"] is True
    assert candidate["source_diversity_corroboration_satisfied"] is False


def test_build_structural_pressure_candidate_batch_keeps_multi_source_high_confidence():
    capital_cluster_batch = {
        "clusters": [
            {
                "capital_flow_cluster_id": "cfc_1",
                "as_of_date": "2026-02-28",
                "system_label": "grid equipment and transformer buildout",
                "demand_driver_summary": "Grid equipment spend is accelerating.",
                "signal_count": 5,
                "source_classes": ["trade_press", "company_release"],
                "time_window": {
                    "start_date": "2026-01-01",
                    "end_date": "2026-02-28",
                },
                "confidence": "high",
            }
        ]
    }
    energy_cluster_batch = {
        "clusters": [
            {
                "energy_flow_pressure_cluster_id": "efpc_1",
                "as_of_date": "2026-02-28",
                "system_label": "grid equipment and transformer pressure",
                "signal_count": 4,
                "source_classes": ["trade_press", "government"],
                "time_window": {
                    "start_date": "2026-01-05",
                    "end_date": "2026-02-28",
                },
                "confidence": "high",
                "strong_infrastructure_response_evidence": True,
            }
        ]
    }

    result = module.build_structural_pressure_candidate_batch(
        capital_cluster_batch,
        energy_cluster_batch,
    )

    candidate = result["candidates"][0]
    assert candidate["confidence"] == "high"
    assert candidate["source_diversity_status"] == "multi_source_class"
    assert candidate["requires_source_diversity_corroboration"] is False
    assert candidate["source_diversity_corroboration_satisfied"] is True
    assert candidate["boundedness_status"] == "bounded"
    assert candidate["requires_system_narrowing"] is False
    assert candidate["bounded_universe_promotion_ready"] is True


def test_build_structural_pressure_candidate_batch_keeps_corroborated_but_broad_candidate_promotion_gated():
    capital_cluster_batch = {
        "clusters": [
            {
                "capital_flow_cluster_id": "cfc_1",
                "as_of_date": "2026-02-28",
                "system_label": "industrial manufacturing expansion",
                "demand_driver_summary": "Industrial expansion is recurring.",
                "signal_count": 5,
                "source_classes": ["trade_press", "company_release"],
                "time_window": {
                    "start_date": "2026-01-01",
                    "end_date": "2026-02-28",
                },
                "confidence": "medium",
            }
        ]
    }
    energy_cluster_batch = {"clusters": []}

    result = module.build_structural_pressure_candidate_batch(
        capital_cluster_batch,
        energy_cluster_batch,
    )

    candidate = result["candidates"][0]
    assert candidate["source_diversity_corroboration_satisfied"] is True
    assert candidate["boundedness_status"] == "broad_review_required"
    assert candidate["requires_system_narrowing"] is True
    assert candidate["bounded_universe_promotion_ready"] is False
