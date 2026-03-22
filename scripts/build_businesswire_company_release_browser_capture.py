#!/usr/bin/env python3
"""
Build raw Business Wire company-release records from a browser capture summary.
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


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("capture_summary_json", type=Path)
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument(
        "--batch-name",
        default="businesswire_presspass_company_release_raw_v1",
    )
    args = parser.parse_args()

    capture_payload = json.loads(args.capture_summary_json.read_text(encoding="utf-8"))
    module = _load_module("businesswire_company_release_collector")
    records = module.build_businesswire_browser_capture_records(
        capture_payload,
        capture_root=args.capture_summary_json.parent,
    )

    metrics = capture_payload.get("metrics") or {}
    output_payload = {
        "name": args.batch_name,
        "publisher": "Business Wire",
        "capture_meta": capture_payload.get("capture_meta") or {},
        "records": records,
        "metrics": {
            "visible_result_count": metrics.get("visible_result_count", 0),
            "captured_article_count": metrics.get("captured_article_count", 0),
            "capture_failure_count": metrics.get("capture_failure_count", 0),
            "parsed_record_count": len(records),
        },
    }

    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(
        json.dumps(output_payload, ensure_ascii=True, indent=2) + "\n",
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
