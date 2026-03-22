from app.services.public_market_execution_handoff_builder import (
    build_public_market_execution_handoff,
)


def test_build_public_market_execution_handoff_builds_prioritized_rows() -> None:
    batch = build_public_market_execution_handoff(
        {
            "queue_rows": [
                {
                    "name": "GE Vernova on grid equipment and transformer buildout",
                    "canonical_entity_name": "GE Vernova",
                    "underlying": "GEV",
                    "market_theme": "grid equipment and transformer buildout",
                    "role_label": "bottleneck_candidate",
                    "final_expression": "shares",
                    "execution_policy_action": "use_default_us_execution_path",
                    "ranking_score": 85.39,
                    "promotion_status": "pick_candidate",
                    "mispricing_score_0_to_100": 78.0,
                    "stock_fit_score_0_to_100": 78.6,
                    "thesis": "GE Vernova bottleneck thesis",
                    "bottleneck_layer": "grid equipment and transformer buildout",
                    "value_capture_layer": "Constrained supplier",
                    "top_catalysts": ["c1", "c2"],
                    "top_invalidations": ["i1", "i2"],
                    "why_missed": ["w1", "w2"],
                },
                {
                    "name": "Eaton on grid equipment and transformer buildout",
                    "canonical_entity_name": "Eaton",
                    "underlying": "ETN",
                    "market_theme": "grid equipment and transformer buildout",
                    "role_label": "supply_chain_beneficiary",
                    "final_expression": "shares",
                    "execution_policy_action": "use_default_us_execution_path",
                    "ranking_score": 66.0,
                    "promotion_status": "watchlist_candidate",
                    "mispricing_score_0_to_100": 62.0,
                    "stock_fit_score_0_to_100": 78.0,
                    "thesis": "Eaton supplier thesis",
                    "bottleneck_layer": "grid equipment and transformer buildout",
                    "value_capture_layer": "Supplier",
                    "top_catalysts": ["c1"],
                    "top_invalidations": ["i1"],
                    "why_missed": ["w1"],
                },
            ]
        }
    )

    assert batch["metrics"]["handoff_count"] == 2
    assert batch["metrics"]["highest_priority_count"] == 1
    assert batch["handoff_rows"][0]["canonical_entity_name"] == "GE Vernova"
    assert batch["handoff_rows"][0]["execution_priority"] == "highest"
