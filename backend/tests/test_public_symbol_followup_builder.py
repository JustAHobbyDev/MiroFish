from app.services.public_symbol_followup_builder import build_public_symbol_followup_batch


def test_build_public_symbol_followup_batch_splits_foreign_and_parent_routes() -> None:
    batch = build_public_symbol_followup_batch(
        [
            {
                "symbol_rows": [
                    {
                        "system_label": "backup power",
                        "canonical_entity_name": "Rolls-Royce",
                        "resolved_issuer_name": "Rolls-Royce Holdings plc",
                        "exchange_scope": "foreign_public_route_unmapped",
                        "symbol_mapping_status": "public_symbol_followup_required_foreign_route",
                        "filing_route_assessment": "rolls_royce_ir",
                        "live_resolution_status": "resolved_direct_foreign_public_route",
                        "route_aware_priority_score": 98,
                    }
                ]
            },
            {
                "symbol_rows": [
                    {
                        "system_label": "transformers",
                        "canonical_entity_name": "Hitachi Energy",
                        "resolved_issuer_name": "Hitachi, Ltd.",
                        "exchange_scope": "public_route_unmapped",
                        "symbol_mapping_status": "public_symbol_followup_required",
                        "filing_route_assessment": "hitachi_ir_and_edinet",
                        "live_resolution_status": "resolved_parent_route",
                        "route_aware_priority_score": 112,
                    }
                ]
            },
        ]
    )

    assert batch["metrics"]["input_symbol_row_count"] == 2
    assert batch["metrics"]["followup_count"] == 2
    assert batch["followup_rows"][0]["followup_type"] == "foreign_public_symbol_followup"
    assert batch["followup_rows"][1]["followup_type"] == "parent_public_symbol_followup"
