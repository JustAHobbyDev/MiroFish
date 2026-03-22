from app.services.bounded_entity_downstream_state_builder import (
    build_bounded_entity_downstream_state,
)


def test_build_bounded_entity_downstream_state_combines_public_and_private_routes() -> None:
    result = build_bounded_entity_downstream_state(
        {
            "queue_rows": [
                {
                    "canonical_entity_name": "Rolls-Royce",
                    "system_label": "data center backup-power equipment buildout",
                    "entity_role": "equipment_or_component_supplier",
                    "priority_tier": "high",
                    "filing_followup_status": "already_supported",
                    "existing_resolved_issuer_name": "Rolls-Royce Holdings plc",
                },
                {
                    "canonical_entity_name": "AVL",
                    "system_label": "data center backup-power equipment buildout",
                    "entity_role": "equipment_or_component_supplier",
                    "priority_tier": "high",
                    "filing_followup_status": "needs_live_resolution",
                    "existing_resolved_issuer_name": "",
                },
            ]
        },
        {
            "support_rows": [
                {
                    "canonical_entity_name": "Rolls-Royce",
                    "resolved_issuer_name": "Rolls-Royce Holdings plc",
                    "filing_route_assessment": "rolls_royce_ir_and_annual_report_route",
                    "filing_support_status": "supported",
                    "filing_strong_evidence_item_count": 4,
                }
            ]
        },
        {
            "plans": [
                {
                    "private_company_diligence_plan_id": "pcd_avl",
                    "canonical_entity_name": "AVL",
                    "resolved_issuer_name": "AVL List GmbH",
                    "origin_live_resolution_result": {
                        "filing_route_assessment": "private_company_official_company_route"
                    },
                }
            ]
        },
    )

    assert result["metrics"]["public_filing_supported_count"] == 1
    assert result["metrics"]["private_company_diligence_required_count"] == 1
    assert result["rows"][0]["canonical_entity_name"] == "Rolls-Royce"
    assert result["rows"][1]["resolved_issuer_name"] == "AVL List GmbH"
