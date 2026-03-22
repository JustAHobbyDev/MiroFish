from app.services.public_symbol_followup_resolution_builder import (
    build_public_symbol_followup_resolution_batch,
)


def test_build_public_symbol_followup_resolution_batch_maps_parent_and_foreign_rows() -> None:
    batch = build_public_symbol_followup_resolution_batch(
        {
            "followup_rows": [
                {
                    "system_label": "data center backup-power equipment buildout",
                    "canonical_entity_name": "Rolls-Royce",
                    "resolved_issuer_name": "Rolls-Royce Holdings plc",
                    "followup_type": "foreign_public_symbol_followup",
                    "filing_route_assessment": "rolls_royce_ir_and_annual_report_route",
                    "live_resolution_status": "resolved_direct_foreign_public_route",
                    "route_aware_priority_score": 98,
                },
                {
                    "system_label": "grid equipment and transformer buildout",
                    "canonical_entity_name": "Hitachi Energy",
                    "resolved_issuer_name": "Hitachi, Ltd.",
                    "followup_type": "parent_public_symbol_followup",
                    "filing_route_assessment": "hitachi_ir_and_edinet",
                    "live_resolution_status": "resolved_parent_route",
                    "route_aware_priority_score": 112,
                },
            ]
        },
        {
            "resolution_inputs": [
                {
                    "canonical_entity_name": "Rolls-Royce",
                    "resolved_issuer_name": "Rolls-Royce Holdings plc",
                    "mapped_public_symbol": "RR.",
                    "exchange_scope": "foreign_home_market_symbol",
                    "symbol_mapping_basis": "official_company_or_ir_note",
                    "symbol_mapping_evidence": {
                        "source_url": "https://www.rolls-royce.com/investors/shareholder-information.aspx",
                        "note": "Official shareholder information page identifying Rolls-Royce Holdings plc (LSE: RR., ADR: RYCEY).",
                    },
                },
                {
                    "canonical_entity_name": "Hitachi Energy",
                    "resolved_issuer_name": "Hitachi, Ltd.",
                    "mapped_public_symbol": "6501",
                    "exchange_scope": "foreign_home_market_code",
                    "symbol_mapping_basis": "official_company_or_ir_note",
                    "symbol_mapping_evidence": {
                        "source_url": "https://www.hitachi.com/IR-e/stock/index.html",
                        "note": "Official Hitachi stock page identifying Hitachi, Ltd. (TSE: 6501).",
                    },
                },
            ]
        },
    )

    assert batch["metrics"]["resolved_symbol_row_count"] == 2
    assert batch["symbol_rows"][0]["mapped_public_symbol"] == "RR."
    assert batch["symbol_rows"][0]["symbol_mapping_status"] == "mapped_foreign_public_symbol"
    assert batch["symbol_rows"][1]["mapped_public_symbol"] == "6501"
    assert batch["symbol_rows"][1]["symbol_mapping_status"] == "mapped_foreign_public_symbol"
