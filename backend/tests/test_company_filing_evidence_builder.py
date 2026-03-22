from app.services.company_filing_evidence_builder import build_company_filing_evidence_batch


def test_build_company_filing_evidence_batch() -> None:
    batch = build_company_filing_evidence_batch(
        {
            "name": "parse_batch_v1",
            "parsed_collections": [
                {
                    "resolved_issuer_name": "Example Corp",
                    "canonical_entity_name": "Example Corp",
                    "system_label": "grid equipment and transformer buildout",
                    "filing_route_assessment": "example_route",
                    "parsed_documents": [
                        {
                            "document_id": "doc1",
                            "document_title": "Annual Report",
                            "filing_type": "annual_report",
                            "parse_status": "parsed",
                            "evidence_snippets": [
                                {
                                    "keyword": "transformer",
                                    "page_number": 12,
                                    "excerpt": "Transformer capacity expansion and manufacturing backlog improved.",
                                },
                                {
                                    "keyword": "power",
                                    "page_number": 18,
                                    "excerpt": "Power grid demand increased across the system.",
                                },
                            ],
                        }
                    ],
                }
            ],
        }
    )

    assert batch["metrics"]["evidence_collection_count"] == 1
    assert batch["metrics"]["total_evidence_item_count"] == 2
    collection = batch["evidence_collections"][0]
    assert collection["summary"]["strong_evidence_item_count"] == 1
    assert collection["summary"]["family_counts"]["component_specific"] == 1
    assert collection["summary"]["family_counts"]["system_context"] == 1
    assert collection["evidence_items"][0]["keyword_family"] == "component_specific"
