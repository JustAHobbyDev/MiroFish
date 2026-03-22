from app.services.public_market_scan_candidate_builder import (
    build_public_market_scan_candidate_batch,
)


def test_build_public_market_scan_candidate_batch_emits_ready_rows_only() -> None:
    batch = build_public_market_scan_candidate_batch(
        {
            "research_rows": [
                {
                    "system_label": "grid equipment and transformer buildout",
                    "canonical_entity_name": "GE Vernova",
                    "resolved_issuer_name": "GE Vernova Inc.",
                    "mapped_public_symbol": "GEV",
                    "exchange_scope": "direct_public_market_symbol",
                    "symbol_mapping_status": "mapped_public_symbol",
                    "market_expression_scope": "public_supplier_expression",
                    "bottleneck_role_label": "bottleneck_candidate",
                    "classification_reason": "strict bottleneck evidence",
                    "market_research_row_status": "ready_for_market_research",
                    "market_research_row_action": "build_bottleneck_market_research_row",
                    "route_aware_priority_score": 95,
                },
                {
                    "system_label": "backup power",
                    "canonical_entity_name": "Rolls-Royce",
                    "resolved_issuer_name": "Rolls-Royce Holdings plc",
                    "mapped_public_symbol": "",
                    "exchange_scope": "foreign_public_route_unmapped",
                    "symbol_mapping_status": "public_symbol_followup_required_foreign_route",
                    "market_expression_scope": "public_supplier_expression",
                    "bottleneck_role_label": "supply_chain_beneficiary",
                    "classification_reason": "beneficiary only",
                    "market_research_row_status": "symbol_followup_required_before_market_research",
                    "market_research_row_action": "resolve_public_symbol_before_market_research_row",
                    "route_aware_priority_score": 80,
                },
            ]
        }
    )

    assert batch["metrics"]["ready_market_scan_candidate_count"] == 1
    row = batch["rows"][0]
    assert row["underlying"] == "GEV"
    assert row["promotion_status"] == "pick_candidate"

