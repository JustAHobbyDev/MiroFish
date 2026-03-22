from app.services.public_market_execution_queue_builder import (
    build_public_market_execution_queue,
)


def test_build_public_market_execution_queue_filters_default_us_executable_rows() -> None:
    batch = build_public_market_execution_queue(
        {
            "policy_rows": [
                {
                    "name": "GE Vernova on grid equipment and transformer buildout",
                    "canonical_entity_name": "GE Vernova",
                    "underlying": "GEV",
                    "market_theme": "grid equipment and transformer buildout",
                    "role_label": "bottleneck_candidate",
                    "final_expression": "shares",
                    "execution_policy_status": "default_us_executable",
                    "execution_policy_action": "use_default_us_execution_path",
                    "ranking_score": 85.39,
                },
                {
                    "name": "Rolls-Royce on data center backup-power equipment buildout",
                    "canonical_entity_name": "Rolls-Royce",
                    "underlying": "RR.",
                    "market_theme": "data center backup-power equipment buildout",
                    "role_label": "supply_chain_beneficiary",
                    "final_expression": "shares",
                    "execution_policy_status": "requires_us_secondary_access_review",
                    "execution_policy_action": "review_secondary_us_listing_before_execution",
                    "ranking_score": 65.29,
                },
            ]
        },
        {
            "rows": [
                {
                    "name": "GE Vernova on grid equipment and transformer buildout",
                    "exchange_scope": "direct_public_market_symbol",
                    "us_accessibility_status": "us_direct_primary",
                }
            ]
        },
        {
            "rows": [
                {
                    "name": "GE Vernova on grid equipment and transformer buildout",
                    "promotion_status": "pick_candidate",
                    "promotion_score_0_to_100": 95.0,
                    "pick_score": 72.89,
                    "mispricing": {"score_0_to_100": 78.0},
                    "stock_fit": {"score_0_to_100": 78.6},
                    "thesis": "GE Vernova bottleneck thesis",
                    "bottleneck_layer": "grid equipment and transformer buildout",
                    "value_capture_layer": "Constrained supplier",
                    "catalysts": ["c1", "c2", "c3", "c4"],
                    "invalidations": ["i1", "i2", "i3", "i4"],
                    "why_missed": ["w1", "w2", "w3", "w4"],
                    "market_data_checks": {"exchange_scope": "direct_public_market_symbol"},
                }
            ]
        },
    )

    assert batch["metrics"]["execution_queue_count"] == 1
    row = batch["queue_rows"][0]
    assert row["canonical_entity_name"] == "GE Vernova"
    assert row["final_expression"] == "shares"
    assert row["top_catalysts"] == ["c1", "c2", "c3"]
