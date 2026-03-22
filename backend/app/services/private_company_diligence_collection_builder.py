"""
Build deterministic private-company diligence collections from local manifests.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List


REPO_ROOT = Path(__file__).resolve().parents[3]


def _coerce_string(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def _resolve_path(path_value: str) -> Path:
    raw = Path(_coerce_string(path_value))
    if raw.is_absolute():
        return raw
    return REPO_ROOT / raw


def _manifest_index(manifest_batch: Dict[str, Any]) -> Dict[str, List[Dict[str, Any]]]:
    index: Dict[str, List[Dict[str, Any]]] = {}
    for document in manifest_batch.get("documents", []):
        entity_name = _coerce_string(document.get("canonical_entity_name"))
        if entity_name:
            index.setdefault(entity_name, []).append(document)
    return index


def build_private_company_diligence_collection_batch(
    private_plan_batch: Dict[str, Any],
    manifest_batch: Dict[str, Any],
) -> Dict[str, Any]:
    documents_by_entity = _manifest_index(manifest_batch)
    collections: List[Dict[str, Any]] = []

    for plan in private_plan_batch.get("plans", []):
        entity_name = _coerce_string(plan.get("canonical_entity_name"))
        documents: List[Dict[str, Any]] = []
        for item in documents_by_entity.get(entity_name, []):
            local_path = _resolve_path(_coerce_string(item.get("local_path")))
            documents.append(
                {
                    "document_id": _coerce_string(item.get("document_id")),
                    "document_type": _coerce_string(item.get("document_type")),
                    "document_title": _coerce_string(item.get("document_title")),
                    "source_url": _coerce_string(item.get("source_url")),
                    "local_path": str(local_path),
                    "local_file_exists": local_path.exists(),
                    "source_priority": _coerce_string(item.get("source_priority")),
                }
            )

        collections.append(
            {
                "private_company_diligence_plan_id": _coerce_string(
                    plan.get("private_company_diligence_plan_id")
                ),
                "canonical_entity_name": entity_name,
                "resolved_issuer_name": _coerce_string(plan.get("resolved_issuer_name")),
                "system_label": _coerce_string(plan.get("system_label")),
                "route_type": _coerce_string(plan.get("route_type")),
                "source_priorities": list(plan.get("source_priorities", [])),
                "collected_documents": documents,
                "collection_summary": {
                    "document_count": len(documents),
                    "existing_document_count": len(
                        [item for item in documents if bool(item.get("local_file_exists"))]
                    ),
                    "missing_document_count": len(
                        [item for item in documents if not bool(item.get("local_file_exists"))]
                    ),
                },
            }
        )

    return {
        "name": "private_company_diligence_collection_batch_v1",
        "collections": collections,
        "metrics": {
            "input_plan_count": len(private_plan_batch.get("plans", [])),
            "collection_count": len(collections),
            "document_count": sum(
                collection.get("collection_summary", {}).get("document_count", 0)
                for collection in collections
            ),
        },
    }
