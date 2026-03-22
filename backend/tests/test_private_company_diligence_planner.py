from app.services.private_company_diligence_planner import build_private_company_diligence_plan_batch


def test_build_private_company_diligence_plan_batch_filters_private_routes() -> None:
    result = build_private_company_diligence_plan_batch(
        {
            "results": [
                {
                    "canonical_entity_name": "CyrusOne",
                    "system_label": "utility and large-load power buildout",
                    "live_resolution_status": "resolved_private_company_route",
                    "resolved_issuer_name": "CyrusOne",
                    "filing_route_assessment": "private_company_official_company_route",
                },
                {
                    "canonical_entity_name": "DTE",
                    "live_resolution_status": "resolved_direct_public_route",
                    "resolved_issuer_name": "DTE Energy Company",
                },
            ]
        }
    )

    assert result["metrics"]["private_company_plan_count"] == 1
    assert result["plans"][0]["canonical_entity_name"] == "CyrusOne"
    assert result["plans"][0]["system_label"] == "utility and large-load power buildout"
    assert result["plans"][0]["route_type"] == "private_company"
