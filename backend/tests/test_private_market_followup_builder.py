from app.services.private_market_followup_builder import build_private_market_followup_batch


def test_build_private_market_followup_batch_keeps_supplier_and_capacity_private_paths_distinct() -> None:
    batch = build_private_market_followup_batch(
        {
            "handoff_rows": [
                {
                    "canonical_entity_name": "AVL",
                    "resolved_issuer_name": "AVL List GmbH",
                    "system_label": "backup lane",
                    "entity_role": "equipment_or_component_supplier",
                    "role_lane": "equipment_supplier",
                    "support_route_type": "private_company",
                    "market_handoff_status": "supplier_chain_followup",
                    "route_aware_priority_score": 80,
                    "route_aware_priority_tier": "high",
                },
                {
                    "canonical_entity_name": "CyrusOne",
                    "resolved_issuer_name": "CyrusOne",
                    "system_label": "utility lane",
                    "entity_role": "capacity_operator_or_owner",
                    "role_lane": "utility_or_operator",
                    "support_route_type": "private_company",
                    "market_handoff_status": "private_watchlist_only",
                    "route_aware_priority_score": 70,
                    "route_aware_priority_tier": "high",
                },
            ]
        }
    )

    assert batch["metrics"]["private_followup_count"] == 2
    avl = next(row for row in batch["followup_rows"] if row["canonical_entity_name"] == "AVL")
    assert avl["private_followup_status"] == "private_supplier_chain_followup"

    cyrus = next(row for row in batch["followup_rows"] if row["canonical_entity_name"] == "CyrusOne")
    assert cyrus["private_followup_status"] == "private_capacity_watchlist_followup"

