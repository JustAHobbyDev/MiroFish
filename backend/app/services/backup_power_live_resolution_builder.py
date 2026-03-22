"""
Deterministic live issuer-resolution results for the narrowed backup-power lane.
"""

from __future__ import annotations

from typing import Any, Dict, List


def _coerce_string(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def _result_for_entity(entity_name: str) -> Dict[str, Any]:
    if entity_name == "AVL":
        return {
            "live_resolution_status": "resolved_private_company_route",
            "resolution_outcome": "private_company_reporting_route_identified",
            "resolved_issuer_name": "AVL List GmbH",
            "resolved_entity_type": "private_company",
            "filing_route_assessment": "private_company_official_company_route",
            "next_action": "Do not start public filing collection. Route AVL into private-company diligence using official company materials and operating announcements.",
            "evidence": [
                {
                    "evidence_type": "official_company_legal_source",
                    "source_url": "https://www.avl.com/en-it/imprint",
                    "note": "Official AVL imprint page identifying AVL LIST GMBH, Austrian commercial-register details, and private-company legal form.",
                },
                {
                    "evidence_type": "official_company_source",
                    "source_url": "https://www.avl.com/en/press/press-release/avl-opens-new-hydrogen-and-fuel-cell-test-center-graz",
                    "note": "Official AVL company press page describing AVL as a large operating company and confirming the corporate site as the primary diligence route rather than a public filing route.",
                },
            ],
        }
    if entity_name == "Rolls-Royce":
        return {
            "live_resolution_status": "resolved_direct_foreign_public_route",
            "resolution_outcome": "direct_foreign_public_issuer_reporting_route_identified",
            "resolved_issuer_name": "Rolls-Royce Holdings plc",
            "resolved_entity_type": "foreign_public_company",
            "filing_route_assessment": "rolls_royce_ir_and_annual_report_route",
            "next_action": "Use Rolls-Royce investor-relations results materials and the official annual report as the first filing route for bounded follow-up.",
            "evidence": [
                {
                    "evidence_type": "official_investor_relations_source",
                    "source_url": "https://www.rolls-royce.com/investors/results-reports-and-presentations/financial-results.aspx",
                    "note": "Official Rolls-Royce investor-relations financial results page for current reporting materials.",
                },
                {
                    "evidence_type": "official_annual_report_pdf",
                    "source_url": "https://www.rolls-royce.com/~/media/Files/R/Rolls-Royce/documents/annual-report/2026/2025-annual-report.pdf",
                    "note": "Official Rolls-Royce 2025 annual report PDF hosted on rolls-royce.com.",
                },
            ],
        }
    return {
        "live_resolution_status": "unresolved_no_official_route_captured",
        "resolution_outcome": "no_live_route_captured",
        "resolved_issuer_name": "",
        "resolved_entity_type": "",
        "filing_route_assessment": "",
        "next_action": "Capture official issuer-route evidence before any filing or private-company diligence step.",
        "evidence": [],
    }


def build_backup_power_live_resolution_batch(
    followup_queue_batch: Dict[str, Any],
) -> Dict[str, Any]:
    results: List[Dict[str, Any]] = []

    for row in followup_queue_batch.get("queue_rows", []):
        if _coerce_string(row.get("system_label")) != "data center backup-power equipment buildout":
            continue
        entity_name = _coerce_string(row.get("canonical_entity_name"))
        result = _result_for_entity(entity_name)
        results.append(
            {
                "canonical_entity_name": entity_name,
                "system_label": _coerce_string(row.get("system_label")),
                **result,
            }
        )

    return {
        "name": "mixed_issuer_resolution_live_backup_power_v1",
        "results": results,
        "metrics": {
            "evaluated_real_entity_count": len(results),
            "resolved_direct_foreign_public_route_count": len(
                [row for row in results if row["live_resolution_status"] == "resolved_direct_foreign_public_route"]
            ),
            "resolved_private_company_route_count": len(
                [row for row in results if row["live_resolution_status"] == "resolved_private_company_route"]
            ),
            "unresolved_count": len(
                [row for row in results if row["live_resolution_status"] == "unresolved_no_official_route_captured"]
            ),
        },
    }
