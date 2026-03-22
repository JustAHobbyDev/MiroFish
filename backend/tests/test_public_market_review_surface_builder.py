from app.services.public_market_review_surface_builder import (
    build_public_market_review_surface,
)


def test_build_public_market_review_surface_combines_pick_access_and_followup() -> None:
    batch = build_public_market_review_surface(
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
                    "name": "Rolls-Royce on data center backup-power equipment buildout",
                    "underlying": "RR.",
                    "market_theme": "data center backup-power equipment buildout",
                    "promotion_status": "watchlist_candidate",
                    "final_expression": "shares",
                    "ranking_score": 65.29,
                },
            ]
        },
        {
            "assessment_rows": [
                {
                    "name": "GE Vernova on grid equipment and transformer buildout",
                    "role_label": "bottleneck_candidate",
                },
                {
                    "name": "Rolls-Royce on data center backup-power equipment buildout",
                    "role_label": "supply_chain_beneficiary",
                },
            ]
        },
        {
            "accessibility_rows": [
                {
                    "name": "GE Vernova on grid equipment and transformer buildout",
                    "canonical_entity_name": "GE Vernova",
                    "exchange_scope": "direct_public_market_symbol",
                    "us_accessibility_status": "us_direct_primary",
                    "us_accessibility_action": "use_direct_us_symbol",
                    "us_reference_present": False,
                },
                {
                    "name": "Rolls-Royce on data center backup-power equipment buildout",
                    "canonical_entity_name": "Rolls-Royce",
                    "exchange_scope": "foreign_home_market_symbol",
                    "us_accessibility_status": "foreign_home_with_us_reference",
                    "us_accessibility_action": "verify_adr_or_otc_liquidity_before_us_expression",
                    "us_reference_present": True,
                },
            ]
        },
        {
            "followup_rows": [
                {
                    "name": "Rolls-Royce on data center backup-power equipment buildout",
                    "followup_type": "us_secondary_access_followup",
                    "followup_action": "confirm_adr_or_otc_symbol_and_check_basic_liquidity",
                }
            ]
        },
    )

    assert batch["metrics"]["review_row_count"] == 2
    assert batch["metrics"]["foreign_access_followup_count"] == 1
    rr = next(row for row in batch["rows"] if row["name"].startswith("Rolls-Royce"))
    assert rr["foreign_access_followup_type"] == "us_secondary_access_followup"

