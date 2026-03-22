from app.services.public_market_foreign_access_followup_builder import (
    build_public_market_foreign_access_followup_batch,
)


def test_build_public_market_foreign_access_followup_batch_filters_non_us_primary_rows() -> None:
    batch = build_public_market_foreign_access_followup_batch(
        {
            "accessibility_rows": [
                {
                    "name": "GE Vernova on grid equipment and transformer buildout",
                    "canonical_entity_name": "GE Vernova",
                    "underlying": "GEV",
                    "market_theme": "grid equipment and transformer buildout",
                    "final_expression": "shares",
                    "exchange_scope": "direct_public_market_symbol",
                    "us_accessibility_status": "us_direct_primary",
                    "us_reference_present": False,
                },
                {
                    "name": "Rolls-Royce on data center backup-power equipment buildout",
                    "canonical_entity_name": "Rolls-Royce",
                    "underlying": "RR.",
                    "market_theme": "data center backup-power equipment buildout",
                    "final_expression": "shares",
                    "exchange_scope": "foreign_home_market_symbol",
                    "us_accessibility_status": "foreign_home_with_us_reference",
                    "us_reference_present": True,
                },
                {
                    "name": "Hitachi Energy on grid equipment and transformer buildout",
                    "canonical_entity_name": "Hitachi Energy",
                    "underlying": "6501",
                    "market_theme": "grid equipment and transformer buildout",
                    "final_expression": "shares",
                    "exchange_scope": "foreign_home_market_code",
                    "us_accessibility_status": "foreign_home_market_only",
                    "us_reference_present": False,
                },
            ]
        }
    )

    assert batch["metrics"]["followup_count"] == 2
    assert batch["metrics"]["us_secondary_access_followup_count"] == 1
    assert batch["metrics"]["home_market_or_proxy_followup_count"] == 1
    assert batch["followup_rows"][0]["canonical_entity_name"] == "Rolls-Royce"
    assert batch["followup_rows"][0]["followup_type"] == "us_secondary_access_followup"
    assert batch["followup_rows"][1]["canonical_entity_name"] == "Hitachi Energy"
    assert batch["followup_rows"][1]["followup_type"] == "home_market_or_proxy_followup"
