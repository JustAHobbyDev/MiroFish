from app.services.bounded_entity_filing_support import build_bounded_entity_filing_support_batch


def test_build_bounded_entity_filing_support_batch() -> None:
    batch = build_bounded_entity_filing_support_batch(
        {
            "expansions": [
                {
                    "canonical_entity_name": "Example Corp",
                    "system_label": "grid equipment and transformer buildout",
                    "priority_tier": "high",
                },
                {
                    "canonical_entity_name": "Other Corp",
                    "system_label": "grid equipment and transformer buildout",
                    "priority_tier": "medium",
                },
            ]
        },
        {
            "evidence_collections": [
                {
                    "canonical_entity_name": "Example Corp",
                    "resolved_issuer_name": "Example Corp",
                    "filing_route_assessment": "example_route",
                    "summary": {
                        "evidence_item_count": 3,
                        "strong_evidence_item_count": 2,
                        "family_counts": {
                            "component_specific": 1,
                            "pressure_or_capacity": 1,
                            "expansion_or_capex": 1,
                        },
                    },
                    "evidence_items": [{"keyword": "transformer"}],
                }
            ]
        },
    )

    assert batch["metrics"]["input_entity_expansion_count"] == 2
    assert batch["metrics"]["supported_entity_count"] == 1
    assert batch["support_rows"][0]["canonical_entity_name"] == "Example Corp"
    assert batch["support_rows"][0]["filing_support_status"] == "supported"
    assert batch["support_rows"][1]["filing_support_status"] == "not_yet_supported"

