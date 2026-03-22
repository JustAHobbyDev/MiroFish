from app.services.structural_pressure_narrower import build_structural_pressure_narrowing_batch


def test_build_structural_pressure_narrowing_batch_creates_backup_power_lane() -> None:
    result = build_structural_pressure_narrowing_batch(
        {
            "candidates": [
                {
                    "pressure_candidate_id": "spc_backup",
                    "system_label": "power generation and backup equipment buildout",
                    "as_of_date": "2025-12-02",
                    "supporting_capital_flow_cluster_ids": ["cluster_backup"],
                }
            ]
        },
        {
            "clusters": [
                {
                    "capital_flow_cluster_id": "cluster_backup",
                    "supporting_capital_flow_signal_ids": [
                        "a1:capital:0",
                        "a2:capital:0",
                    ],
                }
            ]
        },
        {
            "kept_artifacts": [
                {
                    "artifact_id": "a1",
                    "source_class": "company_release",
                    "title": "PrimeForge Power to expand generator package factory for data center and utility resilience demand",
                    "source_url": "https://www.manufacturingdive.com/news/example-real-one",
                },
                {
                    "artifact_id": "a2",
                    "source_class": "trade_press",
                    "title": "Power enclosure maker AVL to establish its first US plant",
                    "source_url": "https://www.manufacturingdive.com/news/example-real-two",
                },
            ],
            "review_artifacts": [],
        },
    )

    assert result["metrics"]["narrowed_candidate_count"] == 1
    candidate = result["narrowed_candidates"][0]
    assert candidate["system_label"] == "data center backup-power equipment buildout"
    assert candidate["narrowing_basis"]["matched_artifact_count"] == 2
    assert candidate["narrowing_basis"]["support_provenance_status"] == "real_only"


def test_build_structural_pressure_narrowing_batch_skips_synthetic_only_support() -> None:
    result = build_structural_pressure_narrowing_batch(
        {
            "candidates": [
                {
                    "pressure_candidate_id": "spc_backup",
                    "system_label": "power generation and backup equipment buildout",
                    "as_of_date": "2025-12-02",
                    "supporting_capital_flow_cluster_ids": ["cluster_backup"],
                }
            ]
        },
        {
            "clusters": [
                {
                    "capital_flow_cluster_id": "cluster_backup",
                    "supporting_capital_flow_signal_ids": [
                        "a1:capital:0",
                        "a2:capital:0",
                    ],
                }
            ]
        },
        {
            "kept_artifacts": [
                {
                    "artifact_id": "a1",
                    "source_class": "company_release",
                    "title": "PrimeForge Power to expand generator package factory for data center and utility resilience demand",
                    "source_url": "https://example.com/releases/example-one",
                },
                {
                    "artifact_id": "a2",
                    "source_class": "company_release",
                    "title": "PeakSpan Power Systems expands generator module assembly for utility and data center demand",
                    "source_url": "https://example.com/releases/example-two",
                },
            ],
            "review_artifacts": [],
        },
    )

    assert result["metrics"]["narrowed_candidate_count"] == 0
