#!/usr/bin/env python3
"""
Fetch an X account timeline into a local JSON artifact for offline analysis.
"""

from __future__ import annotations

import argparse
import json
import os
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

from dotenv import load_dotenv
from requests import HTTPError


ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / ".env", override=False)


def _require_xdk():
    try:
        from xdk import Client
    except ImportError as exc:  # pragma: no cover - exercised at runtime
        raise SystemExit(
            "xdk is not installed. Run `bash ./scripts/backend-uv.sh sync --group dev` first."
        ) from exc
    return Client


def _to_dict(value: Any) -> Any:
    if value is None:
        return None
    if isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, list):
        return [_to_dict(item) for item in value]
    if isinstance(value, tuple):
        return [_to_dict(item) for item in value]
    if isinstance(value, dict):
        return {str(key): _to_dict(item) for key, item in value.items()}
    if hasattr(value, "model_dump"):
        return _to_dict(value.model_dump())
    if hasattr(value, "to_dict"):
        return _to_dict(value.to_dict())
    if hasattr(value, "__dict__"):
        return {
            str(key): _to_dict(item)
            for key, item in vars(value).items()
            if not key.startswith("_")
        }
    return repr(value)


def _collect_terms(values: Iterable[str]) -> list[str]:
    seen: set[str] = set()
    ordered: list[str] = []
    for value in values:
        text = value.strip()
        if not text:
            continue
        lowered = text.lower()
        if lowered in seen:
            continue
        seen.add(lowered)
        ordered.append(text)
    return ordered


def _extract_entities(post: dict[str, Any]) -> dict[str, list[str]]:
    entities = post.get("entities") or {}

    def _pluck(items: Any, key: str) -> list[str]:
        results: list[str] = []
        for item in items or []:
            if not isinstance(item, dict):
                continue
            value = item.get(key)
            if value:
                results.append(str(value))
        return results

    return {
        "cashtags": _pluck(entities.get("cashtags"), "tag"),
        "hashtags": _pluck(entities.get("hashtags"), "tag"),
        "mentions": _pluck(entities.get("mentions"), "username"),
        "urls": _pluck(entities.get("urls"), "expanded_url"),
    }


def _matched_terms(post: dict[str, Any], terms: list[str]) -> list[str]:
    if not terms:
        return []

    haystacks = [post.get("text", "")]
    entity_values = _extract_entities(post)
    for values in entity_values.values():
        haystacks.extend(values)

    merged = "\n".join(str(value) for value in haystacks).lower()
    return [term for term in terms if term.lower() in merged]


@dataclass
class TimelineQuery:
    username: str
    mode: str
    search_query: str | None
    start_time: str | None
    end_time: str | None
    exclude: list[str]
    max_results: int
    max_pages: int | None
    match_terms: list[str]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--username", required=True, help="X username without @")
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument(
        "--mode",
        choices=["user-posts", "search-all"],
        default="search-all",
        help="Use full-archive search or the user posts timeline endpoint.",
    )
    parser.add_argument(
        "--search-query",
        help="Optional explicit full-archive search query. Defaults to from:<username> in search-all mode.",
    )
    parser.add_argument("--start-time", help="ISO8601 UTC lower bound")
    parser.add_argument("--end-time", help="ISO8601 UTC upper bound")
    parser.add_argument(
        "--exclude",
        action="append",
        choices=["retweets", "replies"],
        default=[],
        help="Exclude retweets or replies from the timeline call",
    )
    parser.add_argument("--max-results", type=int, default=100, help="Page size per API request")
    parser.add_argument("--max-pages", type=int, help="Stop after this many pages")
    parser.add_argument(
        "--match-term",
        action="append",
        default=[],
        help="Optional local filter term recorded per post",
    )
    args = parser.parse_args()

    bearer_token = os.environ.get("X_BEARER_TOKEN", "").strip()
    if not bearer_token:
        raise SystemExit("X_BEARER_TOKEN is not set in the environment or .env.")

    Client = _require_xdk()
    client = Client(bearer_token=bearer_token)

    try:
        user_response = client.users.get_by_username(
            username=args.username,
            user_fields=["created_at", "description", "public_metrics", "verified"],
        )
    except HTTPError as exc:
        response = exc.response
        if response is not None and response.status_code == 402:
            raise SystemExit(
                "X API returned 402 Payment Required. The bearer token is valid, but this "
                "project likely does not have paid API usage enabled for the requested "
                "endpoint yet."
            ) from exc
        raise
    user_payload = _to_dict(user_response)
    user_data = (user_payload or {}).get("data") or {}
    user_id = user_data.get("id")
    if not user_id:
        raise SystemExit(f"Could not resolve user id for @{args.username}.")

    match_terms = _collect_terms(args.match_term)
    query = TimelineQuery(
        username=args.username,
        mode=args.mode,
        search_query=args.search_query,
        start_time=args.start_time,
        end_time=args.end_time,
        exclude=args.exclude,
        max_results=max(5, min(500 if args.mode == "search-all" else 100, int(args.max_results))),
        max_pages=args.max_pages,
        match_terms=match_terms,
    )

    posts: list[dict[str, Any]] = []
    page_count = 0
    tweet_fields = [
        "author_id",
        "attachments",
        "conversation_id",
        "created_at",
        "entities",
        "lang",
        "public_metrics",
        "referenced_tweets",
        "text",
    ]
    if query.mode == "search-all":
        search_query = query.search_query or f"from:{args.username}"
        paginator = client.posts.search_all(
            query=search_query,
            max_results=query.max_results,
            start_time=query.start_time,
            end_time=query.end_time,
            tweet_fields=tweet_fields,
        )
    else:
        paginator = client.users.get_posts(
            id=user_id,
            max_results=query.max_results,
            start_time=query.start_time,
            end_time=query.end_time,
            exclude=query.exclude or None,
            tweet_fields=tweet_fields,
        )

    try:
        for page in paginator:
            page_payload = _to_dict(page)
            page_data = (page_payload or {}).get("data") or []
            for post in page_data:
                entities = _extract_entities(post)
                matched_terms = _matched_terms(post, match_terms)
                posts.append(
                    {
                        "id": post.get("id"),
                        "created_at": post.get("created_at"),
                        "text": post.get("text", ""),
                        "conversation_id": post.get("conversation_id"),
                        "lang": post.get("lang"),
                        "author_id": post.get("author_id"),
                        "public_metrics": post.get("public_metrics") or {},
                        "referenced_tweets": post.get("referenced_tweets") or [],
                        "entities": entities,
                        "matched_terms": matched_terms,
                    }
                )
            page_count += 1
            if query.max_pages and page_count >= query.max_pages:
                break
    except HTTPError as exc:
        response = exc.response
        if response is not None and response.status_code == 429:
            raise SystemExit(
                "X API returned 429 Too Many Requests while fetching posts. Narrow the "
                "query, reduce page count, or wait for the rate window to reset."
            ) from exc
        if response is not None and response.status_code == 402:
            raise SystemExit(
                "X API returned 402 Payment Required while fetching posts. Paid usage is "
                "not fully enabled for this project yet."
            ) from exc
        raise

    filtered_posts = [
        post for post in posts if not match_terms or post.get("matched_terms")
    ]

    payload = {
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "query": asdict(query),
        "user": user_data,
        "page_count": page_count,
        "post_count": len(posts),
        "matched_post_count": len(filtered_posts),
        "posts": posts,
        "matched_posts": filtered_posts,
    }

    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(
        f"Wrote {len(posts)} posts for @{args.username} "
        f"({len(filtered_posts)} matched) to {args.output_json}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
