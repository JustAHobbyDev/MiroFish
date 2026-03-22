from app.services.bottleneck_role_classifier import build_bottleneck_role_classification_batch


def test_build_bottleneck_role_classification_batch_keeps_strict_boundary() -> None:
    batch = build_bottleneck_role_classification_batch(
        {
            "rows": [
                {
                    "system_label": "grid equipment and transformer buildout",
                    "canonical_entity_name": "Transformer Co",
                    "resolved_issuer_name": "Transformer Co Inc.",
                    "entity_role": "equipment_or_component_supplier",
                    "role_lane": "equipment_supplier",
                    "support_route_type": "public_filing",
                    "support_status": "supported_public_filing",
                    "route_aware_priority_score": 95,
                    "support_strong_evidence_item_count": 10,
                    "support_component_specific_count": 4,
                    "support_pressure_or_capacity_count": 2,
                    "support_expansion_or_capex_count": 3,
                    "source_classes": ["trade_press"],
                    "top_support_evidence_items": [],
                },
                {
                    "system_label": "utility response",
                    "canonical_entity_name": "Utility Co",
                    "resolved_issuer_name": "Utility Co",
                    "entity_role": "capacity_operator_or_owner",
                    "role_lane": "utility_or_operator",
                    "support_route_type": "public_filing",
                    "support_status": "supported_public_filing",
                    "route_aware_priority_score": 80,
                    "support_strong_evidence_item_count": 8,
                    "support_component_specific_count": 1,
                    "support_pressure_or_capacity_count": 4,
                    "support_expansion_or_capex_count": 2,
                    "source_classes": ["trade_press"],
                    "top_support_evidence_items": [],
                },
                {
                    "system_label": "data center backup-power equipment buildout",
                    "canonical_entity_name": "Backup Co",
                    "resolved_issuer_name": "Backup Co Ltd.",
                    "entity_role": "equipment_or_component_supplier",
                    "role_lane": "equipment_supplier",
                    "support_route_type": "public_filing",
                    "support_status": "supported_public_filing",
                    "route_aware_priority_score": 70,
                    "support_strong_evidence_item_count": 9,
                    "support_component_specific_count": 4,
                    "support_pressure_or_capacity_count": 2,
                    "support_expansion_or_capex_count": 3,
                    "source_classes": ["trade_press"],
                    "top_support_evidence_items": [],
                },
            ]
        },
        {
            "handoff_rows": [
                {
                    "system_label": "grid equipment and transformer buildout",
                    "canonical_entity_name": "Transformer Co",
                    "market_handoff_status": "public_investable_now",
                },
                {
                    "system_label": "utility response",
                    "canonical_entity_name": "Utility Co",
                    "market_handoff_status": "public_investable_now",
                },
                {
                    "system_label": "data center backup-power equipment buildout",
                    "canonical_entity_name": "Backup Co",
                    "market_handoff_status": "public_investable_now",
                },
            ]
        },
    )

    transformer = next(
        row for row in batch["classification_rows"] if row["canonical_entity_name"] == "Transformer Co"
    )
    assert transformer["bottleneck_role_label"] == "bottleneck_candidate"

    utility = next(row for row in batch["classification_rows"] if row["canonical_entity_name"] == "Utility Co")
    assert utility["bottleneck_role_label"] == "capacity_response_operator"

    backup = next(row for row in batch["classification_rows"] if row["canonical_entity_name"] == "Backup Co")
    assert backup["bottleneck_role_label"] == "supply_chain_beneficiary"

