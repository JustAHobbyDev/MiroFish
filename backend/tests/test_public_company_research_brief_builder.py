from app.services.public_company_research_brief_builder import (
    build_public_company_research_brief_batch,
)


def test_build_public_company_research_brief_batch_joins_filing_support() -> None:
    batch = build_public_company_research_brief_batch(
        {
            "handoff_rows": [
                {
                    "name": "GE Vernova on grid equipment and transformer buildout",
                    "canonical_entity_name": "GE Vernova on grid equipment and transformer buildout",
                    "underlying": "GEV",
                    "market_theme": "grid equipment and transformer buildout",
                    "role_label": "bottleneck_candidate",
                    "execution_priority": "highest",
                    "execution_expression": "shares",
                    "thesis": "GE Vernova thesis",
                    "value_capture_layer": "Constrained supplier",
                    "top_catalysts": ["c1", "c2"],
                    "top_invalidations": ["i1"],
                    "why_missed": ["w1"],
                }
            ]
        },
        {
            "support_rows": [
                {
                    "canonical_entity_name": "GE Vernova",
                    "resolved_issuer_name": "GE Vernova Inc.",
                    "filing_support_status": "supported",
                    "filing_evidence_item_count": 19,
                    "filing_strong_evidence_item_count": 16,
                    "filing_component_specific_count": 6,
                    "filing_pressure_or_capacity_count": 5,
                    "filing_expansion_or_capex_count": 4,
                    "top_filing_evidence_items": [
                        {
                            "document_title": "GE Vernova Form 10-K 2025",
                            "filing_type": "10-k_pdf",
                            "keyword": "transformer",
                            "keyword_family": "component_specific",
                            "page_number": 6,
                            "excerpt": "power transformers and switchgear",
                        }
                    ],
                }
            ]
        },
    )

    assert batch["metrics"]["brief_count"] == 1
    row = batch["brief_rows"][0]
    assert row["canonical_entity_name"] == "GE Vernova"
    assert row["resolved_issuer_name"] == "GE Vernova Inc."
    assert row["brief_status"] == "ready_for_human_company_research"
    assert row["top_supporting_excerpts"][0]["keyword"] == "transformer"
