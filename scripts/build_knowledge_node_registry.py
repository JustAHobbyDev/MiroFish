#!/usr/bin/env python3
"""
Build a canonical knowledge-node registry from promoted parse artifacts.
"""

from __future__ import annotations

import argparse
import json
import sys
import types
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
from typing import Any, Dict, List


def _load_module():
    services_root = Path(__file__).resolve().parents[1] / "backend" / "app" / "services"

    app_pkg = types.ModuleType("app")
    app_pkg.__path__ = []
    services_pkg = types.ModuleType("app.services")
    services_pkg.__path__ = [str(services_root)]
    sys.modules["app"] = app_pkg
    sys.modules["app.services"] = services_pkg

    full_name = "app.services.knowledge_node_registry"
    if full_name not in sys.modules:
        spec = spec_from_file_location(full_name, services_root / "knowledge_node_registry.py")
        module = module_from_spec(spec)
        sys.modules[full_name] = module
        assert spec.loader is not None
        spec.loader.exec_module(module)

    return sys.modules[full_name]


def _load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _normalize_rows(payload: Dict[str, Any] | List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    if isinstance(payload, list):
        return payload
    return list(payload.get("rows", []))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest_json", type=Path)
    parser.add_argument("candidate_rows_json", type=Path)
    parser.add_argument("ranked_rows_json", type=Path)
    parser.add_argument("--output-json", required=True, type=Path)
    args = parser.parse_args()

    manifest = _normalize_rows(_load_json(args.manifest_json))
    candidate_rows = _normalize_rows(_load_json(args.candidate_rows_json))
    ranked_rows = _normalize_rows(_load_json(args.ranked_rows_json))

    parse_records = []
    for row in manifest:
        graduation = _load_json(Path(row["graduation"]))
        parse_records.append(
            {
                "name": row.get("name"),
                "structural_parse_path": row.get("structural_parse"),
                "structural_parse": _load_json(Path(row["structural_parse"])),
                "graduation_status": graduation.get("graduation_status"),
                "graduation_score_0_to_100": graduation.get("weighted_score_0_to_100"),
            }
        )

    module = _load_module()
    payload = module.build_knowledge_node_registry(parse_records, candidate_rows, ranked_rows)
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

