from app.services.public_market_research_row_builder import build_public_market_research_row_batch


def test_build_public_market_research_row_batch_attaches_role_labels() -> None:
    batch = build_public_market_research_row_batch(
        symbol_mapping_batches=[
            {
                "symbol_rows": [
                    {
                        "system_label": "grid lane",
                        "canonical_entity_name": "Grid Co",
                        "resolved_issuer_name": "Grid Co Inc.",
                        "mapped_public_symbol": "GRID",
                        "exchange_scope": "direct_public_market_symbol",
                        "symbol_mapping_status": "mapped_public_symbol",
                        "market_expression_scope": "public_supplier_expression",
                        "route_aware_priority_score": 90,
                    },
                    {
                        "system_label": "utility lane",
                        "canonical_entity_name": "Utility Co",
                        "resolved_issuer_name": "Utility Co",
                        "mapped_public_symbol": "",
                        "exchange_scope": "foreign_public_route_unmapped",
                        "symbol_mapping_status": "public_symbol_followup_required_foreign_route",
                        "market_expression_scope": "public_operator_expression",
                        "route_aware_priority_score": 80,
                    },
                ]
            }
        ],
        bottleneck_classification_batches=[
            {
                "classification_rows": [
                    {
                        "system_label": "grid lane",
                        "canonical_entity_name": "Grid Co",
                        "bottleneck_role_label": "bottleneck_candidate",
                        "classification_reason": "strict bottleneck evidence",
                    },
                    {
                        "system_label": "utility lane",
                        "canonical_entity_name": "Utility Co",
                        "bottleneck_role_label": "capacity_response_operator",
                        "classification_reason": "response evidence",
                    },
                ]
            }
        ],
    )

    grid = next(row for row in batch["research_rows"] if row["canonical_entity_name"] == "Grid Co")
    assert grid["market_research_row_status"] == "ready_for_market_research"
    assert grid["market_research_row_action"] == "build_bottleneck_market_research_row"

    utility = next(row for row in batch["research_rows"] if row["canonical_entity_name"] == "Utility Co")
    assert utility["market_research_row_status"] == "symbol_followup_required_before_market_research"
    assert utility["bottleneck_role_label"] == "capacity_response_operator"

