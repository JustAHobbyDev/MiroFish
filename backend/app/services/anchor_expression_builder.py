"""
Deterministic anchor-expression surfacing from prefilter batches.
"""

from __future__ import annotations

import hashlib
import re
from typing import Any, Dict, Iterable, List

from .artifact_provenance import filter_real_artifacts


PHOTONICS_SYSTEM_DRIVERS = {
    "nvidia",
    "broadcom",
    "tsmc",
}

PHOTONICS_UPSTREAM_ISSUERS = {
    "axt",
    "jx advanced metals",
}

PHOTONICS_TERMS = {
    "photonics",
    "optics",
    "optical",
    "laser",
    "lasers",
    "indium phosphide",
    "inp",
    "co-packaged optics",
    "cpo",
    "silicon photonics",
    "transceiver",
    "transceivers",
    "ai networking",
}

PHOTONICS_BUILDOUT_TERMS = {
    "expand",
    "expands",
    "expanding",
    "capacity",
    "manufacturing",
    "facility",
    "fabs",
    "fab",
    "factory",
    "production",
    "supplier",
}


def _coerce_string(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def _anchor_expression_id(entity_name: str, profile_name: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "_", entity_name.lower()).strip("_")
    profile_slug = re.sub(r"[^a-z0-9]+", "_", profile_name.lower()).strip("_")
    digest = hashlib.sha1(f"{profile_slug}|{slug}".encode("utf-8")).hexdigest()[:8]
    return f"aec_{profile_slug}_{slug}_{digest}"


def _iter_prefilter_artifacts(
    prefilter_batches: Iterable[Dict[str, Any]],
    *,
    include_review: bool,
) -> List[Dict[str, Any]]:
    artifacts: List[Dict[str, Any]] = []
    for batch in prefilter_batches:
        artifacts.extend(dict(item) for item in batch.get("kept_artifacts", []))
        if include_review:
            artifacts.extend(dict(item) for item in batch.get("review_artifacts", []))
    return artifacts


def _artifact_text(artifact: Dict[str, Any]) -> str:
    return " ".join(
        [
            _coerce_string(artifact.get("title")),
            _coerce_string(artifact.get("headline")),
            _coerce_string(artifact.get("subheadline")),
            _coerce_string(artifact.get("deck")),
            _coerce_string(artifact.get("body_text")),
            " ".join(_coerce_string(item) for item in artifact.get("category_tags", [])),
        ]
    ).lower()


def _mentioned_entities(artifact: Dict[str, Any], known_entities: List[str]) -> List[str]:
    text = _artifact_text(artifact)
    hits: List[str] = []
    for entity in known_entities:
        lowered = entity.lower()
        if lowered and lowered in text and entity not in hits:
            hits.append(entity)
    return hits


def _photonics_anchor_role(artifact: Dict[str, Any]) -> str:
    issuer = _coerce_string(artifact.get("issuing_company_name"))
    lowered_issuer = issuer.lower()
    title = _coerce_string(artifact.get("title")).lower()
    text = _artifact_text(artifact)

    if lowered_issuer in PHOTONICS_SYSTEM_DRIVERS:
        return "system_demand_driver"
    if lowered_issuer in PHOTONICS_UPSTREAM_ISSUERS:
        return "upstream_dependency"
    if any(term in title for term in ("crystal materials", "substrate", "substrates", "feedstock")):
        return "upstream_dependency"
    if "metals" in lowered_issuer:
        return "upstream_dependency"
    if any(
        term in text
        for term in (
            "indium phosphide substrate",
            "indium phosphide substrates",
            "inp substrate",
            "inp substrates",
            "substrate materials",
            "semiconductor substrate",
            "semiconductor substrates",
        )
    ):
        return "upstream_dependency"
    if "wafer fab" in text or "6-inch inp" in text or "6-inch indium phosphide" in text:
        return "adjacent_anchor"
    if any(term in text for term in ("primary supplier", "market-leading", "global leader")):
        return "anchor_expression"
    return "anchor_expression"


def _photonics_anchor_score(artifact: Dict[str, Any]) -> int:
    issuer = _coerce_string(artifact.get("issuing_company_name")).lower()
    if not issuer:
        return 0

    text = _artifact_text(artifact)
    score = 0
    if any(term in text for term in PHOTONICS_TERMS):
        score += 3
    if any(term in text for term in PHOTONICS_BUILDOUT_TERMS):
        score += 2
    if issuer not in PHOTONICS_SYSTEM_DRIVERS:
        score += 1
    if any(
        term in text
        for term in (
            "ai factory",
            "hyperscale",
            "data center",
            "blackwell",
            "trainium",
            "tpu",
        )
    ):
        score += 1
    return score


def build_anchor_expression_batch(
    prefilter_batches: List[Dict[str, Any]],
    *,
    profile_name: str = "photonics",
    include_review: bool = True,
    include_synthetic: bool = False,
) -> Dict[str, Any]:
    artifacts = _iter_prefilter_artifacts(prefilter_batches, include_review=include_review)
    if not include_synthetic:
        artifacts = filter_real_artifacts(artifacts)

    known_entities = sorted(
        {
            _coerce_string(item.get("issuing_company_name"))
            for item in artifacts
            if _coerce_string(item.get("issuing_company_name"))
        }
    )

    grouped: Dict[str, Dict[str, Any]] = {}
    for artifact in artifacts:
        if profile_name != "photonics":
            continue
        score = _photonics_anchor_score(artifact)
        if score < 4:
            continue

        entity_name = _coerce_string(artifact.get("issuing_company_name"))
        if not entity_name:
            continue

        current = grouped.setdefault(
            entity_name,
            {
                "anchor_expression_candidate_id": _anchor_expression_id(entity_name, profile_name),
                "canonical_entity_name": entity_name,
                "profile_name": profile_name,
                "anchor_role": _photonics_anchor_role(artifact),
                "source_classes": set(),
                "supporting_artifact_ids": [],
                "supporting_titles": [],
                "mentioned_entities": set(),
                "max_anchor_score": 0,
            },
        )
        current["source_classes"].add(_coerce_string(artifact.get("source_class")))
        artifact_id = _coerce_string(artifact.get("artifact_id"))
        if artifact_id:
            current["supporting_artifact_ids"].append(artifact_id)
        title = _coerce_string(artifact.get("title"))
        if title:
            current["supporting_titles"].append(title)
        current["mentioned_entities"].update(_mentioned_entities(artifact, known_entities))
        current["max_anchor_score"] = max(int(current["max_anchor_score"]), score)

    anchors: List[Dict[str, Any]] = []
    for payload in grouped.values():
        role = _coerce_string(payload.get("anchor_role"))
        if role == "system_demand_driver":
            continue
        anchors.append(
            {
                "anchor_expression_candidate_id": payload["anchor_expression_candidate_id"],
                "canonical_entity_name": payload["canonical_entity_name"],
                "profile_name": payload["profile_name"],
                "anchor_role": role,
                "source_classes": sorted({item for item in payload["source_classes"] if item}),
                "supporting_artifact_ids": sorted(
                    {item for item in payload["supporting_artifact_ids"] if item}
                ),
                "supporting_titles": sorted(
                    {item for item in payload["supporting_titles"] if item}
                ),
                "mentioned_entities": sorted(
                    {
                        item
                        for item in payload["mentioned_entities"]
                        if item and item != payload["canonical_entity_name"]
                    }
                ),
                "support_count": len(
                    {item for item in payload["supporting_artifact_ids"] if item}
                ),
                "max_anchor_score": int(payload["max_anchor_score"]),
            }
        )

    anchors.sort(
        key=lambda item: (
            {"anchor_expression": 0, "adjacent_anchor": 1, "upstream_dependency": 2}.get(
                item["anchor_role"], 3
            ),
            -item["max_anchor_score"],
            -item["support_count"],
            item["canonical_entity_name"],
        )
    )

    return {
        "name": "anchor_expression_batch_v1",
        "profile_name": profile_name,
        "anchors": anchors,
        "metrics": {
            "input_prefilter_batch_count": len(prefilter_batches),
            "processed_artifact_count": len(artifacts),
            "anchor_expression_count": len(anchors),
            "anchor_expression_role_counts": {
                "anchor_expression": len([item for item in anchors if item["anchor_role"] == "anchor_expression"]),
                "adjacent_anchor": len([item for item in anchors if item["anchor_role"] == "adjacent_anchor"]),
                "upstream_dependency": len([item for item in anchors if item["anchor_role"] == "upstream_dependency"]),
            },
        },
    }
