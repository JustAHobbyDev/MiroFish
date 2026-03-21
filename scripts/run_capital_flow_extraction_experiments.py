#!/usr/bin/env python3
"""
Run the standard capital-flow extraction experiment order over a prefilter batch.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


EXPERIMENTS = [
    {
        "name": "groq_llama_3_1_8b_instant",
        "provider": "groq",
        "model_name": "llama-3.1-8b-instant",
    },
    {
        "name": "groq_gpt_oss_20b",
        "provider": "groq",
        "model_name": "openai/gpt-oss-20b",
    },
    {
        "name": "openai_gpt_4o_mini",
        "provider": "openai",
        "model_name": "gpt-4o-mini",
    },
]


def _load_metrics(path: Path) -> dict:
    payload = json.loads(path.read_text(encoding="utf-8"))
    return payload.get("metrics", {})


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("prefilter_batch_json", type=Path)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    args.output_dir.mkdir(parents=True, exist_ok=True)

    summary = []
    for experiment in EXPERIMENTS:
        output_path = args.output_dir / f"{experiment['name']}.json"
        cmd = [
            "bash",
            "./scripts/backend-uv.sh",
            "run",
            "python",
            "../scripts/build_capital_flow_signal_batch.py",
            str(args.prefilter_batch_json),
            "--output-json",
            str(output_path),
            "--provider",
            experiment["provider"],
            "--model-name",
            experiment["model_name"],
        ]
        completed = subprocess.run(cmd, cwd=Path(__file__).resolve().parents[1])
        metrics = _load_metrics(output_path) if output_path.exists() else {}
        summary.append(
            {
                "name": experiment["name"],
                "provider": experiment["provider"],
                "model_name": experiment["model_name"],
                "exit_code": completed.returncode,
                "output_json": str(output_path),
                "metrics": metrics,
            }
        )

    summary_path = args.output_dir / "summary.json"
    summary_path.write_text(
        json.dumps({"runs": summary}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
