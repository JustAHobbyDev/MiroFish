#!/usr/bin/env python3
"""
Screen structured mispricing candidates from a JSON file.

This script avoids importing the full Flask app runtime. It loads the screening
modules directly from disk so the research loop can run even when the backend
web stack is not installed locally.
"""

from __future__ import annotations

import argparse
import json
import sys
import types
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path


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


def _load_rows(path: Path):
    payload = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict) and isinstance(payload.get("rows"), list):
        return payload["rows"]
    raise ValueError("input must be a list or an object with a 'rows' list")


def main() -> int:
    parser = argparse.ArgumentParser(description="Screen mispricing candidates from JSON")
    parser.add_argument("input_json", help="Path to input JSON")
    parser.add_argument(
        "--output-json",
        help="Optional output path. Prints to stdout when omitted.",
    )
    args = parser.parse_args()

    module = _load_screening_module()
    rows = _load_rows(Path(args.input_json))

    candidates = []
    for row in rows:
        candidates.append(
            module.MispricingCandidate(
                name=row["name"],
                thesis=row["thesis"],
                underlying=row["underlying"],
                mispricing_type=row["mispricing_type"],
                posture=row["posture"],
                preferred_expression=row["preferred_expression"],
                time_horizon=row["time_horizon"],
                mispricing_signals=module.MispricingSignals(**row["mispricing_signals"]),
                options_expression_signals=module.OptionsExpressionSignals(
                    **row["options_expression_signals"]
                ),
                linked_companies=row.get("linked_companies", []),
                catalysts=row.get("catalysts", []),
                invalidations=row.get("invalidations", []),
                structural_reference=row.get("structural_reference", {}),
                notes=row.get("notes", []),
            )
        )

    results = []
    for candidate, scorecard in zip(candidates, module.screen_candidates(candidates)):
        candidate_dict = candidate.to_dict()
        candidate_dict.update(scorecard.to_dict())
        results.append(candidate_dict)

    output = json.dumps(results, indent=2)
    if args.output_json:
        Path(args.output_json).write_text(output + "\n", encoding="utf-8")
    else:
        print(output)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
