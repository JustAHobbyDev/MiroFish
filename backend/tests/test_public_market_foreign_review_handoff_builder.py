from app.services.public_market_foreign_review_handoff_builder import (
    build_public_market_foreign_review_handoff,
)


def test_build_public_market_foreign_review_handoff_builds_priority_queue() -> None:
    batch = build_public_market_foreign_review_handoff(
        {
            "followup_rows": [
                {
                    "name": "Rolls-Royce on data center backup-power equipment buildout",
                    "canonical_entity_name": "Rolls-Royce",
                    "underlying": "RR.",
                    "market_theme": "data center backup-power equipment buildout",
                    "final_expression": "shares",
                    "exchange_scope": "foreign_home_market_symbol",
                    "us_accessibility_status": "foreign_home_with_us_reference",
                    "followup_type": "us_secondary_access_followup",
                    "followup_action": "confirm_adr_or_otc_symbol_and_check_basic_liquidity",
                    "us_reference_present": True,
                    "symbol_mapping_basis": "official_company_or_ir_note",
                    "symbol_mapping_evidence": {"note": "ADR reference present"},
                },
                {
                    "name": "Hitachi Energy on grid equipment and transformer buildout",
                    "canonical_entity_name": "Hitachi Energy",
                    "underlying": "6501",
                    "market_theme": "grid equipment and transformer buildout",
                    "final_expression": "shares",
                    "exchange_scope": "foreign_home_market_code",
                    "us_accessibility_status": "foreign_home_market_only",
                    "followup_type": "home_market_or_proxy_followup",
                    "followup_action": "decide_home_market_execution_or_find_us_proxy_expression",
                    "us_reference_present": False,
                    "symbol_mapping_basis": "official_company_or_ir_note",
                    "symbol_mapping_evidence": {"note": "TSE code"},
                },
            ]
        },
        {
            "rows": [
                {
                    "name": "Rolls-Royce on data center backup-power equipment buildout",
                    "role_label": "supply_chain_beneficiary",
                    "ranking_score": 65.29,
                },
                {
                    "name": "Hitachi Energy on grid equipment and transformer buildout",
                    "role_label": "supply_chain_beneficiary",
                    "ranking_score": 65.29,
                },
            ]
        },
        {
            "rows": [
                {
                    "name": "Rolls-Royce on data center backup-power equipment buildout",
                    "thesis": "Rolls supplier thesis",
                    "bottleneck_layer": "backup power",
                    "value_capture_layer": "Supplier",
                    "catalysts": ["c1", "c2"],
                    "invalidations": ["i1", "i2"],
                    "why_missed": ["w1", "w2"],
                },
                {
                    "name": "Hitachi Energy on grid equipment and transformer buildout",
                    "thesis": "Hitachi supplier thesis",
                    "bottleneck_layer": "transformers",
                    "value_capture_layer": "Supplier",
                    "catalysts": ["c1"],
                    "invalidations": ["i1"],
                    "why_missed": ["w1"],
                },
            ]
        },
    )

    assert batch["metrics"]["handoff_count"] == 2
    assert batch["metrics"]["highest_priority_count"] == 1
    assert batch["handoff_rows"][0]["canonical_entity_name"] == "Rolls-Royce"
    assert batch["handoff_rows"][0]["foreign_review_priority"] == "highest"
