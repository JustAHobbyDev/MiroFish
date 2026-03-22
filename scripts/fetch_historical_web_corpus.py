#!/usr/bin/env python3
"""
Fetch a retrospective historical web corpus from a manifest of source URLs.
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


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest_json", type=Path)
    parser.add_argument("--output-json", type=Path, required=True)
    args = parser.parse_args()

    module = _load_module("historical_web_archive")
    manifest = json.loads(args.manifest_json.read_text(encoding="utf-8"))
    records = []
    failures = []
    for entry in manifest.get("entries", []):
        try:
            records.append(module.fetch_historical_web_record(entry))
        except Exception as exc:  # pragma: no cover - exercised in live collection
            failures.append(
                {
                    "corpus_entry_id": entry.get("corpus_entry_id"),
                    "source_url": entry.get("source_url"),
                    "error_type": type(exc).__name__,
                    "error": str(exc),
                }
            )
    payload = {
        "name": manifest.get("archive_id", "historical_web_corpus"),
        "archive_id": manifest.get("archive_id"),
        "entries": records,
        "fetch_failures": failures,
        "metrics": {
            "entry_count": len(records),
            "fetch_failure_count": len(failures),
        },
    }
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
