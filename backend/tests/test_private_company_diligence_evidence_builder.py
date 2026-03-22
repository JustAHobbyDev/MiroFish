from app.services.private_company_diligence_evidence_builder import (
    build_private_company_diligence_evidence_batch,
)


def test_build_private_company_diligence_evidence_batch() -> None:
    batch = build_private_company_diligence_evidence_batch(
        {
            "name": "private_parse_batch_v1",
            "parsed_collections": [
                {
                    "resolved_issuer_name": "CyrusOne",
                    "canonical_entity_name": "CyrusOne",
                    "system_label": "utility and large-load power buildout",
                    "route_type": "private_company",
                    "parsed_documents": [
                        {
                            "document_id": "doc1",
                            "document_title": "ABS Issuance",
                            "document_type": "official_financing_announcement",
                            "parse_status": "parsed",
                            "evidence_snippets": [
                                {
                                    "keyword": "abs",
                                    "page_number": None,
                                    "excerpt": "CyrusOne closed a $1.175 billion ABS issuance.",
                                },
                                {
                                    "keyword": "data center",
                                    "page_number": None,
                                    "excerpt": "Data center campus development accelerated.",
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
    assert collection["summary"]["family_counts"]["financing_or_capital"] == 1
    assert collection["summary"]["strong_evidence_item_count"] >= 1
