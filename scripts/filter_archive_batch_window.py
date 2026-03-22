#!/usr/bin/env python3
"""
Freeze archive batches to a date window.
"""

from __future__ import annotations

import argparse
import json
import sys
import types
from datetime import date
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path


def _load_module(name: str):
    services_root = Path(__file__).resolve().parents[1] / "backend" / "app" / "services"
    app_root = Path(__file__).resolve().parents[1] / "backend" / "app"

    app_pkg = types.ModuleType("app")
    app_pkg.__path__ = [str(app_root)]
    services_pkg = types.ModuleType("app.services")
    services_pkg.__path__ = [str(services_root)]
    sys.modules.setdefault("app", app_pkg)
    sys.modules.setdefault("app.services", services_pkg)

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
    parser.add_argument("--batch-type", choices=("prefilter", "signal"), required=True)
    parser.add_argument("--input-json", type=Path, required=True)
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--name", default="")
    parser.add_argument("--start-date", required=True)
    parser.add_argument("--end-date", required=True)
    parser.add_argument("--prefilter-json", type=Path, help="Required when batch-type=signal.")
    args = parser.parse_args()

    module = _load_module("archive_batch_window_filter")
    name = args.name or None

    if args.batch_type == "prefilter":
        payload = module.filter_prefilter_batch_by_window(
            _load_json(args.input_json),
            start_date=date.fromisoformat(args.start_date),
            end_date=date.fromisoformat(args.end_date),
            name=name,
        )
    else:
        if args.prefilter_json is None:
            raise SystemExit("--prefilter-json is required when batch-type=signal")
        filtered_prefilter = _load_json(args.prefilter_json)
        payload = module.filter_signal_batch_by_artifact_ids(
            _load_json(args.input_json),
            allowed_artifact_ids=module.artifact_ids_from_prefilter_batch(filtered_prefilter),
            name=name,
        )

    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
