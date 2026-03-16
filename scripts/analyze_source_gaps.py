#!/usr/bin/env python3
"""
Generate a promotion-aware source gap report for a structural parse.
"""

from __future__ import annotations

import argparse
import json
import sys
import types
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path


def _load_source_registry_module():
    services_root = Path(__file__).resolve().parents[1] / "backend" / "app" / "services"

    app_pkg = types.ModuleType("app")
    app_pkg.__path__ = []
    services_pkg = types.ModuleType("app.services")
    services_pkg.__path__ = [str(services_root)]
    sys.modules["app"] = app_pkg
    sys.modules["app.services"] = services_pkg

    full_name = "app.services.source_registry"
    if full_name not in sys.modules:
        spec = spec_from_file_location(full_name, services_root / "source_registry.py")
        module = module_from_spec(spec)
        sys.modules[full_name] = module
        assert spec.loader is not None
        spec.loader.exec_module(module)

    return sys.modules[full_name]


def _load_optional_json(path: Path | None):
    if path is None or not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source_registry_json", type=Path)
    parser.add_argument("--source-bundle-json", type=Path)
    parser.add_argument("--structural-parse-json", type=Path)
    parser.add_argument("--graduation-json", type=Path)
    parser.add_argument("--source-acquisition-plan-json", type=Path)
    parser.add_argument("--max-actions", type=int, default=6)
    parser.add_argument("--output-json", required=True, type=Path)
    args = parser.parse_args()

    module = _load_source_registry_module()
    source_registry = json.loads(args.source_registry_json.read_text(encoding="utf-8"))
    report = module.build_source_gap_report(
        source_registry,
        source_bundle=_load_optional_json(args.source_bundle_json),
        structural_parse=_load_optional_json(args.structural_parse_json),
        graduation=_load_optional_json(args.graduation_json),
        source_acquisition_plan=_load_optional_json(args.source_acquisition_plan_json),
        max_actions=args.max_actions,
    )

    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
