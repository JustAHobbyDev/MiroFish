from app.services.bounded_entity_filing_priority import build_bounded_entity_filing_priority_batch


def test_build_bounded_entity_filing_priority_batch_prefers_supported_rows() -> None:
    batch = build_bounded_entity_filing_priority_batch(
        {
            "expansions": [
                {
                    "canonical_entity_name": "Supported Grid Co",
                    "system_label": "grid equipment and transformer buildout",
                    "priority_tier": "medium",
                    "support_provenance_status": "real_only",
                    "next_priority_source_classes": ["company_filing", "company_release"],
                },
                {
                    "canonical_entity_name": "Unresolved Utility Co",
                    "system_label": "data center power demand buildout",
                    "priority_tier": "high",
                    "support_provenance_status": "real_only",
                    "next_priority_source_classes": ["company_filing", "trade_press"],
                },
            ]
        },
        {
            "support_rows": [
                {
                    "canonical_entity_name": "Supported Grid Co",
                    "resolved_issuer_name": "Supported Grid Co",
                    "filing_route_assessment": "sec_edgar_route",
                    "filing_support_status": "supported",
                    "filing_evidence_item_count": 6,
                    "filing_strong_evidence_item_count": 5,
                    "filing_component_specific_count": 2,
                    "filing_pressure_or_capacity_count": 2,
                    "filing_expansion_or_capex_count": 1,
                    "top_filing_evidence_items": [{"keyword": "transformer"}],
                }
            ]
        },
    )

    assert batch["metrics"]["input_entity_expansion_count"] == 2
    assert batch["metrics"]["supported_priority_count"] == 1
    assert batch["priority_rows"][0]["canonical_entity_name"] == "Supported Grid Co"
    assert batch["priority_rows"][0]["filing_backed_priority_tier"] == "high"
    assert batch["priority_rows"][0]["selection_action"] == "advance_with_filing_backed_weight"
    assert batch["priority_rows"][1]["selection_action"] == "resolve_and_collect_filing_route"
