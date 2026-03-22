from app.services.bounded_entity_route_review_surface_builder import (
    build_bounded_entity_route_review_surface,
)


def test_build_bounded_entity_route_review_surface_groups_by_lane() -> None:
    batch = build_bounded_entity_route_review_surface(
        [
            {
                "name": "utility_priority",
                "priority_rows": [
                    {
                        "system_label": "utility lane",
                        "canonical_entity_name": "Public Utility",
                        "resolved_issuer_name": "Public Utility Inc.",
                        "entity_role": "capacity_operator_or_owner",
                        "role_lane": "utility_or_operator",
                        "priority_tier": "medium",
                        "support_route_type": "public_filing",
                        "support_status": "supported_public_filing",
                        "route_assessment": "sec_route",
                        "route_aware_priority_score": 80,
                        "route_aware_priority_tier": "high",
                        "selection_action": "advance_with_public_filing_weight",
                        "support_evidence_item_count": 8,
                        "support_strong_evidence_item_count": 6,
                        "support_component_specific_count": 2,
                        "support_pressure_or_capacity_count": 2,
                        "support_expansion_or_capex_count": 1,
                        "support_financing_or_capital_count": 0,
                        "role_specific_evidence_summary": {"load_and_demand_signal_count": 3},
                        "source_classes": ["trade_press"],
                        "top_support_evidence_items": [],
                    }
                ],
            },
            {
                "name": "backup_priority",
                "priority_rows": [
                    {
                        "system_label": "backup lane",
                        "canonical_entity_name": "Private Backup Co",
                        "resolved_issuer_name": "Private Backup Co GmbH",
                        "entity_role": "equipment_or_component_supplier",
                        "role_lane": "equipment_supplier",
                        "priority_tier": "high",
                        "support_route_type": "private_company",
                        "support_status": "supported_private_company",
                        "route_assessment": "private_company",
                        "route_aware_priority_score": 70,
                        "route_aware_priority_tier": "high",
                        "selection_action": "advance_with_private_company_weight",
                        "support_evidence_item_count": 5,
                        "support_strong_evidence_item_count": 5,
                        "support_component_specific_count": 2,
                        "support_pressure_or_capacity_count": 1,
                        "support_expansion_or_capex_count": 1,
                        "support_financing_or_capital_count": 0,
                        "role_specific_evidence_summary": {},
                        "source_classes": ["trade_press"],
                        "top_support_evidence_items": [],
                    }
                ],
            },
        ]
    )

    assert batch["metrics"]["input_priority_batch_count"] == 2
    assert batch["metrics"]["supported_public_count"] == 1
    assert batch["metrics"]["supported_private_count"] == 1
    assert len(batch["rows_by_lane"]["utility lane"]) == 1
    assert len(batch["rows_by_lane"]["backup lane"]) == 1
