"""
Deterministic bounded research-set formation from bounded-universe expansion plans.
"""

from __future__ import annotations

import hashlib
import re
from typing import Any, Dict, Iterable, List, Tuple


STOPWORDS = {
    "and",
    "for",
    "with",
    "from",
    "into",
    "that",
    "this",
    "will",
    "their",
    "about",
    "demand",
    "buildout",
    "expansion",
    "growth",
    "system",
    "systems",
    "infrastructure",
    "manufacturing",
    "equipment",
    "utility",
    "utilities",
    "production",
    "factory",
    "plant",
    "facility",
    "facilities",
    "projects",
    "project",
}

ENTITY_VERBS = (
    "invests",
    "invest",
    "expands",
    "commits",
    "breaks",
    "adds",
    "raises",
    "reports",
    "jumps",
    "soars",
    "expects",
    "inks",
    "advances",
    "picks",
    "selects",
    "confirms",
    "boosts",
    "opens",
    "launches",
    "signs",
    "announces",
    "unveils",
)


def _coerce_string(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def _research_set_id(system_label: str, as_of_date: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "_", system_label.lower()).strip("_")
    suffix = as_of_date or "unknown_date"
    digest = hashlib.sha1(f"{slug}|{suffix}".encode("utf-8")).hexdigest()[:8]
    return f"brs_{slug}_{suffix}_{digest}"


def _artifact_iter(prefilter_batches: Iterable[Dict[str, Any]]) -> List[Dict[str, Any]]:
    items: List[Dict[str, Any]] = []
    for batch in prefilter_batches:
        for key in ("kept_artifacts", "review_artifacts"):
            items.extend(dict(artifact) for artifact in batch.get(key, []))
    return items


def _term_keywords(terms: Iterable[str]) -> List[str]:
    keywords: List[str] = []
    for term in terms:
        for token in re.findall(r"[a-z0-9]+", _coerce_string(term).lower()):
            if len(token) < 4 or token in STOPWORDS:
                continue
            if token not in keywords:
                keywords.append(token)
    return keywords


def _artifact_text(artifact: Dict[str, Any]) -> str:
    return " ".join(
        [
            _coerce_string(artifact.get("title")),
            _coerce_string(artifact.get("subheadline")),
            _coerce_string(artifact.get("deck")),
            _coerce_string(artifact.get("body_text")),
            " ".join(artifact.get("category_tags", [])),
            _coerce_string(artifact.get("section_name")),
        ]
    ).lower()


def _anchor_keywords(plan: Dict[str, Any]) -> List[str]:
    anchors: List[str] = []
    source_text = " ".join(
        [
            _coerce_string(plan.get("system_label")),
            *[_coerce_string(item) for item in plan.get("suspected_stress_layers", [])],
        ]
    )
    for token in re.findall(r"[a-z0-9]+", source_text.lower()):
        if len(token) < 4 or token in STOPWORDS:
            continue
        if token not in anchors:
            anchors.append(token)
    return anchors


def _extract_entity_hint(artifact: Dict[str, Any]) -> str:
    issuer = _coerce_string(artifact.get("issuing_company_name"))
    if issuer:
        return issuer
    title = _coerce_string(artifact.get("title"))
    if not title:
        return ""
    patterns = [
        r"([A-Z][A-Za-z0-9&'.-]+(?: [A-Z][A-Za-z0-9&'.-]+){0,4}(?: subsidiary)?) (?:%s)\b"
        % "|".join(ENTITY_VERBS),
        r"([A-Z][A-Za-z0-9&'.-]+(?: [A-Z][A-Za-z0-9&'.-]+){0,4}(?: subsidiary)?) to (?:build|expand|invest)\b",
    ]
    for pattern in patterns:
        match = re.search(pattern, title)
        if not match:
            continue
        entity = match.group(1).strip(" ,:-")
        entity = re.sub(r"^[A-Z][a-z]+-based\s+", "", entity)
        entity = re.sub(r"\s+subsidiary$", "", entity, flags=re.IGNORECASE)
        return entity
    return ""


def _score_artifact(plan: Dict[str, Any], artifact: Dict[str, Any]) -> Tuple[int, List[str], List[str]]:
    text = _artifact_text(artifact)
    positive_terms = list(plan.get("query_seed_terms", [])) + list(plan.get("suspected_stress_layers", []))
    negative_terms = list(plan.get("negative_boundaries", []))
    anchor_hits = sorted({kw for kw in _anchor_keywords(plan) if kw in text})
    phrase_hits = sorted({term for term in positive_terms if _coerce_string(term).lower() in text})
    keyword_hits = sorted({kw for kw in _term_keywords(positive_terms) if kw in text})
    negative_hits = sorted({term for term in negative_terms if _coerce_string(term).lower() in text})

    score = len(phrase_hits) * 3 + len(keyword_hits)
    if not anchor_hits and not phrase_hits:
        return 0, [], negative_hits
    if negative_hits and score < 6:
        return 0, anchor_hits + phrase_hits + keyword_hits, negative_hits
    if phrase_hits or len(keyword_hits) >= 3 or (anchor_hits and keyword_hits):
        return score + len(anchor_hits), anchor_hits + phrase_hits + keyword_hits, negative_hits
    return 0, phrase_hits + keyword_hits, negative_hits


def _entity_candidates(matches: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    grouped: Dict[str, Dict[str, Any]] = {}
    for match in matches:
        entity_name = _coerce_string(match.get("entity_hint"))
        if not entity_name:
            continue
        current = grouped.setdefault(
            entity_name,
            {
                "entity_name": entity_name,
                "source_classes": set(),
                "artifact_ids": [],
            },
        )
        current["source_classes"].add(_coerce_string(match.get("source_class")))
        current["artifact_ids"].append(_coerce_string(match.get("artifact_id")))

    output: List[Dict[str, Any]] = []
    for entity_name, payload in grouped.items():
        artifact_ids = sorted({item for item in payload["artifact_ids"] if item})
        output.append(
            {
                "entity_name": entity_name,
                "source_classes": sorted({item for item in payload["source_classes"] if item}),
                "artifact_support_count": len(artifact_ids),
                "artifact_ids": artifact_ids,
            }
        )
    output.sort(key=lambda item: (-item["artifact_support_count"], item["entity_name"]))
    return output


def build_bounded_research_set_batch(
    expansion_batch: Dict[str, Any],
    prefilter_batches: List[Dict[str, Any]],
) -> Dict[str, Any]:
    artifacts = _artifact_iter(prefilter_batches)
    research_sets: List[Dict[str, Any]] = []

    for plan in expansion_batch.get("plans", []):
        matches: List[Dict[str, Any]] = []
        for artifact in artifacts:
            source_class = _coerce_string(artifact.get("source_class"))
            if source_class and source_class not in set(plan.get("source_classes_priority", [])):
                continue
            score, matched_terms, negative_hits = _score_artifact(plan, artifact)
            if score <= 0:
                continue
            matches.append(
                {
                    "artifact_id": _coerce_string(artifact.get("artifact_id")),
                    "source_class": source_class,
                    "title": _coerce_string(artifact.get("title")),
                    "source_url": _coerce_string(artifact.get("source_url")),
                    "entity_hint": _extract_entity_hint(artifact),
                    "match_score": score,
                    "matched_terms": matched_terms,
                    "negative_hits": negative_hits,
                }
            )

        matches.sort(key=lambda item: (-item["match_score"], item["artifact_id"]))
        research_sets.append(
            {
                "bounded_research_set_id": _research_set_id(
                    _coerce_string(plan.get("system_label")),
                    _coerce_string(plan.get("as_of_date")),
                ),
                "as_of_date": _coerce_string(plan.get("as_of_date")),
                "status": "candidate",
                "origin_bounded_universe_expansion_plan_id": _coerce_string(
                    plan.get("bounded_universe_expansion_plan_id")
                ),
                "system_label": _coerce_string(plan.get("system_label")),
                "matched_artifacts": matches,
                "matched_artifact_ids": [item["artifact_id"] for item in matches],
                "entity_candidates": _entity_candidates(matches),
                "coverage_metrics": {
                    "matched_artifact_count": len(matches),
                    "matched_source_classes": sorted(
                        {item["source_class"] for item in matches if item["source_class"]}
                    ),
                    "entity_candidate_count": len(_entity_candidates(matches)),
                },
                "source_classes_priority": list(plan.get("source_classes_priority", [])),
                "suspected_stress_layers": list(plan.get("suspected_stress_layers", [])),
                "confidence": _coerce_string(plan.get("confidence")) or "low",
            }
        )

    return {
        "name": "bounded_research_set_batch_v1",
        "research_sets": research_sets,
        "metrics": {
            "input_expansion_plan_count": len(expansion_batch.get("plans", [])),
            "bounded_research_set_count": len(research_sets),
        },
    }
