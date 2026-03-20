#!/usr/bin/env python3
"""
Backfill an X account's public post archive day by day using full-archive search.
"""

from __future__ import annotations

import argparse
import json
import os
import time
from datetime import date, datetime, time as dt_time, timedelta, timezone
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from requests import HTTPError


ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / ".env", override=False)

TWEET_FIELDS = [
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


def _require_xdk():
    try:
        from xdk import Client
    except ImportError as exc:  # pragma: no cover
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


def _parse_date(value: str) -> date:
    return date.fromisoformat(value)


def _iso_utc(day: date) -> str:
    return datetime.combine(day, dt_time.min, tzinfo=timezone.utc).isoformat().replace("+00:00", "Z")


def _iso_datetime(value: datetime) -> str:
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def _extract_entities(post: dict[str, Any]) -> dict[str, list[str]]:
    entities = post.get("entities") or {}

    def _pluck(items: Any, key: str) -> list[str]:
        results: list[str] = []
        for item in items or []:
            if isinstance(item, dict) and item.get(key):
                results.append(str(item[key]))
        return results

    return {
        "cashtags": _pluck(entities.get("cashtags"), "tag"),
        "hashtags": _pluck(entities.get("hashtags"), "tag"),
        "mentions": _pluck(entities.get("mentions"), "username"),
        "urls": _pluck(entities.get("urls"), "expanded_url"),
    }


def _normalize_post(post: dict[str, Any], *, bucket_date: str) -> dict[str, Any]:
    return {
        "id": post.get("id"),
        "created_at": post.get("created_at"),
        "text": post.get("text", ""),
        "conversation_id": post.get("conversation_id"),
        "lang": post.get("lang"),
        "author_id": post.get("author_id"),
        "public_metrics": post.get("public_metrics") or {},
        "referenced_tweets": post.get("referenced_tweets") or [],
        "entities": _extract_entities(post),
        "bucket_date": bucket_date,
    }


def _load_existing(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def _write_payload(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--username", required=True, help="X username without @")
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--start-date", help="YYYY-MM-DD lower bound; defaults to account creation date")
    parser.add_argument("--end-date", help="YYYY-MM-DD upper bound; defaults to today UTC")
    parser.add_argument("--max-results", type=int, default=100, help="Per-request page size (max 500)")
    parser.add_argument("--max-pages-per-day", type=int, default=10)
    parser.add_argument("--sleep-seconds", type=float, default=4.0)
    parser.add_argument("--resume", action="store_true", help="Resume from an existing output artifact")
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
                "X API returned 402 Payment Required. Paid usage is not fully enabled for this project yet."
            ) from exc
        raise

    user_payload = _to_dict(user_response)
    user_data = (user_payload or {}).get("data") or {}
    if not user_data.get("id"):
        raise SystemExit(f"Could not resolve user id for @{args.username}.")

    created_date = datetime.fromisoformat(user_data["created_at"].replace("Z", "+00:00")).date()
    now_utc = datetime.now(timezone.utc)
    start_date = _parse_date(args.start_date) if args.start_date else created_date
    end_date = _parse_date(args.end_date) if args.end_date else (now_utc.date() - timedelta(days=1))
    if start_date > end_date:
        raise SystemExit("start-date must be on or before end-date.")

    payload = {
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "mode": "search-all-daily",
        "username": args.username,
        "user": user_data,
        "start_date": start_date.isoformat(),
        "end_date": end_date.isoformat(),
        "days_completed": [],
        "stopped_early": False,
        "stop_reason": "",
        "posts": [],
    }
    seen_post_ids: set[str] = set()

    if args.resume and args.output_json.exists():
        existing = _load_existing(args.output_json)
        if existing:
            payload.update(existing)
            seen_post_ids = {post["id"] for post in existing.get("posts", []) if post.get("id")}

    completed_days = set(payload.get("days_completed", []))
    posts = list(payload.get("posts", []))

    current_day = end_date
    while current_day >= start_date:
        bucket = current_day.isoformat()
        if bucket in completed_days:
            current_day -= timedelta(days=1)
            continue

        window_start = _iso_utc(current_day)
        bucket_end = datetime.combine(current_day + timedelta(days=1), dt_time.min, tzinfo=timezone.utc)
        window_end = _iso_datetime(bucket_end)
        day_post_count = 0
        page_count = 0

        try:
            paginator = client.posts.search_all(
                query=f"from:{args.username}",
                start_time=window_start,
                end_time=window_end,
                max_results=max(10, min(500, int(args.max_results))),
                tweet_fields=TWEET_FIELDS,
            )

            for page in paginator:
                page_payload = _to_dict(page)
                page_data = (page_payload or {}).get("data") or []
                for raw_post in page_data:
                    normalized = _normalize_post(raw_post, bucket_date=bucket)
                    post_id = normalized.get("id")
                    if post_id and post_id not in seen_post_ids:
                        posts.append(normalized)
                        seen_post_ids.add(post_id)
                    day_post_count += 1
                page_count += 1
                if page_count >= args.max_pages_per_day:
                    break
        except HTTPError as exc:
            response = exc.response
            payload["stopped_early"] = True
            if response is not None and response.status_code == 429:
                payload["stop_reason"] = (
                    f"rate_limited_on_{bucket}; wait for rate window reset and rerun with --resume"
                )
            else:
                payload["stop_reason"] = f"request_failed_on_{bucket}: {exc}"
            payload["posts"] = sorted(posts, key=lambda post: post["created_at"])
            _write_payload(args.output_json, payload)
            raise SystemExit(payload["stop_reason"]) from exc

        completed_days.add(bucket)
        payload["days_completed"] = sorted(completed_days)
        payload["posts"] = sorted(posts, key=lambda post: post["created_at"])
        payload["fetched_at"] = datetime.now(timezone.utc).isoformat()
        payload["stopped_early"] = False
        payload["stop_reason"] = ""
        _write_payload(args.output_json, payload)
        print(f"{bucket}: {day_post_count} posts across {page_count} pages")

        current_day -= timedelta(days=1)
        if args.sleep_seconds > 0:
            time.sleep(args.sleep_seconds)

    print(
        f"Wrote {len(posts)} deduped posts for @{args.username} "
        f"covering {len(completed_days)} days to {args.output_json}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
