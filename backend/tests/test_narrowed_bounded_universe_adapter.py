from app.services.narrowed_bounded_universe_adapter import (
    build_narrowed_bounded_universe_candidate_batch,
)


def test_build_narrowed_bounded_universe_candidate_batch_creates_exploratory_candidate() -> None:
    result = build_narrowed_bounded_universe_candidate_batch(
        {
            "narrowed_candidates": [
                {
                    "narrowed_pressure_candidate_id": "nsp_data_center_backup_power_equipment_buildout_2025_07_16",
                    "origin_pressure_candidate_id": "spc_backup",
                    "system_label": "data center backup-power equipment buildout",
                    "narrowing_basis": {
                        "source_classes": ["trade_press"],
                        "research_ready": True,
                        "support_provenance_status": "real_only",
                        "boundedness_status": "bounded",
                    },
                    "suspected_stress_layers": ["generator packages"],
                }
            ]
        }
    )

    assert result["metrics"]["bounded_universe_candidate_count"] == 1
    candidate = result["candidates"][0]
    assert candidate["status"] == "exploratory_candidate"
    assert candidate["next_source_classes"] == ["trade_press"]
    assert candidate["bounding_basis"]["support_provenance_status"] == "real_only"

