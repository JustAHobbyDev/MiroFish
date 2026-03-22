from app.services.public_market_foreign_execution_handoff_builder import (
    build_public_market_foreign_execution_handoff,
)


def test_build_public_market_foreign_execution_handoff_keeps_priority_and_actions() -> None:
    batch = build_public_market_foreign_execution_handoff(
        {
            "handoff_rows": [
                {
                    "name": "Rolls-Royce on data center backup-power equipment buildout",
                    "canonical_entity_name": "Rolls-Royce",
                    "underlying": "RR.",
                    "market_theme": "data center backup-power equipment buildout",
                    "role_label": "supply_chain_beneficiary",
                    "foreign_review_priority": "highest",
                    "followup_type": "us_secondary_access_followup",
                    "followup_action": "confirm_adr_or_otc_symbol_and_check_basic_liquidity",
                    "exchange_scope": "foreign_home_market_symbol",
                    "us_accessibility_status": "foreign_home_with_us_reference",
                    "final_expression": "shares",
                    "ranking_score": 65.29,
                    "thesis": "Rolls supplier thesis",
                    "bottleneck_layer": "backup power",
                    "value_capture_layer": "Supplier",
                    "top_catalysts": ["c1"],
                    "top_invalidations": ["i1"],
                    "why_missed": ["w1"],
                    "symbol_mapping_basis": "official_company_or_ir_note",
                    "symbol_mapping_evidence": {"note": "ADR reference present"},
                }
            ]
        }
    )

    assert batch["metrics"]["handoff_count"] == 1
    assert batch["handoff_rows"][0]["canonical_entity_name"] == "Rolls-Royce"
    assert batch["handoff_rows"][0]["followup_action"] == "confirm_adr_or_otc_symbol_and_check_basic_liquidity"
