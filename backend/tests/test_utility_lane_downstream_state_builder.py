from app.services.utility_lane_downstream_state_builder import build_utility_lane_downstream_state


def test_build_utility_lane_downstream_state_merges_public_and_private_paths() -> None:
    result = build_utility_lane_downstream_state(
        {
            "queue_rows": [
                {
                    "canonical_entity_name": "DTE",
                    "system_label": "utility and large-load power buildout",
                    "entity_role": "capacity_operator_or_owner",
                    "priority_tier": "medium",
                    "filing_followup_status": "already_supported",
                    "existing_resolved_issuer_name": "DTE Energy Company",
                },
                {
                    "canonical_entity_name": "CyrusOne",
                    "system_label": "utility and large-load power buildout",
                    "entity_role": "capacity_operator_or_owner",
                    "priority_tier": "low",
                    "filing_followup_status": "needs_live_resolution",
                    "existing_resolved_issuer_name": "",
                },
            ]
        },
        {
            "support_rows": [
                {
                    "canonical_entity_name": "DTE",
                    "resolved_issuer_name": "DTE Energy Company",
                    "filing_route_assessment": "sec_route",
                    "filing_support_status": "supported",
                    "filing_strong_evidence_item_count": 7,
                }
            ]
        },
        {
            "plans": [
                {
                    "private_company_diligence_plan_id": "pcd_cyrusone",
                    "canonical_entity_name": "CyrusOne",
                    "resolved_issuer_name": "CyrusOne",
                    "origin_live_resolution_result": {
                        "filing_route_assessment": "private_company_official_company_route"
                    },
                }
            ]
        },
    )

    assert result["metrics"]["public_filing_supported_count"] == 1
    assert result["metrics"]["private_company_diligence_required_count"] == 1
    assert result["rows"][0]["canonical_entity_name"] == "DTE"
    assert result["rows"][1]["canonical_entity_name"] == "CyrusOne"
    assert result["rows"][1]["downstream_status"] == "private_company_diligence_required"

