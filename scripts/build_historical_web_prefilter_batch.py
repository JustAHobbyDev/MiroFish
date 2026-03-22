#!/usr/bin/env python3
"""
Build a mixed-source prefilter batch from a fetched historical web corpus.
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
    parser.add_argument("raw_corpus_json", type=Path)
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--filing-aware", action="store_true")
    args = parser.parse_args()

    module = _load_module("historical_web_archive")
    payload = module.build_historical_web_prefilter_batch(
        json.loads(args.raw_corpus_json.read_text(encoding="utf-8")).get("entries", []),
        batch_name=f"{args.raw_corpus_json.stem}_prefilter_v1",
        filing_aware=args.filing_aware,
    )
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
