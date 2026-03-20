#!/usr/bin/env python3
"""
Build a deterministic company-release prefilter batch from raw release records.
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

    app_pkg = types.ModuleType("app")
    app_pkg.__path__ = []
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


def _load_records(path: Path):
    payload = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict) and isinstance(payload.get("records"), list):
        return payload["records"]
    raise SystemExit(f"{path} must contain either a JSON list or an object with a 'records' list.")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("records_json", type=Path)
    parser.add_argument("--batch-name", default="company_release_prefilter_batch_v1")
    parser.add_argument("--output-json", type=Path, required=True)
    args = parser.parse_args()

    module = _load_module("company_release_archive")
    payload = module.build_company_release_prefilter_batch(
        _load_records(args.records_json),
        batch_name=args.batch_name,
    )
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
