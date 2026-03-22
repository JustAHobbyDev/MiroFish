from app.services.bounded_entity_filing_support import build_bounded_entity_filing_support_batch


def test_build_bounded_entity_filing_support_batch() -> None:
    batch = build_bounded_entity_filing_support_batch(
        {
            "expansions": [
                {
                    "canonical_entity_name": "Example Corp",
                    "system_label": "grid equipment and transformer buildout",
                    "priority_tier": "high",
                    "entity_role": "equipment_or_component_supplier",
                },
                {
                    "canonical_entity_name": "Other Corp",
                    "system_label": "grid equipment and transformer buildout",
                    "priority_tier": "medium",
                    "entity_role": "capacity_operator_or_owner",
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
    assert batch["support_rows"][0]["role_lane"] == "equipment_supplier"
    assert batch["support_rows"][0]["filing_support_status"] == "supported"
    assert batch["support_rows_by_role_lane"]["equipment_supplier"][0]["canonical_entity_name"] == "Example Corp"
    assert batch["support_rows"][1]["filing_support_status"] == "not_yet_supported"


def test_build_bounded_entity_filing_support_batch_adds_utility_specific_summary() -> None:
    batch = build_bounded_entity_filing_support_batch(
        {
            "expansions": [
                {
                    "canonical_entity_name": "Utility Example",
                    "system_label": "data center power demand buildout",
                    "priority_tier": "medium",
                    "entity_role": "capacity_operator_or_owner",
                }
            ]
        },
        {
            "evidence_collections": [
                {
                    "canonical_entity_name": "Utility Example",
                    "resolved_issuer_name": "Utility Example Holdings",
                    "filing_route_assessment": "sec_route",
                    "summary": {
                        "evidence_item_count": 5,
                        "strong_evidence_item_count": 4,
                        "family_counts": {
                            "component_specific": 1,
                            "pressure_or_capacity": 2,
                            "expansion_or_capex": 1,
                            "system_context": 1,
                        },
                    },
                    "evidence_items": [
                        {"keyword": "data center", "keyword_family": "system_context", "excerpt": "data center load growth"},
                        {"keyword": "capacity", "keyword_family": "pressure_or_capacity", "excerpt": "capacity demand"},
                        {"keyword": "substation", "keyword_family": "component_specific", "excerpt": "build substations"},
                        {"keyword": "expansion", "keyword_family": "expansion_or_capex", "excerpt": "capital expansion"},
                    ],
                }
            ]
        },
    )

    row = batch["support_rows"][0]
    assert row["role_lane"] == "utility_or_operator"
    assert row["role_specific_evidence_summary"]["load_and_demand_signal_count"] >= 2
    assert row["role_specific_evidence_summary"]["grid_response_signal_count"] >= 1
    assert row["role_specific_evidence_summary"]["capex_response_signal_count"] == 1


def test_build_bounded_entity_filing_support_batch_accepts_candidate_batches() -> None:
    batch = build_bounded_entity_filing_support_batch(
        {
            "candidates": [
                {
                    "entity_name": "Rolls-Royce",
                    "system_label": "data center backup-power equipment buildout",
                    "priority_tier": "high",
                    "entity_role": "equipment_or_component_supplier",
                    "supporting_titles": ["Rolls-Royce invests $75M in South Carolina engine plant"],
                }
            ]
        },
        {
            "evidence_collections": [
                {
                    "canonical_entity_name": "Rolls-Royce",
                    "resolved_issuer_name": "Rolls-Royce Holdings plc",
                    "filing_route_assessment": "rolls_royce_route",
                    "summary": {
                        "evidence_item_count": 2,
                        "strong_evidence_item_count": 2,
                        "family_counts": {
                            "component_specific": 1,
                            "pressure_or_capacity": 0,
                            "expansion_or_capex": 1,
                        },
                    },
                    "evidence_items": [{"keyword": "engine"}],
                }
            ]
        },
    )

    assert batch["metrics"]["input_entity_expansion_count"] == 1
    assert batch["support_rows"][0]["canonical_entity_name"] == "Rolls-Royce"
    assert batch["support_rows"][0]["filing_support_status"] == "supported"
