#!/usr/bin/env python3
"""
Run zero-context energy-flow-pressure extraction over a prefilter batch.
"""

from __future__ import annotations

import argparse
import json
import sys
import types
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path


def _load_module(name: str):
    services_root = Path(__file__).resolve().parents[1] / "backend" / "app" / "services"
    utils_root = Path(__file__).resolve().parents[1] / "backend" / "app" / "utils"
    app_root = Path(__file__).resolve().parents[1] / "backend" / "app"

    app_pkg = types.ModuleType("app")
    app_pkg.__path__ = [str(app_root)]
    services_pkg = types.ModuleType("app.services")
    services_pkg.__path__ = [str(services_root)]
    utils_pkg = types.ModuleType("app.utils")
    utils_pkg.__path__ = [str(utils_root)]
    sys.modules.setdefault("app", app_pkg)
    sys.modules.setdefault("app.services", services_pkg)
    sys.modules.setdefault("app.utils", utils_pkg)

    full_name = f"app.services.{name}"
    if full_name not in sys.modules:
        spec = spec_from_file_location(full_name, services_root / f"{name}.py")
        module = module_from_spec(spec)
        sys.modules[full_name] = module
        assert spec.loader is not None
        spec.loader.exec_module(module)

    return sys.modules[full_name]


def _load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("prefilter_batch_json", type=Path)
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--provider")
    parser.add_argument("--model-name")
    args = parser.parse_args()

    module = _load_module("energy_flow_pressure_extractor")
    extractor_kwargs = {}
    if args.provider:
        extractor_kwargs["provider"] = args.provider
    if args.model_name:
        extractor_kwargs["model_name"] = args.model_name
    extractor = module.EnergyFlowPressureExtractor(**extractor_kwargs)
    payload = module.build_energy_flow_pressure_signal_batch(
        _load_json(args.prefilter_batch_json),
        extractor=extractor,
    )
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
