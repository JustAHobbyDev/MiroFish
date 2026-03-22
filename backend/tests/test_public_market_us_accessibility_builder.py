from app.services.public_market_us_accessibility_builder import (
    build_public_market_us_accessibility_batch,
)


def test_build_public_market_us_accessibility_batch_classifies_direct_and_foreign_rows() -> None:
    batch = build_public_market_us_accessibility_batch(
        {
            "rows": [
                {
                    "name": "GE Vernova on grid equipment and transformer buildout",
                    "underlying": "GEV",
                    "market_theme": "grid equipment and transformer buildout",
                    "final_expression": "shares",
                },
                {
                    "name": "Rolls-Royce on data center backup-power equipment buildout",
                    "underlying": "RR.",
                    "market_theme": "data center backup-power equipment buildout",
                    "final_expression": "shares",
                },
                {
                    "name": "Hitachi Energy on grid equipment and transformer buildout",
                    "underlying": "6501",
                    "market_theme": "grid equipment and transformer buildout",
                    "final_expression": "shares",
                },
            ]
        },
        {
            "rows": [
                {
                    "name": "GE Vernova on grid equipment and transformer buildout",
                    "linked_companies": ["GE Vernova"],
                    "market_data_checks": {
                        "exchange_scope": "direct_public_market_symbol",
                    },
                },
                {
                    "name": "Rolls-Royce on data center backup-power equipment buildout",
                    "linked_companies": ["Rolls-Royce"],
                    "market_data_checks": {
                        "exchange_scope": "foreign_home_market_symbol",
                    },
                },
                {
                    "name": "Hitachi Energy on grid equipment and transformer buildout",
                    "linked_companies": ["Hitachi Energy"],
                    "market_data_checks": {
                        "exchange_scope": "foreign_home_market_code",
                    },
                },
            ]
        },
        [
            {
                "symbol_rows": [
                    {
                        "system_label": "data center backup-power equipment buildout",
                        "canonical_entity_name": "Rolls-Royce",
                        "symbol_mapping_basis": "official_company_or_ir_note",
                        "symbol_mapping_evidence": {
                            "note": "Official shareholder information page identifying Rolls-Royce Holdings plc (LSE: RR., ADR: RYCEY)."
                        },
                    },
                    {
                        "system_label": "grid equipment and transformer buildout",
                        "canonical_entity_name": "Hitachi Energy",
                        "symbol_mapping_basis": "official_company_or_ir_note",
                        "symbol_mapping_evidence": {
                            "note": "Official Hitachi stock page identifying Hitachi, Ltd. (TSE: 6501)."
                        },
                    },
                ]
            }
        ],
    )

    assert batch["metrics"]["input_pick_row_count"] == 3
    assert batch["metrics"]["us_direct_primary_count"] == 1
    assert batch["metrics"]["foreign_home_with_us_reference_count"] == 1
    assert batch["metrics"]["foreign_home_market_only_count"] == 1

    rows = {row["canonical_entity_name"]: row for row in batch["accessibility_rows"]}
    assert rows["GE Vernova"]["us_accessibility_status"] == "us_direct_primary"
    assert rows["Rolls-Royce"]["us_accessibility_status"] == "foreign_home_with_us_reference"
    assert rows["Hitachi Energy"]["us_accessibility_status"] == "foreign_home_market_only"
