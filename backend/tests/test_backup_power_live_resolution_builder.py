from app.services.backup_power_live_resolution_builder import (
    build_backup_power_live_resolution_batch,
)


def test_build_backup_power_live_resolution_batch() -> None:
    result = build_backup_power_live_resolution_batch(
        {
            "queue_rows": [
                {
                    "canonical_entity_name": "AVL",
                    "system_label": "data center backup-power equipment buildout",
                },
                {
                    "canonical_entity_name": "Rolls-Royce",
                    "system_label": "data center backup-power equipment buildout",
                },
            ]
        }
    )

    assert result["metrics"]["evaluated_real_entity_count"] == 2
    assert result["metrics"]["resolved_private_company_route_count"] == 1
    assert result["metrics"]["resolved_direct_foreign_public_route_count"] == 1
    assert result["results"][0]["system_label"] == "data center backup-power equipment buildout"
