#!/usr/bin/env python3
"""
Extract expression-centric context windows from a normalized X archive.
"""

from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Any


DEFAULT_METHOD_TERMS = [
    "supply chain",
    "bom",
    "bill of materials",
    "mapping",
    "model",
    "research",
    "dd",
    "thesis",
    "analyst",
    "analyst note",
    "report",
    "semianalysis",
    "trendforce",
    "morgan stanley",
    "digitimes",
    "lightcounting",
    "smm",
    "counterpoint",
    "northland",
    "ubs",
    "needham",
    "benchmark",
    "conference",
    "filing",
    "10-q",
    "10-k",
    "earnings",
    "earnings call",
    "customer",
    "customers",
    "qualification",
    "capacity",
    "price hikes",
]


def _load_posts(path: Path) -> list[dict[str, Any]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    posts = payload.get("posts")
    if not isinstance(posts, list):
        raise SystemExit(f"{path} does not look like a normalized archive payload with a posts list.")
    return posts


def _match_expression(text: str, expression: str) -> bool:
    return bool(re.search(rf"\${re.escape(expression)}\b", text, re.IGNORECASE))


def _compile_term_pattern(term: str) -> re.Pattern[str]:
    escaped = re.escape(term)
    starts_alnum = term[:1].isalnum()
    ends_alnum = term[-1:].isalnum()
    if starts_alnum:
        escaped = r"\b" + escaped
    if ends_alnum:
        escaped = escaped + r"\b"
    return re.compile(escaped, re.IGNORECASE)


def _find_hits(text: str, terms: list[str]) -> list[str]:
    return [term for term in terms if _compile_term_pattern(term).search(text)]


def _build_summary(
    posts: list[dict[str, Any]],
    expressions: list[str],
    method_terms: list[str],
    max_matches: int,
) -> dict[str, Any]:
    summary: dict[str, Any] = {
        "expression_contexts": {},
        "global_term_counts": {},
    }

    global_counts: dict[str, int] = defaultdict(int)
    for post in posts:
        hits = _find_hits(post.get("text", ""), method_terms)
        for hit in hits:
            global_counts[hit] += 1
    summary["global_term_counts"] = dict(sorted(global_counts.items(), key=lambda kv: (-kv[1], kv[0])))

    for expression in expressions:
        expr_posts = []
        term_counts: dict[str, int] = defaultdict(int)
        for post in posts:
            text = post.get("text", "")
            if not _match_expression(text, expression):
                continue
            hits = _find_hits(text, method_terms)
            if not hits:
                continue
            for hit in hits:
                term_counts[hit] += 1
            expr_posts.append(
                {
                    "created_at": post.get("created_at"),
                    "hits": hits,
                    "text": text.replace("\n", " "),
                }
            )

        summary["expression_contexts"][expression] = {
            "match_count": len(expr_posts),
            "term_counts": dict(sorted(term_counts.items(), key=lambda kv: (-kv[1], kv[0]))),
            "matches": expr_posts[:max_matches],
        }

    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--archive-json", type=Path, required=True)
    parser.add_argument("--expression", action="append", required=True, help="Ticker without leading $.")
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--max-matches", type=int, default=50)
    parser.add_argument(
        "--method-term",
        action="append",
        help="Additional method/source term to search for. Can be passed multiple times.",
    )
    args = parser.parse_args()

    method_terms = list(DEFAULT_METHOD_TERMS)
    for term in args.method_term or []:
        normalized = term.strip().lower()
        if normalized and normalized not in method_terms:
            method_terms.append(normalized)

    posts = _load_posts(args.archive_json)
    summary = _build_summary(
        posts=posts,
        expressions=[expr.upper() for expr in args.expression],
        method_terms=method_terms,
        max_matches=max(1, args.max_matches),
    )

    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote context summary for {', '.join(args.expression)} to {args.output_json}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
