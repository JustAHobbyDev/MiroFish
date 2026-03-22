from app.services.bounded_entity_route_support import build_bounded_entity_route_support_batch


def test_build_bounded_entity_route_support_batch_mixes_public_and_private() -> None:
    batch = build_bounded_entity_route_support_batch(
        {
            "queue_rows": [
                {
                    "canonical_entity_name": "Public Supplier",
                    "system_label": "backup power",
                    "entity_role": "equipment_or_component_supplier",
                    "priority_tier": "high",
                    "source_classes": ["trade_press"],
                    "support_provenance_status": "real_only",
                    "filing_followup_status": "already_supported",
                    "existing_resolved_issuer_name": "Public Supplier plc",
                },
                {
                    "canonical_entity_name": "Private Operator",
                    "system_label": "utility lane",
                    "entity_role": "capacity_operator_or_owner",
                    "priority_tier": "medium",
                    "source_classes": ["trade_press"],
                    "support_provenance_status": "real_only",
                    "filing_followup_status": "needs_live_resolution",
                    "existing_resolved_issuer_name": "",
                },
            ]
        },
        {
            "support_rows": [
                {
                    "canonical_entity_name": "Public Supplier",
                    "resolved_issuer_name": "Public Supplier plc",
                    "filing_route_assessment": "annual_report_route",
                    "filing_support_status": "supported",
                    "filing_evidence_item_count": 5,
                    "filing_strong_evidence_item_count": 4,
                    "filing_component_specific_count": 2,
                    "filing_pressure_or_capacity_count": 1,
                    "filing_expansion_or_capex_count": 1,
                    "role_specific_evidence_summary": {},
                    "top_filing_evidence_items": [{"keyword": "generator"}],
                }
            ]
        },
        {
            "plans": [
                {
                    "canonical_entity_name": "Private Operator",
                    "resolved_issuer_name": "Private Operator LLC",
                    "route_type": "private_company",
                }
            ]
        },
        {
            "evidence_collections": [
                {
                    "canonical_entity_name": "Private Operator",
                    "resolved_issuer_name": "Private Operator LLC",
                    "evidence_items": [
                            {
                                "keyword": "data center",
                                "keyword_family": "system_context",
                                "document_type": "official_press_release",
                                "evidence_strength": "medium",
                                "excerpt": "Data center load growth requires new grid capacity.",
                            },
                            {
                                "keyword": "financing",
                                "keyword_family": "financing_or_capital",
                                "document_type": "official_financing_announcement",
                                "evidence_strength": "high",
                                "excerpt": "Private financing supports campus expansion.",
                            },
                    ],
                    "summary": {
                        "evidence_item_count": 2,
                        "strong_evidence_item_count": 2,
                        "family_counts": {
                            "component_specific": 0,
                            "pressure_or_capacity": 0,
                            "expansion_or_capex": 0,
                            "financing_or_capital": 1,
                            "system_context": 1,
                            "other": 0,
                        },
                    },
                }
            ]
        },
    )

    assert batch["metrics"]["supported_public_count"] == 1
    assert batch["metrics"]["supported_private_count"] == 1
    assert batch["support_rows"][0]["support_status"] == "supported_public_filing"
    private_row = next(row for row in batch["support_rows"] if row["canonical_entity_name"] == "Private Operator")
    assert private_row["support_status"] == "supported_private_company"
    assert private_row["support_route_type"] == "private_company"
    assert private_row["role_specific_evidence_summary"]["load_and_demand_signal_count"] >= 1


def test_build_bounded_entity_route_support_batch_marks_planned_private_without_evidence() -> None:
    batch = build_bounded_entity_route_support_batch(
        {
            "queue_rows": [
                {
                    "canonical_entity_name": "Private Planned",
                    "system_label": "backup power",
                    "entity_role": "equipment_or_component_supplier",
                    "priority_tier": "medium",
                    "source_classes": ["trade_press"],
                    "support_provenance_status": "real_only",
                    "filing_followup_status": "needs_live_resolution",
                }
            ]
        },
        {"support_rows": []},
        {
            "plans": [
                {
                    "canonical_entity_name": "Private Planned",
                    "resolved_issuer_name": "Private Planned GmbH",
                    "route_type": "private_company",
                }
            ]
        },
        {"evidence_collections": []},
    )

    assert batch["support_rows"][0]["support_status"] == "private_company_planned"
