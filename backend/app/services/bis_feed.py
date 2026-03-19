"""
Live BIS feed retrieval and normalization.

This service fetches the BIS homepage, extracts policy-relevant items from the
`Special Issues` and `News & Updates` sections, and normalizes the result into
the `policy_feed` contract consumed by the policy feed connector.
"""

from __future__ import annotations

from datetime import datetime, timezone
from html.parser import HTMLParser
import logging
import re
from typing import Any, Dict, Iterable, List, Optional
from urllib.parse import urljoin
from urllib.request import Request, urlopen

from .federal_register_query_profiles import resolve_query_profile
from .federal_register_relevance import (
    filter_documents_by_relevance,
    match_process_layers,
)

logger = logging.getLogger(__name__)


BIS_BASE_URL = "https://media.bis.gov"
BIS_HOMEPAGE_URL = f"{BIS_BASE_URL}/"
BIS_SOURCE_TARGET_ID = "src_target_bis_updates"
BIS_SOURCE_TARGET_NAME = "Bureau of Industry and Security (BIS), U.S. Department of Commerce"
_MONTH_PATTERN = (
    r"(January|February|March|April|May|June|July|August|September|October|"
    r"November|December)\s+\d{1,2},\s+\d{4}"
)


def _normalize_list(value: Any) -> List[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def _iso_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _normalize_space(value: str) -> str:
    return re.sub(r"\s+", " ", value or "").strip()


def _extract_date(value: str) -> str:
    match = re.search(_MONTH_PATTERN, value or "")
    if not match:
        return ""
    try:
        return datetime.strptime(match.group(0), "%B %d, %Y").date().isoformat()
    except ValueError:
        return ""


def _matches_query(text: str, query: str) -> bool:
    normalized_text = _normalize_space(text).lower()
    normalized_query = _normalize_space(query).lower()
    if not normalized_query:
        return True
    if normalized_query in normalized_text:
        return True

    terms = re.findall(r"[a-z0-9]+", normalized_query)
    significant_terms = [term for term in terms if len(term) >= 3]
    if not significant_terms:
        return True

    matched_terms = sum(1 for term in significant_terms if term in normalized_text)
    required_matches = max(1, (len(significant_terms) + 1) // 2)
    return matched_terms >= required_matches


def _passes_date_filters(
    published_at: str,
    *,
    published_gte: str | None,
    published_lte: str | None,
) -> bool:
    if not published_at:
        return True
    if published_gte and published_at < published_gte:
        return False
    if published_lte and published_at > published_lte:
        return False
    return True


class _BisHomepageParser(HTMLParser):
    """Capture heading, text, and link events in document order."""

    _BLOCK_TAGS = {
        "article",
        "br",
        "div",
        "h1",
        "h2",
        "h3",
        "h4",
        "h5",
        "h6",
        "li",
        "p",
        "section",
        "span",
        "ul",
    }

    def __init__(self) -> None:
        super().__init__()
        self.events: List[Dict[str, Any]] = []
        self._text_parts: List[str] = []
        self._heading_tag: str | None = None
        self._heading_parts: List[str] = []
        self._link_href: str | None = None
        self._link_parts: List[str] = []
        self._skip_depth = 0

    def handle_starttag(self, tag: str, attrs: List[tuple[str, str | None]]) -> None:
        if tag in {"script", "style"}:
            self._skip_depth += 1
            return
        if self._skip_depth:
            return
        if tag in self._BLOCK_TAGS:
            self._flush_text()
        if tag in {"h1", "h2", "h3", "h4", "h5", "h6"}:
            self._flush_text()
            self._heading_tag = tag
            self._heading_parts = []
            return
        if tag == "a":
            self._flush_text()
            attrs_map = dict(attrs)
            self._link_href = attrs_map.get("href") or ""
            self._link_parts = []

    def handle_endtag(self, tag: str) -> None:
        if tag in {"script", "style"} and self._skip_depth:
            self._skip_depth -= 1
            return
        if self._skip_depth:
            return
        if tag == self._heading_tag:
            text = _normalize_space("".join(self._heading_parts))
            if text:
                self.events.append(
                    {
                        "type": "heading",
                        "level": int(tag[1]),
                        "text": text,
                    }
                )
            self._heading_tag = None
            self._heading_parts = []
            return
        if tag == "a" and self._link_href is not None:
            text = _normalize_space("".join(self._link_parts))
            if text:
                self.events.append(
                    {
                        "type": "link",
                        "text": text,
                        "href": self._link_href,
                    }
                )
            self._link_href = None
            self._link_parts = []
            return
        if tag in self._BLOCK_TAGS:
            self._flush_text()

    def handle_data(self, data: str) -> None:
        if self._skip_depth:
            return
        if self._heading_tag is not None:
            self._heading_parts.append(data)
            return
        if self._link_href is not None:
            self._link_parts.append(data)
            return
        self._text_parts.append(data)

    def close(self) -> None:
        super().close()
        self._flush_text()

    def _flush_text(self) -> None:
        text = _normalize_space("".join(self._text_parts))
        if text:
            self.events.append({"type": "text", "text": text})
        self._text_parts = []


def _pick_canonical_link(links: List[Dict[str, str]]) -> str:
    for link in links:
        href = link.get("href", "")
        if not href:
            continue
        return urljoin(BIS_BASE_URL, href)
    return BIS_HOMEPAGE_URL


def _is_noise_item(item: Dict[str, Any]) -> bool:
    title = _normalize_space(str(item.get("title", ""))).lower()
    summary = _normalize_space(str(item.get("summary", ""))).lower()
    canonical_url = str(item.get("canonical_url", "")).lower()
    published_at = str(item.get("published_at", ""))

    if not title:
        return True
    if title.startswith("share to "):
        return True
    if title in {"bis forms", "contact bis", "email updates"}:
        return True
    if "/external/external" in canonical_url:
        return True
    if "/licensing/bis-forms" in canonical_url:
        return True
    if not published_at and summary == title:
        return True
    return False


def parse_bis_homepage_items(html: str) -> List[Dict[str, Any]]:
    parser = _BisHomepageParser()
    parser.feed(html)
    parser.close()

    items: List[Dict[str, Any]] = []
    current_section: str | None = None
    current_item: Dict[str, Any] | None = None

    def flush_current() -> None:
        nonlocal current_item
        if not current_item:
            return
        summary = _normalize_space(" ".join(current_item.pop("summary_parts", [])))
        current_item["summary"] = summary
        current_item["excerpt"] = summary or current_item["title"]
        current_item["canonical_url"] = _pick_canonical_link(current_item.pop("links", []))
        if not current_item.get("published_at"):
            current_item["published_at"] = _extract_date(summary)
        items.append(current_item)
        current_item = None

    for event in parser.events:
        event_type = event["type"]
        if event_type == "heading":
            heading_text = event["text"].lower()
            heading_level = int(event["level"])
            if heading_level <= 2:
                if heading_text == "special issues":
                    flush_current()
                    current_section = "special_issue"
                    continue
                if heading_text == "read the latest news & updates":
                    flush_current()
                    current_section = "news_update"
                    continue
                if current_section in {"special_issue", "news_update"}:
                    flush_current()
                    current_section = None
                    continue
            if current_section == "special_issue" and heading_level == 4:
                flush_current()
                current_item = {
                    "title": event["text"],
                    "section": current_section,
                    "summary_parts": [],
                    "links": [],
                    "published_at": "",
                }
                continue
        if current_section == "special_issue":
            if not current_item:
                continue
            if event_type == "text":
                current_item["summary_parts"].append(event["text"])
            elif event_type == "link":
                current_item["links"].append(event)
        elif current_section == "news_update":
            if event_type == "link":
                flush_current()
                title = event["text"]
                if title.lower().startswith("see more news"):
                    continue
                current_item = {
                    "title": title,
                    "section": current_section,
                    "summary_parts": [],
                    "links": [event],
                    "published_at": "",
                }
            elif current_item and event_type == "text":
                if not current_item["published_at"]:
                    maybe_date = _extract_date(event["text"])
                    if maybe_date:
                        current_item["published_at"] = maybe_date
                        continue
                current_item["summary_parts"].append(event["text"])

    flush_current()
    return items


def _fetch_html(url: str, *, timeout_seconds: int = 20) -> str:
    request = Request(
        url,
        headers={
            "Accept": "text/html,application/xhtml+xml",
            "User-Agent": "MiroFish BISConnector/1.0",
        },
    )
    with urlopen(request, timeout=timeout_seconds) as response:
        return response.read().decode("utf-8")


def _normalize_item_to_policy_feed(
    item: Dict[str, Any],
    *,
    target_themes: Iterable[str],
    focus_process_layers: Iterable[str],
    focus_geographies: Iterable[str],
    ticker_refs: Iterable[str],
    policy_scope: Iterable[str],
    relevance_metadata: Optional[Dict[str, Any]] = None,
    matched_process_layers: Optional[List[str]] = None,
    matched_profile: Optional[str] = None,
) -> Dict[str, Any]:
    title = item.get("title") or "Untitled BIS update"
    section = item.get("section") or "news_update"
    document_key = re.sub(r"[^a-z0-9]+", "_", title.lower()).strip("_") or "bis_update"
    process_layers = matched_process_layers or [str(value) for value in _normalize_list(focus_process_layers)]
    geographies = [str(value) for value in _normalize_list(focus_geographies)]
    themes = [str(value) for value in _normalize_list(target_themes)]
    relevance = relevance_metadata or {}
    relevance_class = relevance.get("relevance_class", "directly_relevant")
    is_adjacent = relevance_class == "adjacent"
    rel_strength = "low" if is_adjacent else "high"
    rel_confidence = "low" if is_adjacent else "medium"

    relationship_hints: List[Dict[str, Any]] = []
    for process_layer in process_layers:
        relationship_hints.append(
            {
                "key": f"{document_key}_affected_{process_layer}",
                "relationship_type": "AFFECTED_BY_EVENT",
                "source_type": "ProcessLayer",
                "source_name": process_layer,
                "target_type": "Event",
                "target_name": title,
                "relationship_strength": rel_strength,
                "confidence": rel_confidence,
            }
        )
        if not is_adjacent:
            for geography in geographies:
                relationship_hints.append(
                    {
                        "key": f"{document_key}_constrained_{process_layer}_{geography}",
                        "relationship_type": "CONSTRAINED_BY",
                        "source_type": "ProcessLayer",
                        "source_name": process_layer,
                        "target_type": "Geography",
                        "target_name": geography,
                        "relationship_strength": "medium",
                        "confidence": "medium",
                    }
                )

    entity_hints: List[Dict[str, Any]] = [
        {
            "entity_type": "Event",
            "canonical_name": title,
            "attributes": {
                "event_type": section,
                "publisher": "Bureau of Industry and Security",
            },
            "confidence": "high",
        }
    ]
    entity_hints.extend(
        {
            "entity_type": "ProcessLayer",
            "canonical_name": process_layer,
            "attributes": {"process_stage": "policy_affected"},
            "confidence": "medium",
        }
        for process_layer in process_layers
    )
    entity_hints.extend(
        {
            "entity_type": "Geography",
            "canonical_name": geography,
            "confidence": "medium",
        }
        for geography in geographies
    )
    entity_hints.extend(
        {
            "entity_type": "Theme",
            "canonical_name": theme.replace("_", " ").title(),
            "confidence": "medium",
        }
        for theme in themes
    )

    summary = item.get("summary") or title
    claim_candidates = []
    if process_layers:
        claim_candidates.append(
            {
                "claim_key": f"claim_{document_key}_bis_update_affects_process_layers",
                "claim_type": "policy_transmission_assertion",
                "claim_text": (
                    f"{title} may affect {', '.join(process_layers)} before downstream market narratives update."
                ),
                "claim_status": "supported",
                "claim_kind": "inferential",
                "confidence": "medium",
                "entity_names": [title, *process_layers, *geographies],
                "relationship_keys": [relationship["key"] for relationship in relationship_hints],
            }
        )

    return {
        "document_id": f"bis_{document_key}",
        "source_target_id": BIS_SOURCE_TARGET_ID,
        "source_target_name": BIS_SOURCE_TARGET_NAME,
        "source_class": "government_policy_enforcement",
        "publisher": "Bureau of Industry and Security",
        "title": title,
        "canonical_url": item.get("canonical_url") or BIS_HOMEPAGE_URL,
        "published_at": item.get("published_at", ""),
        "retrieved_at": _iso_now(),
        "source_quality": "high",
        "source_reliability_score": 0.94,
        "usage_mode": "evidence",
        "attachment_type": "html",
        "jurisdiction": "US",
        "language": "en",
        "ticker_refs": [str(value).upper() for value in _normalize_list(ticker_refs)],
        "theme_refs": themes,
        "policy_scope": [str(value) for value in _normalize_list(policy_scope)],
        "summary": summary,
        "excerpt": item.get("excerpt") or summary,
        "research_tags": {
            "themes": [theme.replace("_", " ").title() for theme in themes],
            "process_layers": process_layers,
            "geographies": geographies,
            "bis_sections": [section],
        },
        "entity_hints": entity_hints,
        "relationship_hints": relationship_hints,
        "claim_candidates": claim_candidates,
        "relevance_score": relevance.get("relevance_score"),
        "relevance_class": relevance_class,
        "positive_markers": relevance.get("positive_markers", []),
        "negative_markers": relevance.get("negative_markers", []),
        "matched_profile": matched_profile,
        "matched_process_layers": process_layers,
        "notes": [
            "Normalized from live BIS website response.",
            f"Section: {section}",
            *(
                [f"Relevance: {relevance_class} ({relevance.get('relevance_score', '?')})"]
                if relevance
                else []
            ),
        ],
    }


def fetch_bis_policy_feed(
    *,
    query_profile: Optional[str] = None,
    query: str = "",
    published_gte: str | None = None,
    published_lte: str | None = None,
    per_page: int = 20,
    page: int = 1,
    target_themes: Iterable[str] | None = None,
    focus_process_layers: Iterable[str] | None = None,
    focus_geographies: Iterable[str] | None = None,
    ticker_refs: Iterable[str] | None = None,
    policy_scope: Iterable[str] | None = None,
    minimum_relevance_score: int = 20,
    include_adjacent: bool = True,
    positive_markers: Iterable[str] | None = None,
    negative_markers: Iterable[str] | None = None,
) -> Dict[str, Any]:
    caller_explicit_layers = list(focus_process_layers) if focus_process_layers else []

    resolved = resolve_query_profile(
        query_profile,
        overrides={
            "query": query or None,
            "target_themes": list(target_themes) if target_themes else None,
            "focus_process_layers": list(focus_process_layers) if focus_process_layers else None,
            "focus_geographies": list(focus_geographies) if focus_geographies else None,
            "ticker_refs": list(ticker_refs) if ticker_refs else None,
            "policy_scope": list(policy_scope) if policy_scope else None,
        },
    )
    effective_query = resolved.get("query", query) or ""
    effective_target_themes = resolved.get("target_themes") or []
    effective_process_layers = resolved.get("focus_process_layers") or []
    effective_geographies = resolved.get("focus_geographies") or []
    effective_tickers = resolved.get("ticker_refs") or []
    effective_policy_scope = resolved.get("policy_scope") or []
    effective_positive = list(positive_markers) if positive_markers else resolved.get("positive_markers")
    effective_negative = list(negative_markers) if negative_markers else resolved.get("negative_markers")

    html = _fetch_html(BIS_HOMEPAGE_URL)
    raw_items = parse_bis_homepage_items(html)

    filtered_items = [
        {
            **item,
            "abstract": item.get("summary", ""),
            "topics": [item.get("section", "")],
        }
        for item in raw_items
        if not _is_noise_item(item)
        and _matches_query(f"{item.get('title', '')} {item.get('summary', '')}", effective_query)
        and _passes_date_filters(
            item.get("published_at", ""),
            published_gte=published_gte,
            published_lte=published_lte,
        )
    ]

    start = max(page - 1, 0) * max(per_page, 1)
    end = start + max(per_page, 1)
    paged_items = filtered_items[start:end]

    scored_items = filter_documents_by_relevance(
        paged_items,
        minimum_score=minimum_relevance_score,
        include_adjacent=include_adjacent,
        positive_markers=effective_positive,
        negative_markers=effective_negative,
    )

    documents = []
    for item in scored_items:
        relevance = item.pop("_relevance", {})
        doc_layers = match_process_layers(
            item,
            effective_process_layers,
            explicit_layers=caller_explicit_layers,
        )
        documents.append(
            _normalize_item_to_policy_feed(
                item,
                target_themes=effective_target_themes,
                focus_process_layers=effective_process_layers,
                focus_geographies=effective_geographies,
                ticker_refs=effective_tickers,
                policy_scope=effective_policy_scope,
                relevance_metadata=relevance,
                matched_process_layers=doc_layers,
                matched_profile=query_profile,
            )
        )

    notes = ["Fetched from BIS website homepage."]
    if query_profile:
        notes.append(f"Query profile: {query_profile}")
    if effective_query:
        notes.append(f"Query: {effective_query}")
    return {
        "name": "bis_policy_feed_live_v1",
        "theme": next(iter(effective_target_themes), ""),
        "synthetic_sample": False,
        "notes": notes,
        "feed_documents": documents,
        "fetch_metadata": {
            "api_url": BIS_HOMEPAGE_URL,
            "raw_result_count": len(raw_items),
            "candidate_count": len(filtered_items),
            "result_count": len(documents),
            "filtered_out": len(filtered_items) - len(documents),
            "retrieved_at": _iso_now(),
            "query_profile": query_profile or None,
            "minimum_relevance_score": minimum_relevance_score,
            "include_adjacent": include_adjacent,
        },
    }
