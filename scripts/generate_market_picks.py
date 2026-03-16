#!/usr/bin/env python3
"""
Generate ranked market picks from a structured scan batch.

This script is opinionated on purpose. It forces a final expression choice:
- `shares`
- `leaps_call`
- `reject`

That keeps the workflow focused on pick generation rather than open-ended notes.
"""

from __future__ import annotations

import argparse
import json
import sys
import types
from dataclasses import asdict, dataclass
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
from typing import Any, Dict, List


DEFAULT_STOCK_FIT_WEIGHTS: Dict[str, float] = {
    "market_accessibility": 0.16,
    "implementation_simplicity": 0.18,
    "balance_sheet_resilience": 0.14,
    "dilution_risk_inverse": 0.14,
    "thesis_linearity": 0.14,
    "duration_tolerance": 0.14,
    "listing_quality": 0.10,
}


def _load_screening_module():
    services_root = Path(__file__).resolve().parents[1] / "backend" / "app" / "services"

    app_pkg = types.ModuleType("app")
    app_pkg.__path__ = []
    services_pkg = types.ModuleType("app.services")
    services_pkg.__path__ = [str(services_root)]
    sys.modules["app"] = app_pkg
    sys.modules["app.services"] = services_pkg

    for name in ["chokepoint_scoring", "mispricing_screening"]:
        full_name = f"app.services.{name}"
        if full_name in sys.modules:
            continue
        spec = spec_from_file_location(full_name, services_root / f"{name}.py")
        module = module_from_spec(spec)
        sys.modules[full_name] = module
        assert spec.loader is not None
        spec.loader.exec_module(module)

    return sys.modules["app.services.mispricing_screening"]


def _load_rows(path: Path) -> List[Dict[str, Any]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict) and isinstance(payload.get("rows"), list):
        return payload["rows"]
    raise ValueError("input must be a list or object with a 'rows' list")


def _validate_weights(weights: Dict[str, float]) -> Dict[str, float]:
    total = sum(float(value) for value in weights.values())
    if total <= 0:
        raise ValueError("weights must sum to a positive number")
    return {key: float(value) / total for key, value in weights.items()}


def _clamp_signal(value: float) -> float:
    return max(0.0, min(5.0, float(value)))


@dataclass
class StockExpressionSignals:
    market_accessibility: float
    implementation_simplicity: float
    balance_sheet_resilience: float
    dilution_risk_inverse: float
    thesis_linearity: float
    duration_tolerance: float
    listing_quality: float

    def normalized(self) -> Dict[str, float]:
        return {key: _clamp_signal(value) for key, value in asdict(self).items()}


def _score_stock_fit(signals: StockExpressionSignals) -> Dict[str, Any]:
    normalized_weights = _validate_weights(DEFAULT_STOCK_FIT_WEIGHTS)
    signal_map = signals.normalized()
    weighted = {
        key: signal_map[key] * normalized_weights[key]
        for key in normalized_weights
    }
    score = (sum(weighted.values()) / 5.0) * 100.0
    strongest = sorted(weighted.items(), key=lambda item: item[1], reverse=True)[:3]
    weakest = list(reversed(sorted(weighted.items(), key=lambda item: item[1])[:2]))
    return {
        "score_0_to_100": round(score, 2),
        "weighted_signals": {key: round(value, 4) for key, value in weighted.items()},
        "strongest_drivers": [(key, round(value, 4)) for key, value in strongest],
        "weakest_drivers": [(key, round(value, 4)) for key, value in weakest],
    }


def _choose_expression(mispricing_score: float, options_fit_score: float, stock_fit_score: float) -> str:
    if mispricing_score < 65:
        return "reject"
    if stock_fit_score >= 60 and stock_fit_score >= options_fit_score + 8:
        return "shares"
    if options_fit_score >= 60 and options_fit_score >= stock_fit_score + 8:
        return "leaps_call"
    if stock_fit_score >= 60 and options_fit_score < 60:
        return "shares"
    if options_fit_score >= 60 and stock_fit_score < 60:
        return "leaps_call"
    return "reject"


def _pick_score(mispricing_score: float, stock_fit_score: float, options_fit_score: float, expression: str) -> float:
    expression_bonus = {
        "shares": 4.0,
        "leaps_call": 2.0,
        "reject": -12.0,
    }[expression]
    return round((mispricing_score * 0.55) + (max(stock_fit_score, options_fit_score) * 0.35) + expression_bonus, 2)


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate ranked picks from a structured scan batch")
    parser.add_argument("input_json", help="Path to scan batch JSON")
    parser.add_argument("--output-json", required=True, help="Where to write ranked picks JSON")
    args = parser.parse_args()

    module = _load_screening_module()
    rows = _load_rows(Path(args.input_json))

    ranked = []
    for row in rows:
        candidate = module.MispricingCandidate(
            name=row["name"],
            thesis=row["thesis"],
            underlying=row["underlying"],
            mispricing_type=row["mispricing_type"],
            posture="candidate_generation",
            preferred_expression="undecided",
            time_horizon=row["time_horizon"],
            mispricing_signals=module.MispricingSignals(**row["mispricing_signals"]),
            options_expression_signals=module.OptionsExpressionSignals(
                **row["options_expression_signals"]
            ),
            linked_companies=row.get("linked_companies", []),
            catalysts=row.get("catalysts", []),
            invalidations=row.get("invalidations", []),
            structural_reference={
                "market_theme": row.get("market_theme"),
                "bottleneck_layer": row.get("bottleneck_layer"),
                "value_capture_layer": row.get("value_capture_layer"),
                "why_missed": row.get("why_missed", []),
            },
            notes=row.get("notes", []),
        )
        mispricing_scorecard = module.score_mispricing_candidate(candidate)
        stock_fit = _score_stock_fit(StockExpressionSignals(**row["stock_expression_signals"]))
        mispricing_score = mispricing_scorecard.mispricing.score_0_to_100
        options_fit_score = mispricing_scorecard.options_fit.score_0_to_100
        stock_fit_score = stock_fit["score_0_to_100"]
        final_expression = _choose_expression(mispricing_score, options_fit_score, stock_fit_score)
        ranked.append(
            {
                "name": row["name"],
                "underlying": row["underlying"],
                "market_theme": row.get("market_theme"),
                "thesis": row["thesis"],
                "bottleneck_layer": row.get("bottleneck_layer"),
                "value_capture_layer": row.get("value_capture_layer"),
                "why_missed": row.get("why_missed", []),
                "catalysts": row.get("catalysts", []),
                "invalidations": row.get("invalidations", []),
                "mispricing": mispricing_scorecard.mispricing.to_dict(),
                "options_fit": mispricing_scorecard.options_fit.to_dict(),
                "stock_fit": stock_fit,
                "final_expression": final_expression,
                "pick_score": _pick_score(mispricing_score, stock_fit_score, options_fit_score, final_expression),
            }
        )

    ranked.sort(key=lambda row: row["pick_score"], reverse=True)
    output = {
        "method": "market scan -> mispricing score -> stock-vs-LEAPS choice -> ranked picks",
        "rows": ranked,
    }
    out_path = Path(args.output_json)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
