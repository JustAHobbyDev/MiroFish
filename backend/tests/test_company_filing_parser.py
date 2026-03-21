from pathlib import Path

import fitz

from app.services.company_filing_parser import (
    build_company_filing_parse_batch,
    parse_company_filing_document,
)


def test_parse_company_filing_document_pdf(tmp_path: Path) -> None:
    pdf_path = tmp_path / "sample.pdf"
    doc = fitz.open()
    page = doc.new_page()
    page.insert_text(
        (72, 72),
        "Transformer backlog expanded because power grid manufacturing capacity remained tight.",
    )
    doc.save(pdf_path)
    doc.close()

    parsed = parse_company_filing_document(
        {
            "document_id": "doc_pdf_1",
            "document_title": "Sample PDF",
            "filing_type": "annual_report",
            "local_path": str(pdf_path),
        },
        "grid equipment and transformer buildout",
    )

    assert parsed["parse_status"] == "parsed"
    assert parsed["keyword_counts"]["transformer"] >= 1
    assert parsed["keyword_counts"]["backlog"] >= 1
    assert parsed["document_page_count"] == 1
    assert any(snippet["keyword"] == "transformer" for snippet in parsed["evidence_snippets"])


def test_parse_company_filing_document_html(tmp_path: Path) -> None:
    html_path = tmp_path / "sample.html"
    html_path.write_text(
        "<html><body><p>Manufacturing expansion increased grid capacity and power equipment demand.</p></body></html>",
        encoding="utf-8",
    )

    parsed = parse_company_filing_document(
        {
            "document_id": "doc_html_1",
            "document_title": "Sample HTML",
            "filing_type": "10-k_html",
            "local_path": str(html_path),
        },
        "grid equipment and transformer buildout",
    )

    assert parsed["parse_status"] == "parsed"
    assert parsed["keyword_counts"]["manufacturing"] >= 1
    assert parsed["keyword_counts"]["capacity"] >= 1
    assert parsed["document_page_count"] is None


def test_build_company_filing_parse_batch(tmp_path: Path) -> None:
    pdf_path = tmp_path / "sample.pdf"
    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((72, 72), "Power transformer expansion supports manufacturing backlog.")
    doc.save(pdf_path)
    doc.close()

    batch = build_company_filing_parse_batch(
        {
            "name": "collection_batch_v1",
            "collections": [
                {
                    "company_filing_collection_id": "cfc_1",
                    "canonical_entity_name": "Example Corp",
                    "resolved_issuer_name": "Example Corp",
                    "system_label": "grid equipment and transformer buildout",
                    "filing_route_assessment": "example_route",
                    "collected_documents": [
                        {
                            "document_id": "doc_pdf_1",
                            "document_title": "Sample PDF",
                            "filing_type": "annual_report",
                            "local_path": str(pdf_path),
                        }
                    ],
                }
            ],
        }
    )

    assert batch["metrics"]["input_collection_count"] == 1
    assert batch["metrics"]["parsed_collection_count"] == 1
    assert batch["metrics"]["parsed_document_count"] == 1
    parsed_document = batch["parsed_collections"][0]["parsed_documents"][0]
    assert parsed_document["keyword_counts"]["transformer"] >= 1


def test_parse_company_filing_document_resolves_repo_relative_path(tmp_path: Path, monkeypatch) -> None:
    pdf_path = tmp_path / "sample.pdf"
    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((72, 72), "Grid transformer backlog increased.")
    doc.save(pdf_path)
    doc.close()

    from app.services import company_filing_parser as parser_module

    monkeypatch.setattr(parser_module, "REPO_ROOT", tmp_path)

    parsed = parse_company_filing_document(
        {
            "document_id": "doc_pdf_relative",
            "document_title": "Relative Path PDF",
            "filing_type": "annual_report",
            "local_path": "sample.pdf",
        },
        "grid equipment and transformer buildout",
    )

    assert parsed["parse_status"] == "parsed"
    assert parsed["keyword_counts"]["grid"] >= 1
