from app.services.bounded_entity_lane_narrower import (
    build_bounded_entity_lane_narrowing_batch,
)


def test_build_bounded_entity_lane_narrowing_batch_filters_to_real_data_center_utility_rows() -> None:
    batch = build_bounded_entity_lane_narrowing_batch(
        {
            "candidates": [
                {
                    "entity_name": "DTE",
                    "system_label": "utility and large-load power buildout",
                    "support_provenance_status": "real_only",
                    "supporting_titles": [
                        "DTE inks first data center deal to grow electric load 25%"
                    ],
                },
                {
                    "entity_name": "Synthetic Utility",
                    "system_label": "utility and large-load power buildout",
                    "support_provenance_status": "synthetic_only",
                    "supporting_titles": [
                        "Synthetic utility data center project"
                    ],
                },
                {
                    "entity_name": "Eaton",
                    "system_label": "utility and large-load power buildout",
                    "support_provenance_status": "real_only",
                    "supporting_titles": [
                        "Eaton invests $340M in US transformer production"
                    ],
                },
            ]
        },
        {
            "queue_rows": [
                {
                    "canonical_entity_name": "DTE",
                    "system_label": "utility and large-load power buildout",
                    "source_classes": ["trade_press"],
                },
                {
                    "canonical_entity_name": "Synthetic Utility",
                    "system_label": "utility and large-load power buildout",
                    "source_classes": ["company_release"],
                },
                {
                    "canonical_entity_name": "Eaton",
                    "system_label": "utility and large-load power buildout",
                    "source_classes": ["trade_press"],
                },
            ]
        },
    )

    assert batch["metrics"]["narrowed_lane_count"] == 1
    assert batch["metrics"]["narrowed_queue_count"] == 1
    assert batch["narrowed_lanes"][0]["system_label"] == "data center utility response buildout"
    assert batch["queue_rows"][0]["canonical_entity_name"] == "DTE"
    assert batch["queue_rows"][0]["system_label"] == "data center utility response buildout"
