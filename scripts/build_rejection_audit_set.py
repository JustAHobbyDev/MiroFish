#!/usr/bin/env python3
"""
Build a rejection-audit review set from a prefilter batch and extraction batches.
"""

from __future__ import annotations

import argparse
import json
import random
from pathlib import Path
from typing import Any, Dict, Iterable


DEFAULT_RANDOM_SEED = 20260320


def _load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _build_artifact_lookup(prefilter_batch: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    lookup: Dict[str, Dict[str, Any]] = {}
    for section in ("kept_artifacts", "review_artifacts"):
        for artifact in prefilter_batch.get(section, []):
            artifact_id = str(artifact.get("artifact_id") or "")
            if artifact_id:
                lookup[artifact_id] = artifact
    return lookup


def _sample_prefilter_drops(
    prefilter_batch: Dict[str, Any],
    *,
    sample_size: int,
    random_seed: int,
) -> list[Dict[str, Any]]:
    drops = list(prefilter_batch.get("dropped_audit_records", []))
    if not drops:
        return []

    rng = random.Random(random_seed)
    sample = drops if len(drops) <= sample_size else rng.sample(drops, sample_size)
    sample = sorted(sample, key=lambda row: (str(row.get("published_at") or ""), str(row.get("title") or "")))

    results: list[Dict[str, Any]] = []
    for row in sample:
        results.append(
            {
                "audit_type": "prefilter_drop",
                "artifact_id": row.get("artifact_id"),
                "source_class": row.get("source_class"),
                "publisher_or_author": row.get("publisher_or_author"),
                "published_at": row.get("published_at"),
                "title": row.get("title"),
                "triage": row.get("triage"),
                "reason": row.get("reason"),
                "matched_families": row.get("matched_families", []),
                "fired_rules": row.get("fired_rules", []),
                "excluded_generic_hits": row.get("excluded_generic_hits", []),
                "review_label": None,
                "review_notes": "",
            }
        )
    return results


def _iter_no_candidate_audits(
    extraction_batch: Dict[str, Any],
    artifact_lookup: Dict[str, Dict[str, Any]],
) -> Iterable[Dict[str, Any]]:
    for row in extraction_batch.get("processed_results", []):
        if row.get("produced_candidates") is not False:
            continue
        artifact_id = str(row.get("artifact_id") or "")
        artifact = artifact_lookup.get(artifact_id, {})
        yield {
            "audit_type": "llm_no_candidate",
            "artifact_id": artifact_id,
            "source_class": row.get("source_class") or artifact.get("source_class"),
            "provider_name": row.get("provider_name"),
            "model_name": row.get("model_name"),
            "prompt_version": row.get("prompt_version"),
            "publisher_or_author": artifact.get("publisher_or_author"),
            "published_at": artifact.get("published_at"),
            "title": artifact.get("title"),
            "source_url": artifact.get("source_url"),
            "prefilter_triage": row.get("prefilter_triage") or artifact.get("prefilter_triage"),
            "rejection_reason": row.get("rejection_reason"),
            "heuristic_filter_applied": bool(row.get("heuristic_filter_applied")),
            "heuristic_filter_reason": row.get("heuristic_filter_reason"),
            "review_label": None,
            "review_notes": "",
        }


def build_rejection_audit_set(
    *,
    prefilter_batch: Dict[str, Any],
    extraction_batches: list[Dict[str, Any]],
    sample_size: int,
    random_seed: int,
) -> Dict[str, Any]:
    artifact_lookup = _build_artifact_lookup(prefilter_batch)
    sampled_prefilter_drops = _sample_prefilter_drops(
        prefilter_batch,
        sample_size=sample_size,
        random_seed=random_seed,
    )

    extraction_no_candidate_sets = []
    total_no_candidate_count = 0
    for batch in extraction_batches:
        items = list(_iter_no_candidate_audits(batch, artifact_lookup))
        total_no_candidate_count += len(items)
        extraction_no_candidate_sets.append(
            {
                "provider_name": next((row.get("provider_name") for row in batch.get("processed_results", []) if row.get("provider_name")), None),
                "model_name": batch.get("model_name"),
                "prompt_version": batch.get("prompt_version"),
                "items": items,
            }
        )

    return {
        "audit_name": f"{prefilter_batch.get('name', 'rejection_audit')}_review_set_v1",
        "source_batch_name": prefilter_batch.get("name"),
        "random_seed": random_seed,
        "prefilter_drop_sample_size": len(sampled_prefilter_drops),
        "prefilter_drop_population_size": len(prefilter_batch.get("dropped_audit_records", [])),
        "llm_no_candidate_total_count": total_no_candidate_count,
        "sampled_prefilter_drops": sampled_prefilter_drops,
        "llm_no_candidate_sets": extraction_no_candidate_sets,
        "review_guidance": {
            "allowed_labels": [
                "correct_rejection",
                "borderline_should_review",
                "false_negative",
            ],
            "notes": [
                "Use correct_rejection when the artifact should clearly remain rejected for the current rising-demand structural-pressure workflow.",
                "Use borderline_should_review when the artifact is not a clear signal but may deserve a weaker review queue rather than hard rejection.",
                "Use false_negative when the artifact plausibly contains meaningful capital-flow or physical-buildout implications that the current pipeline should have surfaced.",
            ],
        },
    }


def _write_markdown_summary(payload: Dict[str, Any], output_path: Path) -> None:
    lines = [
        "# Rejection Audit Set",
        "",
        f"- Source batch: `{payload.get('source_batch_name')}`",
        f"- Random seed: `{payload.get('random_seed')}`",
        f"- Prefilter drop sample: `{payload.get('prefilter_drop_sample_size')}` / `{payload.get('prefilter_drop_population_size')}`",
        f"- LLM no-candidate total: `{payload.get('llm_no_candidate_total_count')}`",
        "",
        "## LLM No-Candidate Sets",
        "",
    ]

    for batch in payload.get("llm_no_candidate_sets", []):
        lines.append(f"- `{batch.get('provider_name')}` / `{batch.get('model_name')}`: `{len(batch.get('items', []))}`")

    lines.extend(
        [
            "",
            "## Review Labels",
            "",
            "- `correct_rejection`",
            "- `borderline_should_review`",
            "- `false_negative`",
            "",
        ]
    )

    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("prefilter_batch_json", type=Path)
    parser.add_argument("extraction_batch_json", nargs="+", type=Path)
    parser.add_argument("--sample-size", type=int, default=25)
    parser.add_argument("--random-seed", type=int, default=DEFAULT_RANDOM_SEED)
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-markdown", type=Path)
    args = parser.parse_args()

    payload = build_rejection_audit_set(
        prefilter_batch=_load_json(args.prefilter_batch_json),
        extraction_batches=[_load_json(path) for path in args.extraction_batch_json],
        sample_size=args.sample_size,
        random_seed=args.random_seed,
    )
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    if args.output_markdown:
        args.output_markdown.parent.mkdir(parents=True, exist_ok=True)
        _write_markdown_summary(payload, args.output_markdown)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
