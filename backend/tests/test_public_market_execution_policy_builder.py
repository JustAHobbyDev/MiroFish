from app.services.public_market_execution_policy_builder import (
    build_public_market_execution_policy_batch,
)


def test_build_public_market_execution_policy_batch_is_conservative_by_default() -> None:
    batch = build_public_market_execution_policy_batch(
        {
            "rows": [
                {
                    "name": "GE Vernova on grid equipment and transformer buildout",
                    "canonical_entity_name": "GE Vernova",
                    "underlying": "GEV",
                    "market_theme": "grid equipment and transformer buildout",
                    "role_label": "bottleneck_candidate",
                    "final_expression": "shares",
                    "us_accessibility_status": "us_direct_primary",
                    "ranking_score": 85.39,
                },
                {
                    "name": "Rolls-Royce on data center backup-power equipment buildout",
                    "canonical_entity_name": "Rolls-Royce",
                    "underlying": "RR.",
                    "market_theme": "data center backup-power equipment buildout",
                    "role_label": "supply_chain_beneficiary",
                    "final_expression": "shares",
                    "us_accessibility_status": "foreign_home_with_us_reference",
                    "foreign_access_followup_type": "us_secondary_access_followup",
                    "ranking_score": 65.29,
                },
                {
                    "name": "Hitachi Energy on grid equipment and transformer buildout",
                    "canonical_entity_name": "Hitachi Energy",
                    "underlying": "6501",
                    "market_theme": "grid equipment and transformer buildout",
                    "role_label": "supply_chain_beneficiary",
                    "final_expression": "shares",
                    "us_accessibility_status": "foreign_home_market_only",
                    "foreign_access_followup_type": "home_market_or_proxy_followup",
                    "ranking_score": 65.29,
                },
                {
                    "name": "DTE on data center utility response buildout",
                    "canonical_entity_name": "DTE",
                    "underlying": "DTE",
                    "market_theme": "data center utility response buildout",
                    "role_label": "capacity_response_operator",
                    "final_expression": "reject",
                    "us_accessibility_status": "us_direct_primary",
                    "ranking_score": 53.05,
                },
            ]
        }
    )

    assert batch["metrics"]["default_us_executable_count"] == 1
    assert batch["metrics"]["requires_us_secondary_access_review_count"] == 1
    assert batch["metrics"]["requires_foreign_execution_review_count"] == 1
    assert batch["metrics"]["blocked_by_pick_reject_count"] == 1
