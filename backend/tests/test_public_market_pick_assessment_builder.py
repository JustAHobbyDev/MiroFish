from app.services.public_market_pick_assessment_builder import (
    build_public_market_pick_assessment_batch,
)


def test_build_public_market_pick_assessment_batch_summarizes_by_role_and_expression() -> None:
    batch = build_public_market_pick_assessment_batch(
        {
            "rows": [
                {
                    "name": "GE Vernova on grid equipment and transformer buildout",
                    "underlying": "GEV",
                    "market_theme": "grid equipment and transformer buildout",
                    "promotion_status": "pick_candidate",
                    "final_expression": "shares",
                    "ranking_score": 85.39,
                },
                {
                    "name": "DTE on data center utility response buildout",
                    "underlying": "DTE",
                    "market_theme": "data center utility response buildout",
                    "promotion_status": "watchlist_candidate",
                    "final_expression": "reject",
                    "ranking_score": 53.05,
                },
            ]
        },
        {
            "rows": [
                {
                    "name": "GE Vernova on grid equipment and transformer buildout",
                    "mispricing_type": "hidden_bottleneck",
                    "market_data_checks": {
                        "exchange_scope": "direct_public_market_symbol",
                    },
                },
                {
                    "name": "DTE on data center utility response buildout",
                    "mispricing_type": "capacity_response_operator",
                    "market_data_checks": {
                        "exchange_scope": "direct_public_market_symbol",
                    },
                },
            ]
        },
    )

    assert batch["metrics"]["input_pick_row_count"] == 2
    assert batch["metrics"]["shares_count"] == 1
    assert batch["metrics"]["reject_count"] == 1
    assert batch["role_expression_counts"]["bottleneck_candidate"]["shares"] == 1
    assert batch["role_expression_counts"]["capacity_response_operator"]["reject"] == 1
