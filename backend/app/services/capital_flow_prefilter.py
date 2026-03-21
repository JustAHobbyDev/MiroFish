"""
Deterministic event-form prefilter for capital-flow-oriented archive collection.

This module is intentionally shallow. It only inspects allowed metadata fields
such as title, headline, deck, section name, and tags. It does not inspect full
body text and does not use any historical or cluster context.
"""

from __future__ import annotations

import re
from typing import Any, Dict, Iterable, List, Tuple


TRIAGE_KEEP = "keep"
TRIAGE_REVIEW = "review"
TRIAGE_DROP = "drop"

STRONG_FIELDS = ("title", "headline", "subheadline", "deck")
MEDIUM_FIELDS = ("section_name", "category_tags")
WEAK_FIELDS = ("publisher_metadata",)
ALLOWED_FIELDS = STRONG_FIELDS + MEDIUM_FIELDS + WEAK_FIELDS


EVENT_FORM_FAMILIES: Dict[str, Tuple[str, ...]] = {
    "awards_and_funding": (
        "award",
        "awarded",
        "grant",
        "grants",
        "loan",
        "loans",
        "subsidy",
        "subsidies",
        "funding",
        "financing",
        "incentive",
        "tax credit",
        "loan guarantee",
    ),
    "contracts_and_orders": (
        "contract",
        "contracts",
        "order",
        "orders",
        "bookings",
        "purchase order",
        "procurement",
        "supply agreement",
        "offtake",
        "framework agreement",
    ),
    "facility_and_capacity_expansion": (
        "expand",
        "expansion",
        "capacity",
        "capacity increase",
        "new facility",
        "new plant",
        "new fab",
        "new line",
        "ramp",
        "scale-up",
        "manufacturing buildout",
    ),
    "construction_and_deployment": (
        "groundbreaking",
        "construction",
        "buildout",
        "deployment",
        "rollout",
        "commissioning",
        "opening",
        "operational",
        "start of operations",
    ),
    "partnerships_with_buildout_implications": (
        "partnership",
        "collaboration",
        "joint venture",
        "strategic agreement",
        "manufacturing agreement",
        "supply partnership",
    ),
    "planning_and_land_access_enablement": (
        "record of decision",
        "integrated activity plan",
        "public land order",
        "land opening",
        "lease sale",
    ),
}


EVENT_FORM_REGEXES: Dict[str, Tuple[str, ...]] = {
    "awards_and_funding": (
        r"\baward(?:ed|s)?\b",
        r"\bgrant(?:ed|s)?\b",
        r"\bloan(?:s|ed)?\b",
        r"\bsubsid(?:y|ies|ized|ising)\b",
        r"\bfinanc(?:e|ing|ed)\b",
        r"\btax credit\b",
        r"\bloan guarantee\b",
    ),
    "contracts_and_orders": (
        r"\bcontract(?:s|ed)?\b",
        r"\border(?:s|ed)?\b",
        r"\bbooking(?:s)?\b",
        r"\bpurchase order(?:s)?\b",
        r"\bprocurement\b",
        r"\bsupply agreement(?:s)?\b",
        r"\bofftake\b",
        r"\bframework agreement(?:s)?\b",
    ),
    "facility_and_capacity_expansion": (
        r"\bexpand(?:ing|ed|s|ion)?\b",
        r"\bcapacity(?: increase| expansion| additions?)?\b",
        r"\bnew (?:facility|plant|fab|line)\b",
        r"\bnew [\w-]+(?: [\w-]+){0,3} (?:facility|plant|fab|line)\b",
        r"\bramp(?:ing|ed|s)?\b",
        r"\bscale-up\b",
        r"\bmanufacturing buildout\b",
    ),
    "construction_and_deployment": (
        r"\bgroundbreak(?:ing)?\b",
        r"\bbreaks? ground\b",
        r"\bconstruction\b",
        r"\bbuildout\b",
        r"\bdeploy(?:ment|ed|ing|s)?\b",
        r"\brollout\b",
        r"\bcommissioning\b",
        r"\bopening\b",
        r"\boperational\b",
        r"\bstart of operations\b",
    ),
    "partnerships_with_buildout_implications": (
        r"\bpartnership(?:s)?\b",
        r"\bcollaboration(?:s)?\b",
        r"\bjoint venture(?:s)?\b",
        r"\bstrategic agreement(?:s)?\b",
        r"\bmanufacturing agreement(?:s)?\b",
        r"\bsupply partnership(?:s)?\b",
    ),
    "planning_and_land_access_enablement": (
        r"\brecord of decision\b",
        r"\bintegrated activity plan\b",
        r"\bpublic land order\b",
        r"\bopening of (?:public )?lands?\b",
        r"\blease sale\b",
    ),
}


REVIEW_ONLY_FAMILIES = {
    "partnerships_with_buildout_implications",
    "planning_and_land_access_enablement",
}


EXCLUDED_GENERIC_PATTERNS: Tuple[str, ...] = (
    r"\bai\b",
    r"\bgrowth\b",
    r"\binnovation\b",
    r"\bmarket opportunity\b",
    r"\bstrategic\b",
    r"\bleadership\b",
    r"\bnext generation\b",
    r"\bstrong demand\b",
)


def _normalize_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, (list, tuple, set)):
        return " ".join(_normalize_text(item) for item in value if item is not None).strip()
    if isinstance(value, dict):
        return " ".join(
            _normalize_text(item) for item in value.values() if item is not None
        ).strip()
    return str(value).strip()


