#!/usr/bin/env python3
"""
Build a node-aware ranking view from the canonical knowledge-node registry.
"""

from __future__ import annotations

import argparse
import json
import sys
import types
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path


def _load_module():
    services_root = Path(__file__).resolve().parents[1] / "backend" / "app" / "services"

    app_pkg = types.ModuleType("app")
    app_pkg.__path__ = []
    services_pkg = types.ModuleType("app.services")
    services_pkg.__path__ = [str(services_root)]
    sys.modules["app"] = app_pkg
    sys.modules["app.services"] = services_pkg

    full_name = "app.services.node_aware_ranking"
    if full_name not in sys.modules:
        spec = spec_from_file_location(full_name, services_root / "node_aware_ranking.py")
        module = module_from_spec(spec)
        sys.modules[full_name] = module
        assert spec.loader is not None
        spec.loader.exec_module(module)

    return sys.modules[full_name]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("knowledge_node_registry_json", type=Path)
    parser.add_argument("--output-json", required=True, type=Path)
    args = parser.parse_args()

    registry = json.loads(args.knowledge_node_registry_json.read_text(encoding="utf-8"))
    module = _load_module()
    payload = module.build_node_aware_ranking(registry)
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

