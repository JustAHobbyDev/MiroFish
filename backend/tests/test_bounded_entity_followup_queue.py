from app.services.bounded_entity_followup_queue import build_bounded_entity_followup_queue


def test_build_bounded_entity_followup_queue_filters_to_real_operator_rows() -> None:
    result = build_bounded_entity_followup_queue(
        {
            "candidates": [
                {
                    "entity_name": "DTE",
                    "system_label": "utility and large-load power buildout",
                    "entity_role": "capacity_operator_or_owner",
                    "priority_tier": "medium",
                    "source_classes": ["trade_press"],
                    "support_provenance_status": "real_only",
                },
                {
                    "entity_name": "Eaton",
                    "system_label": "utility and large-load power buildout",
                    "entity_role": "equipment_or_component_supplier",
                    "priority_tier": "medium",
                    "source_classes": ["trade_press"],
                    "support_provenance_status": "real_only",
                },
                {
                    "entity_name": "Synthetic Utility",
                    "system_label": "utility and large-load power buildout",
                    "entity_role": "capacity_operator_or_owner",
                    "priority_tier": "medium",
                    "source_classes": ["company_release"],
                    "support_provenance_status": "synthetic_only",
                },
            ]
        },
        {
            "support_rows": [
                {
                    "canonical_entity_name": "DTE",
                    "resolved_issuer_name": "DTE Energy Company",
                    "filing_support_status": "supported",
                }
            ]
        },
        system_label="utility and large-load power buildout",
        allowed_entity_roles=["capacity_operator_or_owner", "power_or_utility_operator"],
    )

    assert result["metrics"]["selected_queue_count"] == 1
    row = result["queue_rows"][0]
    assert row["canonical_entity_name"] == "DTE"
    assert row["filing_followup_status"] == "already_supported"
    assert row["existing_resolved_issuer_name"] == "DTE Energy Company"
