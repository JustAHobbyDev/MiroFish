from app.services.public_market_symbol_mapper import build_public_market_symbol_mapping_batch


def test_build_public_market_symbol_mapping_batch_maps_sec_and_foreign_symbols() -> None:
    batch = build_public_market_symbol_mapping_batch(
        {
            "handoff_rows": [
                {
                    "canonical_entity_name": "FirstEnergy",
                    "resolved_issuer_name": "FirstEnergy Corp.",
                    "system_label": "utility lane",
                    "market_handoff_status": "public_investable_now",
                    "market_expression_scope": "public_operator_expression",
                    "route_assessment": "firstenergy_sec_edgar",
                    "route_aware_priority_score": 90,
                },
                {
                    "canonical_entity_name": "Mitsubishi Electric",
                    "resolved_issuer_name": "Mitsubishi Electric Corporation",
                    "system_label": "transformer lane",
                    "market_handoff_status": "public_investable_now",
                    "market_expression_scope": "public_supplier_expression",
                    "route_assessment": "mitsubishi_electric_ir",
                    "route_aware_priority_score": 80,
                },
                {
                    "canonical_entity_name": "Rolls-Royce",
                    "resolved_issuer_name": "Rolls-Royce Holdings plc",
                    "system_label": "backup lane",
                    "market_handoff_status": "public_investable_now",
                    "market_expression_scope": "public_supplier_expression",
                    "route_assessment": "rolls_royce_ir",
                    "route_aware_priority_score": 70,
                },
            ]
        },
        issuer_resolution_batches=[
            {
                "results": [
                    {
                        "canonical_entity_name": "FirstEnergy",
                        "live_resolution_status": "resolved_direct_public_route",
                        "filing_route_assessment": "firstenergy_sec_edgar",
                        "evidence": [
                            {
                                "source_url": "https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=FE&type=10-k",
                                "note": "Official SEC lookup",
                            }
                        ],
                    },
                    {
                        "canonical_entity_name": "Mitsubishi Electric",
                        "live_resolution_status": "resolved_direct_foreign_public_route",
                        "filing_route_assessment": "mitsubishi_electric_ir",
                        "evidence": [
                            {
                                "source_url": "https://example.com/ir",
                                "note": "Official Mitsubishi Electric stock information page showing Tokyo Stock Exchange stock code 6503.",
                            }
                        ],
                    },
                    {
                        "canonical_entity_name": "Rolls-Royce",
                        "live_resolution_status": "resolved_direct_foreign_public_route",
                        "filing_route_assessment": "rolls_royce_ir",
                        "evidence": [
                            {
                                "source_url": "https://example.com/rr",
                                "note": "Official annual report PDF hosted on rolls-royce.com.",
                            }
                        ],
                    },
                ]
            }
        ],
        filing_collection_batches=[],
    )

    firstenergy = next(row for row in batch["symbol_rows"] if row["canonical_entity_name"] == "FirstEnergy")
    assert firstenergy["mapped_public_symbol"] == "FE"
    assert firstenergy["symbol_mapping_status"] == "mapped_public_symbol"

    melec = next(row for row in batch["symbol_rows"] if row["canonical_entity_name"] == "Mitsubishi Electric")
    assert melec["mapped_public_symbol"] == "6503"
    assert melec["symbol_mapping_status"] == "mapped_foreign_public_symbol"

    rr = next(row for row in batch["symbol_rows"] if row["canonical_entity_name"] == "Rolls-Royce")
    assert rr["symbol_mapping_status"] == "public_symbol_followup_required_foreign_route"

