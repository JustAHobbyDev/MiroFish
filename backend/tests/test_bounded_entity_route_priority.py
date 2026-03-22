from app.services.bounded_entity_route_priority import build_bounded_entity_route_priority_batch


def test_build_bounded_entity_route_priority_batch_keeps_public_and_private_distinct() -> None:
    batch = build_bounded_entity_route_priority_batch(
        {
            "support_rows": [
                {
                    "canonical_entity_name": "Public Supplier",
                    "system_label": "backup power",
                    "priority_tier": "high",
                    "entity_role": "equipment_or_component_supplier",
                    "role_lane": "equipment_supplier",
                    "support_status": "supported_public_filing",
                    "support_route_type": "public_filing",
                    "route_assessment": "annual_report_route",
                    "support_strong_evidence_item_count": 4,
                    "support_component_specific_count": 2,
                    "support_pressure_or_capacity_count": 1,
                    "support_expansion_or_capex_count": 1,
                    "support_financing_or_capital_count": 0,
                    "role_specific_evidence_summary": {},
                },
                {
                    "canonical_entity_name": "Private Operator",
                    "system_label": "utility lane",
                    "priority_tier": "medium",
                    "entity_role": "capacity_operator_or_owner",
                    "role_lane": "utility_or_operator",
                    "support_status": "supported_private_company",
                    "support_route_type": "private_company",
                    "route_assessment": "private_company_official_company_route",
                    "support_strong_evidence_item_count": 3,
                    "support_component_specific_count": 0,
                    "support_pressure_or_capacity_count": 2,
                    "support_expansion_or_capex_count": 1,
                    "support_financing_or_capital_count": 1,
                    "role_specific_evidence_summary": {
                        "load_and_demand_signal_count": 2,
                        "grid_response_signal_count": 1,
                        "capex_response_signal_count": 2,
                    },
                },
            ]
        }
    )

    assert batch["metrics"]["supported_public_count"] == 1
    assert batch["metrics"]["supported_private_count"] == 1
    assert batch["priority_rows"][0]["selection_action"] == "advance_with_public_filing_weight"
    private_row = next(row for row in batch["priority_rows"] if row["canonical_entity_name"] == "Private Operator")
    assert private_row["selection_action"] == "advance_with_private_company_weight"
    assert private_row["route_aware_priority_tier"] in {"medium", "high"}
