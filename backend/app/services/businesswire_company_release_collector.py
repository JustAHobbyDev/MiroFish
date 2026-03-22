"""
Fetch and parse Business Wire article pages into company-release records.

This collector is intentionally URL-driven. In this environment, Business Wire's
newsroom index is access-controlled for plain programmatic clients, so the
practical v1 path is:

1. discover or copy known Business Wire article URLs
2. fetch article pages directly
3. normalize them into the existing company_release lane
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

import requests
from bs4 import BeautifulSoup


BUSINESS_WIRE_PUBLISHER = "Business Wire"
BUSINESS_WIRE_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/137.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Cache-Control": "no-cache",
    "Pragma": "no-cache",
}
_TITLE_VERB_SPLIT = re.compile(
    r"\b("
    r"announces|invests|expands|launches|reports|opens|breaks|selects|chooses|"
    r"partners|enters|signs|acquires|receives|unveils|introduces|commits|backs"
    r")\b",
    re.IGNORECASE,
)


class BusinessWireAccessDeniedError(RuntimeError):
    """Raised when Business Wire blocks programmatic access."""


def _coerce_string(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def _clean_text(text: str) -> str:
    return " ".join(text.split())


def _meta_content(soup: BeautifulSoup, *, name: str = "", prop: str = "") -> str:
    if name:
        tag = soup.find("meta", attrs={"name": name})
        if tag and tag.get("content"):
            return _coerce_string(tag.get("content"))
    if prop:
        tag = soup.find("meta", attrs={"property": prop})
        if tag and tag.get("content"):
            return _coerce_string(tag.get("content"))
    return ""


def _extract_json_ld_objects(soup: BeautifulSoup) -> List[Dict[str, Any]]:
    objects: List[Dict[str, Any]] = []
    for script in soup.find_all("script", attrs={"type": "application/ld+json"}):
        raw = script.string or script.get_text()
        if not raw:
            continue
        try:
            parsed = json.loads(raw)
        except json.JSONDecodeError:
            continue
        if isinstance(parsed, dict):
            objects.append(parsed)
        elif isinstance(parsed, list):
            objects.extend(item for item in parsed if isinstance(item, dict))
    return objects


def _json_ld_article(objects: List[Dict[str, Any]]) -> Dict[str, Any]:
    for obj in objects:
        type_value = obj.get("@type")
        types = type_value if isinstance(type_value, list) else [type_value]
        normalized = {_coerce_string(value).lower() for value in types if value}
        if {"newsarticle", "article"} & normalized:
            return obj
    return {}


def _body_from_article_json(article_obj: Dict[str, Any]) -> str:
    body = article_obj.get("articleBody")
    return _clean_text(_coerce_string(body))


def _body_from_html(soup: BeautifulSoup) -> str:
    selectors = [
        "div.bw-release-story p",
        "article p",
        "main p",
        "div[itemprop='articleBody'] p",
    ]
    paragraphs: List[str] = []
    for selector in selectors:
        nodes = soup.select(selector)
        if not nodes:
            continue
        paragraphs = [_clean_text(node.get_text(" ", strip=True)) for node in nodes]
        paragraphs = [item for item in paragraphs if item]
        if paragraphs:
            break
    return "\n\n".join(paragraphs)


def _category_tags(soup: BeautifulSoup) -> List[str]:
    keywords = _meta_content(soup, name="keywords")
    if keywords:
        return [item.strip() for item in keywords.split(",") if item.strip()]
    return []


def _issuer_name(title: str, body_text: str) -> str:
    if ":" in title:
        prefix = _clean_text(title.split(":", 1)[0])
        if 2 <= len(prefix.split()) <= 8:
            return prefix

    verb_match = _TITLE_VERB_SPLIT.search(title)
    if verb_match:
        prefix = _clean_text(title[: verb_match.start()])
        if 1 <= len(prefix.split()) <= 8:
            return prefix

    body_start = _clean_text(body_text.split("\n", 1)[0])
    dateline_match = re.search(r"\)\s*--\s*([A-Z][A-Za-z0-9&.,'()\- ]{2,120}?)\s+(?:announced|today|has|is|will)\b", body_start)
    if dateline_match:
        return _clean_text(dateline_match.group(1))

    return ""


def parse_businesswire_article_html(html: str, *, source_url: str) -> Dict[str, Any]:
    if "Access Denied" in html and "businesswire.com" in source_url:
        raise BusinessWireAccessDeniedError(f"Business Wire blocked access for {source_url}")

    soup = BeautifulSoup(html, "lxml")
    article_obj = _json_ld_article(_extract_json_ld_objects(soup))

    title = (
        _coerce_string(article_obj.get("headline"))
        or _meta_content(soup, prop="og:title")
        or _meta_content(soup, name="title")
        or _clean_text(_coerce_string(getattr(soup.find("h1"), "get_text", lambda *args, **kwargs: "")(" ", strip=True)))
    )

    published_at = (
        _coerce_string(article_obj.get("datePublished"))
        or _meta_content(soup, prop="article:published_time")
        or _coerce_string(getattr(soup.find("time"), "get", lambda *_: "")("datetime"))
    )

    body_text = _body_from_article_json(article_obj) or _body_from_html(soup)
    issuer_name = _issuer_name(title, body_text)
    canonical_url = (
        _coerce_string(getattr(soup.find("link", attrs={"rel": "canonical"}), "get", lambda *_: "")("href"))
        or source_url
    )

    return {
        "source_url": canonical_url,
        "publisher": BUSINESS_WIRE_PUBLISHER,
        "issuer_name": issuer_name,
        "published_at": published_at,
        "title": title,
        "headline": title,
        "categories": _category_tags(soup),
        "body": body_text,
    }


def fetch_businesswire_article(url: str, *, timeout_seconds: float = 20.0) -> Dict[str, Any]:
    response = requests.get(url, headers=BUSINESS_WIRE_HEADERS, timeout=timeout_seconds)
    response.raise_for_status()
    return parse_businesswire_article_html(response.text, source_url=url)


def fetch_businesswire_company_release_records(
    urls: Iterable[str],
    *,
    fetcher: Optional[Any] = None,
) -> List[Dict[str, Any]]:
    fetch_one = fetcher or fetch_businesswire_article
    records: List[Dict[str, Any]] = []
    for url in urls:
        cleaned_url = _coerce_string(url)
        if not cleaned_url:
            continue
        records.append(fetch_one(cleaned_url))
    return records


def _capture_result_html(
    result: Dict[str, Any],
    *,
    capture_root: Optional[Path] = None,
) -> str:
    inline_html = _coerce_string(result.get("article_html"))
    if inline_html:
        return inline_html

    article_path = _coerce_string(result.get("article_path"))
    if not article_path:
        raise ValueError("Business Wire browser capture result is missing article_html and article_path")

    path = Path(article_path)
    if not path.is_absolute():
        if capture_root is None:
            raise ValueError(
                "Business Wire browser capture result uses a relative article_path without a capture_root"
            )
        path = capture_root / path

    return path.read_text(encoding="utf-8")


def build_businesswire_browser_capture_records(
    capture_payload: Dict[str, Any],
    *,
    capture_root: Optional[Path] = None,
) -> List[Dict[str, Any]]:
    results = capture_payload.get("results")
    if not isinstance(results, list):
        raise ValueError("Business Wire browser capture payload must contain a 'results' list")

    records: List[Dict[str, Any]] = []
    for result in results:
        if not isinstance(result, dict):
            continue
        if _coerce_string(result.get("capture_status")) not in {"", "captured"}:
            continue

        html = _capture_result_html(result, capture_root=capture_root)
        source_url = _coerce_string(result.get("article_final_url") or result.get("url"))
        if not source_url:
            raise ValueError("Business Wire browser capture result is missing a source URL")

        record = parse_businesswire_article_html(html, source_url=source_url)
        if not record.get("published_at"):
            record["published_at"] = _coerce_string(result.get("published_label"))
        if _coerce_string(result.get("teaser")):
            record["summary"] = _coerce_string(result.get("teaser"))
        record["capture_result_meta"] = {
            "result_index": result.get("result_index"),
            "search_title": _coerce_string(result.get("title")),
            "search_published_label": _coerce_string(result.get("published_label")),
            "search_teaser": _coerce_string(result.get("teaser")),
        }
        records.append(record)

    return records
