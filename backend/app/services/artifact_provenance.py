"""
Artifact provenance helpers for synthetic-vs-live segregation.
"""

from __future__ import annotations

from typing import Any, Dict, Iterable, List
from urllib.parse import urlparse


def _coerce_string(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def classify_artifact_provenance(artifact: Dict[str, Any]) -> str:
    if bool(artifact.get("synthetic_sample")):
        return "synthetic_flagged"
    provenance_class = _coerce_string(artifact.get("provenance_class")).lower()
    if provenance_class.startswith("synthetic"):
        return provenance_class
    source_url = _coerce_string(artifact.get("source_url")).lower()
    host = urlparse(source_url).netloc
    if host in {"example.com", "www.example.com"}:
        return "synthetic_example"
    return "external_real_or_unknown"


def support_provenance_status(artifacts: Iterable[Dict[str, Any]]) -> str:
    classes = {
        classify_artifact_provenance(artifact)
        for artifact in artifacts
    }
    if not classes:
        return "unknown"
    synthetic_classes = {item for item in classes if item.startswith("synthetic")}
    if synthetic_classes == classes:
        return "synthetic_only"
    if synthetic_classes:
        return "mixed"
    return "real_only"


def artifact_provenance_classes(artifacts: Iterable[Dict[str, Any]]) -> List[str]:
    return sorted(
        {
            classify_artifact_provenance(artifact)
            for artifact in artifacts
        }
    )


def is_synthetic_artifact(artifact: Dict[str, Any]) -> bool:
    return classify_artifact_provenance(artifact).startswith("synthetic")


def filter_real_artifacts(artifacts: Iterable[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return [dict(artifact) for artifact in artifacts if not is_synthetic_artifact(artifact)]
