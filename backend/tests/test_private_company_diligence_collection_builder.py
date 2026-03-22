from app.services.private_company_diligence_collection_builder import (
    build_private_company_diligence_collection_batch,
)


def test_build_private_company_diligence_collection_batch_attaches_manifest_documents() -> None:
    result = build_private_company_diligence_collection_batch(
        {
            "plans": [
                {
                    "private_company_diligence_plan_id": "pcd_cyrusone",
                    "canonical_entity_name": "CyrusOne",
                    "resolved_issuer_name": "CyrusOne",
                    "system_label": "utility and large-load power buildout",
                    "route_type": "private_company",
                    "source_priorities": ["official_company_site"],
                }
            ]
        },
        {
            "documents": [
                {
                    "canonical_entity_name": "CyrusOne",
                    "document_id": "cyrusone_about",
                    "document_type": "official_company_page",
                    "document_title": "About Us",
                    "source_url": "https://www.cyrusone.com/about-us",
                    "local_path": "README.md",
                    "source_priority": "official_company_site",
                }
            ]
        },
    )

    assert result["metrics"]["collection_count"] == 1
    collection = result["collections"][0]
    assert collection["canonical_entity_name"] == "CyrusOne"
    assert collection["collection_summary"]["document_count"] == 1

