from app.services.utility_lane_review_surface_builder import build_utility_lane_review_surface


def test_build_utility_lane_review_surface_combines_public_and_private_routes() -> None:
    result = build_utility_lane_review_surface(
        {
            "rows": [
                {
                    "canonical_entity_name": "FirstEnergy",
                    "system_label": "utility and large-load power buildout",
                    "entity_role": "capacity_operator_or_owner",
                    "priority_tier": "medium",
                    "downstream_status": "public_filing_supported",
                    "resolved_issuer_name": "FirstEnergy Corp.",
                    "followup_status": "already_supported",
                    "filing_strong_evidence_item_count": 8,
                    "next_action": "reuse_existing_filing_support",
                },
                {
                    "canonical_entity_name": "CyrusOne",
                    "system_label": "utility and large-load power buildout",
                    "entity_role": "capacity_operator_or_owner",
                    "priority_tier": "low",
                    "downstream_status": "private_company_diligence_required",
                    "resolved_issuer_name": "CyrusOne",
                    "followup_status": "needs_live_resolution",
                    "filing_strong_evidence_item_count": 0,
                    "next_action": "run_private_company_diligence",
                },
            ]
        },
        {
            "queue_rows": [
                {"canonical_entity_name": "FirstEnergy", "source_classes": ["trade_press"]},
                {"canonical_entity_name": "CyrusOne", "source_classes": ["trade_press"]},
            ]
        },
        {
            "support_rows": [
                {
                    "canonical_entity_name": "FirstEnergy",
                    "role_specific_evidence_summary": {
                        "load_and_demand_signal_count": 4,
                        "grid_response_signal_count": 2,
                        "capex_response_signal_count": 1,
                    },
                }
            ]
        },
        {
            "collections": [
                {
                    "canonical_entity_name": "CyrusOne",
                    "collection_summary": {
                        "document_count": 3,
                        "existing_document_count": 3,
                    },
                }
            ]
        },
    )

    assert result["metrics"]["public_filing_reuse_count"] == 1
    assert result["metrics"]["private_company_diligence_count"] == 1
    assert result["rows"][0]["canonical_entity_name"] == "FirstEnergy"
    assert result["rows"][1]["private_existing_document_count"] == 3