def _extract_allowed_fields(artifact: Dict[str, Any]) -> Dict[str, str]:
    category_tags = artifact.get("category_tags")
    publisher_metadata = artifact.get("publisher_metadata") or artifact.get("metadata")
    return {
        "title": _normalize_text(artifact.get("title")),
        "headline": _normalize_text(artifact.get("headline")),
        "subheadline": _normalize_text(artifact.get("subheadline")),
        "deck": _normalize_text(artifact.get("deck")),
        "section_name": _normalize_text(artifact.get("section_name")),
        "category_tags": _normalize_text(category_tags),
        "publisher_metadata": _normalize_text(publisher_metadata),
    }


def _find_family_hits(text: str) -> Dict[str, List[str]]:
    normalized = text.lower()
    hits: Dict[str, List[str]] = {}
    for family, patterns in EVENT_FORM_REGEXES.items():
        matched: List[str] = []
        for pattern in patterns:
            if re.search(pattern, normalized):
                matched.append(pattern)
        if matched:
            hits[family] = matched
    return hits


def _count_distinct_families(field_hits: Dict[str, Dict[str, List[str]]]) -> int:
    families = {
        family
        for per_field in field_hits.values()
        for family in per_field.keys()
    }
    return len(families)


def _collect_field_hits(artifact: Dict[str, Any]) -> Dict[str, Dict[str, List[str]]]:
    field_values = _extract_allowed_fields(artifact)
    hits: Dict[str, Dict[str, List[str]]] = {}
    for field_name, field_value in field_values.items():
        if not field_value:
            continue
        family_hits = _find_family_hits(field_value)
        if family_hits:
            hits[field_name] = family_hits
    return hits


def _collect_excluded_generic_hits(artifact: Dict[str, Any]) -> List[str]:
    hits: List[str] = []
    field_values = _extract_allowed_fields(artifact)
    for field_value in field_values.values():
        normalized = field_value.lower()
        for pattern in EXCLUDED_GENERIC_PATTERNS:
            if re.search(pattern, normalized) and pattern not in hits:
                hits.append(pattern)
    return hits


def _flatten_fired_rules(field_hits: Dict[str, Dict[str, List[str]]]) -> List[str]:
    fired: List[str] = []
    for field_name, family_hits in field_hits.items():
        for family_name, patterns in family_hits.items():
            for pattern in patterns:
                fired.append(f"{field_name}:{family_name}:{pattern}")
    return fired


def triage_capital_flow_artifact(artifact: Dict[str, Any]) -> Dict[str, Any]:
    """
    Deterministically triage an artifact into keep/review/drop.

    The result includes rule provenance so rejected artifacts can be audited.
    """
    field_hits = _collect_field_hits(artifact)
    generic_hits = _collect_excluded_generic_hits(artifact)

    strong_hits = {field: field_hits[field] for field in STRONG_FIELDS if field in field_hits}
    medium_hits = {field: field_hits[field] for field in MEDIUM_FIELDS if field in field_hits}
    weak_hits = {field: field_hits[field] for field in WEAK_FIELDS if field in field_hits}
    distinct_family_count = _count_distinct_families(field_hits)
    family_names = sorted(
        {
            family
            for per_field in field_hits.values()
            for family in per_field.keys()
        }
    )

    family_set = set(family_names)
    has_review_only_families = bool(family_set) and family_set.issubset(REVIEW_ONLY_FAMILIES)

    if strong_hits and any(
        family not in REVIEW_ONLY_FAMILIES
        for family in {
            family
            for per_field in strong_hits.values()
            for family in per_field.keys()
        }
    ):
        triage = TRIAGE_KEEP
        reason = "Strong-field event-form hit in an explicit capital-flow family."
    elif distinct_family_count >= 2:
        triage = TRIAGE_KEEP
        reason = "Multiple distinct event-form families were detected across allowed fields."
    elif has_review_only_families:
        triage = TRIAGE_REVIEW
        reason = "Only review-only event-form language was detected without explicit buildout form."
    elif medium_hits or weak_hits:
        triage = TRIAGE_REVIEW
        reason = "Only medium/weak-field event-form evidence was detected."
    else:
        triage = TRIAGE_DROP
        reason = "No qualifying event-form evidence was detected in allowed fields."

    return {
        "artifact_id": artifact.get("artifact_id"),
        "source_class": artifact.get("source_class"),
        "triage": triage,
        "reason": reason,
        "matched_families": family_names,
        "field_hits": field_hits,
        "fired_rules": _flatten_fired_rules(field_hits),
        "excluded_generic_hits": generic_hits,
        "allowed_fields_examined": list(ALLOWED_FIELDS),
    }


def build_prefilter_audit_record(
    artifact: Dict[str, Any],
    triage_result: Dict[str, Any],
) -> Dict[str, Any]:
    """Build a compact audit record for keep/review/drop decisions."""
    return {
        "artifact_id": artifact.get("artifact_id"),
        "source_class": artifact.get("source_class"),
        "publisher_or_author": artifact.get("publisher_or_author"),
        "published_at": artifact.get("published_at"),
        "title": artifact.get("title") or artifact.get("headline"),
        "triage": triage_result.get("triage"),
        "reason": triage_result.get("reason"),
        "matched_families": list(triage_result.get("matched_families") or []),
        "fired_rules": list(triage_result.get("fired_rules") or []),
        "excluded_generic_hits": list(triage_result.get("excluded_generic_hits") or []),
    }


def triage_batch(artifacts: Iterable[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Convenience helper for deterministic batch triage."""
    return [triage_capital_flow_artifact(artifact) for artifact in artifacts]
