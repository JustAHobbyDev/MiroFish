from pathlib import Path

from app.services.private_company_diligence_parser import (
    build_private_company_diligence_parse_batch,
    parse_private_company_diligence_document,
)


def test_parse_private_company_diligence_document_html(tmp_path: Path) -> None:
    html_path = tmp_path / "cyrusone.html"
    html_path.write_text(
        "<html><body><p>CyrusOne closed a $1.175 billion ABS issuance for hyperscale data center campus development.</p></body></html>",
        encoding="utf-8",
    )

    parsed = parse_private_company_diligence_document(
        {
            "document_id": "doc_html_1",
            "document_title": "ABS Issuance",
            "document_type": "official_financing_announcement",
            "local_path": str(html_path),
        },
        "utility and large-load power buildout",
    )

    assert parsed["parse_status"] == "parsed"
    assert parsed["keyword_counts"]["abs"] >= 1
    assert parsed["keyword_counts"]["hyperscale"] >= 1
    assert parsed["keyword_counts"]["campus"] >= 1


def test_build_private_company_diligence_parse_batch(tmp_path: Path) -> None:
    html_path = tmp_path / "cyrusone.html"
    html_path.write_text(
        "<html><body><p>Rapid data center campus development increased power capacity needs.</p></body></html>",
        encoding="utf-8",
    )

    batch = build_private_company_diligence_parse_batch(
        {
            "name": "private_collection_batch_v1",
            "collections": [
                {
                    "private_company_diligence_plan_id": "pcd_cyrusone",
                    "canonical_entity_name": "CyrusOne",
                    "resolved_issuer_name": "CyrusOne",
                    "system_label": "utility and large-load power buildout",
                    "route_type": "private_company",
                    "collected_documents": [
                        {
                            "document_id": "doc_html_1",
                            "document_title": "Campus Development",
                            "document_type": "official_press_release",
                            "local_path": str(html_path),
                        }
                    ],
                }
            ],
        }
    )

    assert batch["metrics"]["parsed_collection_count"] == 1
    parsed_document = batch["parsed_collections"][0]["parsed_documents"][0]
    assert parsed_document["keyword_counts"]["data center"] >= 1
    assert parsed_document["keyword_counts"]["capacity"] >= 1
