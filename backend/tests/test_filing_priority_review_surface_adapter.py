from app.services.filing_priority_review_surface_adapter import (
    build_filing_priority_review_surface_batch,
)


def test_build_filing_priority_review_surface_batch_maps_filing_fields_to_review_shape() -> None:
    batch = build_filing_priority_review_surface_batch(
        {
            "name": "filing_priority",
            "priority_rows": [
                {
                    "canonical_entity_name": "Supplier Co",
                    "system_label": "grid equipment and transformer buildout",
                    "base_priority_tier": "high",
                    "resolved_issuer_name": "Supplier Co plc",
                    "filing_route_assessment": "sec_route",
                    "filing_support_status": "supported",
                    "filing_evidence_item_count": 12,
                    "filing_strong_evidence_item_count": 9,
                    "filing_component_specific_count": 4,
                    "filing_pressure_or_capacity_count": 3,
                    "filing_expansion_or_capex_count": 2,
                    "filing_backed_priority_score": 88,
                    "filing_backed_priority_tier": "high",
                    "top_filing_evidence_items": [],
                }
            ],
        }
    )

    row = batch["rows"][0]
    assert row["support_status"] == "supported_public_filing"
    assert row["entity_role"] == "equipment_or_component_supplier"
    assert row["support_component_specific_count"] == 4
    assert row["route_aware_priority_score"] == 88

