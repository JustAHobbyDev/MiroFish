"""
Build deterministic market-scan candidate rows from ready public market-research rows.
"""

from __future__ import annotations

from typing import Any, Dict, List


def _coerce_string(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def _why_missed(role_label: str, exchange_scope: str) -> List[str]:
    reasons: List[str] = []
    if role_label == "bottleneck_candidate":
        reasons.extend(
            [
                "market attention is concentrated on downstream power and AI beneficiaries",
                "constrained component-layer suppliers are less obvious from headline buildout coverage",
            ]
        )
    elif role_label == "capacity_response_operator":
        reasons.extend(
            [
                "utility load-response names are often read as regulated capex stories rather than structural demand-surprise expressions",
                "market focus is usually on data-center tenants rather than the utility-side response layer",
            ]
        )
    else:
        reasons.extend(
            [
                "beneficiary role is real but not yet framed as a strict chokepoint thesis",
                "supplier relevance is easier to miss when coverage emphasizes end-market demand instead of component exposure",
            ]
        )
    if exchange_scope == "foreign_home_market_code":
        reasons.append("primary listing is outside the default U.S. ticker workflow")
    return reasons


def _catalysts(system_label: str, role_label: str) -> List[str]:
    catalysts = ["additional capacity announcements", "order backlog conversion into reported revenue"]
    if "utility response" in system_label:
        catalysts.extend(["new large-load agreements", "utility capex plan increases"])
    if "transformer" in system_label or role_label == "bottleneck_candidate":
        catalysts.extend(["transformer and switchgear lead-time commentary", "substation and grid-equipment expansion updates"])
    if "backup-power" in system_label:
        catalysts.extend(["data-center backup-power order growth", "generator deployment announcements"])
    return catalysts


def _invalidations(role_label: str) -> List[str]:
    invalidations = [
        "capacity expansion arrives without meaningful demand conversion",
        "component or backlog signals fade in subsequent company reporting",
    ]
    if role_label == "capacity_response_operator":
        invalidations.append("large-load demand does not convert into durable utility earnings or capex response")
    else:
        invalidations.append("downstream demand shifts to substitute suppliers or adjacent architectures")
    return invalidations


def _mispricing_signals(role_label: str) -> Dict[str, float]:
    if role_label == "bottleneck_candidate":
        return {
            "hiddenness": 4.0,
            "recognition_gap": 4.0,
            "catalyst_clarity": 3.5,
            "propagation_asymmetry": 4.0,
            "duration_mismatch": 4.0,
            "evidence_quality": 4.5,
            "crowding_inverse": 3.5,
            "valuation_nonlinearity": 3.5,
        }
    if role_label == "capacity_response_operator":
        return {
            "hiddenness": 2.5,
            "recognition_gap": 2.5,
            "catalyst_clarity": 3.5,
            "propagation_asymmetry": 2.5,
            "duration_mismatch": 3.5,
            "evidence_quality": 4.0,
            "crowding_inverse": 2.5,
            "valuation_nonlinearity": 2.0,
        }
    return {
        "hiddenness": 3.0,
        "recognition_gap": 3.0,
        "catalyst_clarity": 3.0,
        "propagation_asymmetry": 3.0,
        "duration_mismatch": 3.5,
        "evidence_quality": 4.0,
        "crowding_inverse": 2.5,
        "valuation_nonlinearity": 2.5,
    }


def _asymmetry_signals(role_label: str) -> Dict[str, float]:
    if role_label == "bottleneck_candidate":
        return {
            "ecosystem_centrality": 4.0,
            "downstream_valuation_gap": 3.5,
            "microcap_rerating_potential": 2.0,
        }
    if role_label == "capacity_response_operator":
        return {
            "ecosystem_centrality": 3.0,
            "downstream_valuation_gap": 2.0,
            "microcap_rerating_potential": 0.5,
        }
    return {
        "ecosystem_centrality": 3.0,
        "downstream_valuation_gap": 2.5,
        "microcap_rerating_potential": 1.0,
    }


def _options_expression_signals(role_label: str) -> Dict[str, float]:
    if role_label == "bottleneck_candidate":
        return {
            "convexity_need": 3.0,
            "tenor_alignment": 3.5,
            "vol_expansion_potential": 3.0,
            "downside_definedness": 2.0,
            "liquidity_path": 2.0,
            "implementation_simplicity": 3.0,
            "catalyst_timing_specificity": 2.5,
        }
    return {
        "convexity_need": 1.5,
        "tenor_alignment": 2.5,
        "vol_expansion_potential": 1.5,
        "downside_definedness": 1.5,
        "liquidity_path": 1.5,
        "implementation_simplicity": 3.0,
        "catalyst_timing_specificity": 2.0,
    }


def _stock_expression_signals(exchange_scope: str) -> Dict[str, float]:
    listing_quality = 4.0
    market_accessibility = 4.0
    if exchange_scope in {"foreign_home_market_code", "foreign_home_market_symbol"}:
        listing_quality = 3.0
        market_accessibility = 2.5
    return {
        "market_accessibility": market_accessibility,
        "implementation_simplicity": 4.5,
        "balance_sheet_resilience": 3.5,
        "dilution_risk_inverse": 3.5,
        "thesis_linearity": 4.0,
        "duration_tolerance": 4.0,
        "listing_quality": listing_quality,
    }


def _leaps_bias_signals(role_label: str, exchange_scope: str) -> Dict[str, float]:
    if exchange_scope in {"foreign_home_market_code", "foreign_home_market_symbol"}:
        return {
            "iv_cheapness": 0.0,
            "surface_staleness": 0.0,
            "pre_expiration_repricing_potential": 0.0,
            "stock_vs_call_convexity_advantage": 0.0,
            "long_dated_liquidity_quality": 0.0,
        }
    if role_label == "bottleneck_candidate":
        return {
            "iv_cheapness": 2.0,
            "surface_staleness": 2.0,
            "pre_expiration_repricing_potential": 2.5,
            "stock_vs_call_convexity_advantage": 2.0,
            "long_dated_liquidity_quality": 2.0,
        }
    return {
        "iv_cheapness": 1.0,
        "surface_staleness": 1.0,
        "pre_expiration_repricing_potential": 1.0,
        "stock_vs_call_convexity_advantage": 1.0,
        "long_dated_liquidity_quality": 1.0,
    }


def _promotion_status(role_label: str) -> str:
    if role_label == "bottleneck_candidate":
        return "pick_candidate"
    return "watchlist_candidate"


def _promotion_score(priority_score: int, role_label: str) -> float:
    base = min(95.0, max(55.0, float(priority_score)))
    if role_label == "bottleneck_candidate":
        return min(95.0, base + 5.0)
    return min(90.0, base)


def _mispricing_type(role_label: str) -> str:
    if role_label == "bottleneck_candidate":
        return "hidden_bottleneck"
    if role_label == "capacity_response_operator":
        return "capacity_response_operator"
    return "supply_chain_beneficiary"


def _bottleneck_layer(system_label: str, role_label: str) -> str:
    if role_label == "capacity_response_operator":
        return f"{system_label} response layer"
    return system_label


def _value_capture_layer(role_label: str) -> str:
    if role_label == "bottleneck_candidate":
        return "Constrained upstream component supplier with system-level leverage"
    if role_label == "capacity_response_operator":
        return "Utility or operator capturing demand-response capex and load growth"
    return "Relevant supply-chain beneficiary without strict bottleneck proof"


def _thesis(row: Dict[str, Any]) -> str:
    entity = _coerce_string(row.get("canonical_entity_name"))
    role_label = _coerce_string(row.get("bottleneck_role_label"))
    system_label = _coerce_string(row.get("system_label"))
    if role_label == "bottleneck_candidate":
        return (
            f"{entity} appears to sit in a constrained {system_label} layer, with filing-backed "
            "component specificity, pressure signals, and capacity-expansion evidence that may still be underappreciated."
        )
    if role_label == "capacity_response_operator":
        return (
            f"{entity} appears positioned to capture {system_label} demand-response economics through "
            "load growth, capex response, and utility-side infrastructure spending."
        )
    return (
        f"{entity} appears to be a relevant beneficiary of {system_label}, but the current evidence "
        "supports a beneficiary posture more cleanly than a strict bottleneck claim."
    )


def build_public_market_scan_candidate_batch(
    public_market_research_row_batch: Dict[str, Any],
) -> Dict[str, Any]:
    rows: List[Dict[str, Any]] = []

    for row in public_market_research_row_batch.get("research_rows", []):
        if _coerce_string(row.get("market_research_row_status")) != "ready_for_market_research":
            continue

        system_label = _coerce_string(row.get("system_label"))
        entity_name = _coerce_string(row.get("canonical_entity_name"))
        symbol = _coerce_string(row.get("mapped_public_symbol"))
        role_label = _coerce_string(row.get("bottleneck_role_label"))
        exchange_scope = _coerce_string(row.get("exchange_scope"))
        priority_score = int(row.get("route_aware_priority_score", 0))

        rows.append(
            {
                "name": f"{entity_name} on {system_label}",
                "market_theme": system_label,
                "thesis": _thesis(row),
                "underlying": symbol,
                "mispricing_type": _mispricing_type(role_label),
                "time_horizon": "12-24m",
                "linked_companies": [entity_name],
                "bottleneck_layer": _bottleneck_layer(system_label, role_label),
                "value_capture_layer": _value_capture_layer(role_label),
                "why_missed": _why_missed(role_label, exchange_scope),
                "catalysts": _catalysts(system_label, role_label),
                "invalidations": _invalidations(role_label),
                "mispricing_signals": _mispricing_signals(role_label),
                "asymmetry_signals": _asymmetry_signals(role_label),
                "leaps_bias_signals": _leaps_bias_signals(role_label, exchange_scope),
                "options_expression_signals": _options_expression_signals(role_label),
                "stock_expression_signals": _stock_expression_signals(exchange_scope),
                "promotion_status": _promotion_status(role_label),
                "promotion_score_0_to_100": _promotion_score(priority_score, role_label),
                "parse_evidence_summary": {
                    "classification_reason": _coerce_string(row.get("classification_reason")),
                    "market_research_row_action": _coerce_string(row.get("market_research_row_action")),
                },
                "market_data_checks": {
                    "symbol_mapping_status": _coerce_string(row.get("symbol_mapping_status")),
                    "exchange_scope": exchange_scope,
                },
                "notes": [
                    f"deterministic market research row built from {role_label}",
                    f"resolved issuer: {_coerce_string(row.get('resolved_issuer_name'))}",
                ],
            }
        )

    rows.sort(key=lambda item: (item["market_theme"], item["name"]))
    return {
        "method": "public market research rows -> deterministic market scan candidates",
        "rows": rows,
        "metrics": {
            "input_research_row_count": len(public_market_research_row_batch.get("research_rows", [])),
            "ready_market_scan_candidate_count": len(rows),
            "pick_candidate_count": len([row for row in rows if row["promotion_status"] == "pick_candidate"]),
            "watchlist_candidate_count": len([row for row in rows if row["promotion_status"] == "watchlist_candidate"]),
        },
    }
