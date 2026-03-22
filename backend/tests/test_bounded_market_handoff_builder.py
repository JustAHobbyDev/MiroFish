from app.services.bounded_market_handoff_builder import build_bounded_market_handoff_batch


def test_build_bounded_market_handoff_batch_preserves_public_private_boundary() -> None:
    batch = build_bounded_market_handoff_batch(
        {
            "rows": [
                {
                    "system_label": "backup power",
                    "canonical_entity_name": "Public Supplier",
                    "resolved_issuer_name": "Public Supplier plc",
                    "entity_role": "equipment_or_component_supplier",
                    "role_lane": "equipment_supplier",
                    "support_route_type": "public_filing",
                    "support_status": "supported_public_filing",
                    "route_assessment": "annual_report_route",
                    "route_aware_priority_score": 90,
                    "route_aware_priority_tier": "high",
                    "selection_action": "advance_with_public_filing_weight",
                    "source_classes": ["trade_press"],
                    "top_support_evidence_items": [],
                },
                {
                    "system_label": "backup power",
                    "canonical_entity_name": "Private Supplier",
                    "resolved_issuer_name": "Private Supplier GmbH",
                    "entity_role": "equipment_or_component_supplier",
                    "role_lane": "equipment_supplier",
                    "support_route_type": "private_company",
                    "support_status": "supported_private_company",
                    "route_assessment": "private_company",
                    "route_aware_priority_score": 80,
                    "route_aware_priority_tier": "high",
                    "selection_action": "advance_with_private_company_weight",
                    "source_classes": ["trade_press"],
                    "top_support_evidence_items": [],
                },
                {
                    "system_label": "utility response",
                    "canonical_entity_name": "Private Operator",
                    "resolved_issuer_name": "Private Operator LLC",
                    "entity_role": "capacity_operator_or_owner",
                    "role_lane": "utility_or_operator",
                    "support_route_type": "private_company",
                    "support_status": "supported_private_company",
                    "route_assessment": "private_company",
                    "route_aware_priority_score": 75,
                    "route_aware_priority_tier": "high",
                    "selection_action": "advance_with_private_company_weight",
                    "source_classes": ["trade_press"],
                    "top_support_evidence_items": [],
                },
                {
                    "system_label": "utility response",
                    "canonical_entity_name": "Unresolved Utility",
                    "resolved_issuer_name": "",
                    "entity_role": "capacity_operator_or_owner",
                    "role_lane": "utility_or_operator",
                    "support_route_type": "",
                    "support_status": "needs_live_resolution",
                    "route_assessment": "",
                    "route_aware_priority_score": 40,
                    "route_aware_priority_tier": "medium",
                    "selection_action": "resolve_issuer_and_collect_filing_route",
                    "source_classes": ["trade_press"],
                    "top_support_evidence_items": [],
                },
            ]
        }
    )

    assert batch["metrics"]["public_investable_now_count"] == 1
    assert batch["metrics"]["supplier_chain_followup_count"] == 1
    assert batch["metrics"]["private_watchlist_only_count"] == 1
    assert batch["metrics"]["hold_for_more_corroboration_count"] == 1

    public_row = next(
        row for row in batch["handoff_rows"] if row["canonical_entity_name"] == "Public Supplier"
    )
    assert public_row["market_handoff_status"] == "public_investable_now"
    assert public_row["ticker_handoff_status"] == "eligible_for_public_symbol_mapping"

    private_supplier = next(
        row for row in batch["handoff_rows"] if row["canonical_entity_name"] == "Private Supplier"
    )
    assert private_supplier["market_handoff_status"] == "supplier_chain_followup"
    assert private_supplier["ticker_handoff_status"] == "blocked_private_route"

    private_operator = next(
        row for row in batch["handoff_rows"] if row["canonical_entity_name"] == "Private Operator"
    )
    assert private_operator["market_handoff_status"] == "private_watchlist_only"

    unresolved_row = next(
        row for row in batch["handoff_rows"] if row["canonical_entity_name"] == "Unresolved Utility"
    )
    assert unresolved_row["market_handoff_status"] == "hold_for_more_corroboration"
    assert unresolved_row["ticker_handoff_block_reason"] == "issuer_route_not_resolved"
