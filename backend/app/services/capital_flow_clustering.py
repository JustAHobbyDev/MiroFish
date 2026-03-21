"""
Deterministic clustering for capital-flow signal candidates.
"""

from __future__ import annotations

import hashlib
import re
from datetime import date, timedelta
from typing import Any, Dict, Iterable, List, Optional


ROLLING_WINDOW_DAYS = 90


def _coerce_string(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def _parse_date(value: Any) -> Optional[date]:
    text = _coerce_string(value)
    if not text:
        return None
    text = text.replace("Z", "+00:00")
    try:
        return date.fromisoformat(text[:10])
    except ValueError:
        return None


def _artifact_lookup(prefilter_batch: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    lookup: Dict[str, Dict[str, Any]] = {}
    for key in ("kept_artifacts", "review_artifacts"):
        for artifact in prefilter_batch.get(key, []):
            lookup[_coerce_string(artifact.get("artifact_id"))] = dict(artifact)
    return lookup


def _extract_geography_hints(text: str) -> List[str]:
    normalized = text.lower()
    hints: List[str] = []
    mapping = (
        ("united states", "United States"),
        ("u.s.", "United States"),
        ("us ", "United States"),
        ("texas", "Texas"),
        ("arizona", "Arizona"),
        ("virginia", "Virginia"),
        ("ohio", "Ohio"),
        ("north carolina", "North Carolina"),
        ("south carolina", "South Carolina"),
        ("pittsburgh", "Pennsylvania"),
        ("louisiana", "Louisiana"),
        ("tennessee", "Tennessee"),
        ("mississippi", "Mississippi"),
    )
    for needle, label in mapping:
        if needle in normalized and label not in hints:
            hints.append(label)
    return hints


def _derive_system_label(text: str) -> str:
    normalized = text.lower()
    if any(term in normalized for term in ("transformer", "switchgear", "grid equipment", "substation")):
        return "grid equipment and transformer buildout"
    if any(term in normalized for term in ("engine", "generator", "gas power", "nuclear", "wind")):
        return "power generation and backup equipment buildout"
    if (
        "data center" in normalized
        and any(term in normalized for term in ("hyperscale", "campus", "it capacity", "construction", "ground", "mw", "gw"))
    ):
        return "data center campus buildout"
    if any(term in normalized for term in ("utility", "large-load", "large load", "load growth", "interconnection", "electricity infrastructure", "grid", "power system")):
        return "utility and large-load power buildout"
    if any(term in normalized for term in ("manufacturing", "factory", "plant", "facility", "production")):
        return "industrial manufacturing expansion"
    return "general industrial buildout"


def _derive_demand_driver_summary(system_label: str) -> str:
    mapping = {
        "grid equipment and transformer buildout": "Utilities, grid bottlenecks, and large-load demand are driving spend into transformers and adjacent grid equipment.",
        "utility and large-load power buildout": "Large-load and utility response needs are driving spend into power-system expansion and supporting infrastructure.",
        "data center campus buildout": "Hyperscale and AI data-center expansion is driving recurring physical buildout and financing activity.",
        "power generation and backup equipment buildout": "Rising power demand and resilience needs are driving investment into generation and backup-power equipment.",
        "industrial manufacturing expansion": "Industrial capacity additions are driving recurring manufacturing buildout and plant expansion signals.",
        "general industrial buildout": "Multiple artifacts suggest recurring industrial buildout activity in one provisional lane.",
    }
    return mapping.get(system_label, "Multiple artifacts suggest recurring capital deployment in one provisional system.")


def _derive_cluster_statement(system_label: str) -> str:
    mapping = {
        "grid equipment and transformer buildout": "Multiple artifacts imply recurring spend and buildout around transformers, switchgear, and adjacent grid-equipment capacity.",
        "utility and large-load power buildout": "Multiple artifacts imply recurring utility and large-load power-system spend, financing, or infrastructure response.",
        "data center campus buildout": "Multiple artifacts imply recurring financing and construction activity in data-center campus buildout.",
        "power generation and backup equipment buildout": "Multiple artifacts imply recurring investment in generation and backup-power equipment expansion.",
        "industrial manufacturing expansion": "Multiple artifacts imply recurring manufacturing plant and capacity expansion in one industrial lane.",
        "general industrial buildout": "Multiple artifacts imply recurring buildout or committed spend in one industrial system.",
    }
    return mapping.get(system_label, "Multiple artifacts imply recurring directional capital flow in one provisional system.")


def _normalize_signal(
    processed_result: Dict[str, Any],
    artifact: Dict[str, Any],
    candidate: Dict[str, Any],
    candidate_index: int,
) -> Dict[str, Any]:
    artifact_id = _coerce_string(processed_result.get("artifact_id"))
    title = _coerce_string(artifact.get("title"))
    body_text = _coerce_string(artifact.get("body_text"))
    combined_text = " ".join(
        [
            title,
            body_text,
            _coerce_string(candidate.get("observable_statement")),
            _coerce_string(candidate.get("capital_flow_implication")),
            " ".join(candidate.get("system_hints", [])),
            _coerce_string(candidate.get("physical_implication")),
        ]
    )
    return {
        "signal_id": f"{artifact_id}:capital:{candidate_index}",
        "artifact_id": artifact_id,
        "source_class": _coerce_string(processed_result.get("source_class")),
        "published_at": _coerce_string(artifact.get("published_at")),
        "published_date": _parse_date(artifact.get("published_at")),
        "title": title,
        "prefilter_triage": _coerce_string(processed_result.get("prefilter_triage")),
        "capital_flow_implication_type": _coerce_string(candidate.get("capital_flow_implication_type")),
        "observation_directness": _coerce_string(candidate.get("observation_directness")),
        "system_hints": list(candidate.get("system_hints", [])),
        "confidence": _coerce_string(candidate.get("confidence")),
        "system_label": _derive_system_label(combined_text),
        "geography_hints": _extract_geography_hints(combined_text),
    }


def _iter_signals(
    signal_batch: Dict[str, Any],
    prefilter_batch: Dict[str, Any],
) -> List[Dict[str, Any]]:
    lookup = _artifact_lookup(prefilter_batch)
    signals: List[Dict[str, Any]] = []
    for processed_result in signal_batch.get("processed_results", []):
        if not processed_result.get("produced_candidates"):
            continue
        artifact_id = _coerce_string(processed_result.get("artifact_id"))
        artifact = lookup.get(artifact_id, {})
        for index, candidate in enumerate(processed_result.get("candidates", [])):
            signals.append(_normalize_signal(processed_result, artifact, candidate, index))
    return signals


def _confidence_for_cluster(cluster_signals: List[Dict[str, Any]]) -> str:
    artifact_count = len({signal["artifact_id"] for signal in cluster_signals})
    source_class_count = len({signal["source_class"] for signal in cluster_signals})
    direct_count = sum(1 for signal in cluster_signals if signal["observation_directness"] == "direct")
    if artifact_count >= 4 and source_class_count >= 2 and direct_count >= 3:
        return "high"
    if artifact_count >= 2 and len(cluster_signals) >= 3:
        return "medium"
    return "low"


def _window_for_cluster(cluster_signals: List[Dict[str, Any]]) -> Dict[str, Optional[str]]:
    dates = [signal["published_date"] for signal in cluster_signals if signal["published_date"] is not None]
    if not dates:
        return {"start_date": None, "end_date": None}
    return {
        "start_date": min(dates).isoformat(),
        "end_date": max(dates).isoformat(),
    }


def _cluster_id(system_label: str, end_date: Optional[str]) -> str:
    slug = re.sub(r"[^a-z0-9]+", "_", system_label.lower()).strip("_")
    suffix = end_date or "unknown_date"
    digest = hashlib.sha1(f"{slug}|{suffix}".encode("utf-8")).hexdigest()[:8]
    return f"cfc_{slug}_{suffix}_{digest}"


def build_capital_flow_cluster_batch(
    signal_batch: Dict[str, Any],
    prefilter_batch: Dict[str, Any],
) -> Dict[str, Any]:
    signals = [signal for signal in _iter_signals(signal_batch, prefilter_batch) if signal["published_date"] is not None]
    signals.sort(key=lambda item: (item["system_label"], item["published_date"], item["signal_id"]))

    grouped: Dict[str, List[Dict[str, Any]]] = {}
    for signal in signals:
        grouped.setdefault(signal["system_label"], []).append(signal)

    clusters: List[Dict[str, Any]] = []
    for system_label, system_signals in grouped.items():
        bucket: List[Dict[str, Any]] = []
        for signal in system_signals:
            if not bucket:
                bucket.append(signal)
                continue
            last_date = max(item["published_date"] for item in bucket if item["published_date"] is not None)
            assert last_date is not None
            if signal["published_date"] - last_date <= timedelta(days=ROLLING_WINDOW_DAYS):
                bucket.append(signal)
            else:
                if len({item["artifact_id"] for item in bucket}) >= 2:
                    window = _window_for_cluster(bucket)
                    clusters.append(
                        {
                            "capital_flow_cluster_id": _cluster_id(system_label, window["end_date"]),
                            "as_of_date": window["end_date"],
                            "status": "candidate",
                            "system_label": system_label,
                            "cluster_statement": _derive_cluster_statement(system_label),
                            "supporting_capital_flow_signal_ids": [item["signal_id"] for item in bucket],
                            "signal_count": len(bucket),
                            "artifact_count": len({item["artifact_id"] for item in bucket}),
                            "source_classes": sorted({item["source_class"] for item in bucket if item["source_class"]}),
                            "time_window": window,
                            "geography_hints": sorted({hint for item in bucket for hint in item["geography_hints"]}),
                            "demand_driver_summary": _derive_demand_driver_summary(system_label),
                            "confidence": _confidence_for_cluster(bucket),
                            "capital_flow_implication_types_present": sorted(
                                {item["capital_flow_implication_type"] for item in bucket if item["capital_flow_implication_type"]}
                            ),
                        }
                    )
                bucket = [signal]
        if len({item["artifact_id"] for item in bucket}) >= 2:
            window = _window_for_cluster(bucket)
            clusters.append(
                {
                    "capital_flow_cluster_id": _cluster_id(system_label, window["end_date"]),
                    "as_of_date": window["end_date"],
                    "status": "candidate",
                    "system_label": system_label,
                    "cluster_statement": _derive_cluster_statement(system_label),
                    "supporting_capital_flow_signal_ids": [item["signal_id"] for item in bucket],
                    "signal_count": len(bucket),
                    "artifact_count": len({item["artifact_id"] for item in bucket}),
                    "source_classes": sorted({item["source_class"] for item in bucket if item["source_class"]}),
                    "time_window": window,
                    "geography_hints": sorted({hint for item in bucket for hint in item["geography_hints"]}),
                    "demand_driver_summary": _derive_demand_driver_summary(system_label),
                    "confidence": _confidence_for_cluster(bucket),
                    "capital_flow_implication_types_present": sorted(
                        {item["capital_flow_implication_type"] for item in bucket if item["capital_flow_implication_type"]}
                    ),
                }
            )

    return {
        "name": f"{_coerce_string(signal_batch.get('name'))}_capital_flow_clusters_v1",
        "source_class": _coerce_string(signal_batch.get("source_class")),
        "clusters": clusters,
        "metrics": {
            "input_signal_count": len(signals),
            "cluster_count": len(clusters),
        },
    }
