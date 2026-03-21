"""
Zero-context LLM extraction for capital-flow signal candidates.

This module runs one artifact at a time through a fixed prompt and validates the
returned JSON against the v1 extraction contract.
"""

from __future__ import annotations

import os
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Optional

from ..config import Config
from ..utils.llm_client import LLMClient


DEFAULT_CAPITAL_FLOW_EXTRACTION_MODEL = os.environ.get(
    "CAPITAL_FLOW_EXTRACTION_MODEL",
    "gpt-4o-mini",
)
DEFAULT_CAPITAL_FLOW_EXTRACTION_PROVIDER = os.environ.get(
    "CAPITAL_FLOW_EXTRACTION_PROVIDER",
    Config.LLM_PROVIDER,
)
CAPITAL_FLOW_EXTRACTION_PROMPT_VERSION = "capital_flow_signal_extraction_v1"
ALLOWED_IMPLICATION_TYPES = {
    "direct_capital_allocation",
    "procurement_or_commitment_pull",
    "capacity_response",
    "architecture_induced_intensity",
    "policy_enabled_buildout",
}
ALLOWED_DIRECTNESS = {"direct", "indirect"}
ALLOWED_CONFIDENCE = {"low", "medium", "high"}


SYSTEM_PROMPT = """You are extracting possible capital-flow implications from a single public artifact.

Use only the artifact and its provenance.

Do not use prior knowledge about historical winners, bottlenecks, companies, themes, or the broader corpus.

Your job is not to form a thesis.

Your job is to decide whether this artifact alone contains one or more concrete observations that plausibly imply directional capital flow, procurement pull, capacity response, or physical buildout in a real system.

If no such implication is plausible from the artifact alone, return no candidates.

Return strict JSON only."""


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _coerce_string(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def _normalize_system_hints(value: Any) -> List[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [item for item in (_coerce_string(v) for v in value) if item]
    if isinstance(value, tuple):
        return [item for item in (_coerce_string(v) for v in value) if item]
    single = _coerce_string(value)
    return [single] if single else []


def build_capital_flow_extraction_messages(artifact: Dict[str, Any]) -> List[Dict[str, str]]:
    user_prompt = f"""Artifact metadata:
- artifact_id: {_coerce_string(artifact.get("artifact_id"))}
- source_class: {_coerce_string(artifact.get("source_class"))}
- publisher_or_author: {_coerce_string(artifact.get("publisher_or_author"))}
- published_at: {_coerce_string(artifact.get("published_at"))}
- title: {_coerce_string(artifact.get("title"))}
- source_url: {_coerce_string(artifact.get("source_url"))}

Artifact body:
{_coerce_string(artifact.get("body_text"))}

Task:
1. Determine whether this artifact alone implies possible directional capital flow into a real system.
2. If yes, extract up to 3 capital_flow_signal_candidate objects.
3. Each candidate must contain:
   - observable_statement
   - capital_flow_implication_type
   - observation_directness
   - capital_flow_implication
   - system_hints
   - physical_implication
   - confidence
4. Do not mention specific stocks as the answer unless the artifact itself is explicitly about them.
5. Do not infer a bottleneck or market mispricing.
6. If the artifact does not plausibly imply directional capital flow from the artifact alone, return no candidates."""
    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_prompt},
    ]


def _validate_candidate(candidate: Dict[str, Any], index: int) -> Dict[str, Any]:
    observable_statement = _coerce_string(candidate.get("observable_statement"))
    implication_type = _coerce_string(candidate.get("capital_flow_implication_type"))
    directness = _coerce_string(candidate.get("observation_directness"))
    implication = _coerce_string(candidate.get("capital_flow_implication"))
    system_hints = _normalize_system_hints(candidate.get("system_hints"))
    physical_implication = _coerce_string(candidate.get("physical_implication"))
    confidence = _coerce_string(candidate.get("confidence"))

    if not observable_statement:
        raise ValueError(f"candidate[{index}] missing observable_statement")
    if implication_type not in ALLOWED_IMPLICATION_TYPES:
        raise ValueError(f"candidate[{index}] has invalid capital_flow_implication_type: {implication_type!r}")
    if directness not in ALLOWED_DIRECTNESS:
        raise ValueError(f"candidate[{index}] has invalid observation_directness: {directness!r}")
    if not implication:
        raise ValueError(f"candidate[{index}] missing capital_flow_implication")
    if not system_hints:
        raise ValueError(f"candidate[{index}] missing system_hints")
    if not physical_implication:
        raise ValueError(f"candidate[{index}] missing physical_implication")
    if confidence not in ALLOWED_CONFIDENCE:
        raise ValueError(f"candidate[{index}] has invalid confidence: {confidence!r}")

    return {
        "observable_statement": observable_statement,
        "capital_flow_implication_type": implication_type,
        "observation_directness": directness,
        "capital_flow_implication": implication,
        "system_hints": system_hints,
        "physical_implication": physical_implication,
        "confidence": confidence,
    }


def validate_capital_flow_extraction_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    if not isinstance(payload, dict):
        raise ValueError("Extraction payload must be a JSON object.")

    produced_candidates = payload.get("produced_candidates")
    candidates = payload.get("candidates")
    rejection_reason = payload.get("rejection_reason")

    if not isinstance(produced_candidates, bool):
        raise ValueError("produced_candidates must be a boolean.")
    if not isinstance(candidates, list):
        raise ValueError("candidates must be a list.")

    validated_candidates = [
        _validate_candidate(candidate, index)
        for index, candidate in enumerate(candidates)
    ]

    normalized_rejection_reason = None
    if rejection_reason is not None:
        normalized_rejection_reason = _coerce_string(rejection_reason) or None

    if produced_candidates and not validated_candidates:
        raise ValueError("produced_candidates=true requires at least one valid candidate.")
    if not produced_candidates and validated_candidates:
        raise ValueError("produced_candidates=false cannot include candidates.")
    if not produced_candidates and not normalized_rejection_reason:
        raise ValueError("produced_candidates=false requires a rejection_reason.")

    return {
        "produced_candidates": produced_candidates,
        "candidates": validated_candidates,
        "rejection_reason": normalized_rejection_reason,
    }


class CapitalFlowExtractor:
    """Thin zero-context extraction wrapper with strict validation."""

    def __init__(
        self,
        *,
        llm_client: Optional[LLMClient] = None,
        provider: Optional[str] = None,
        model_name: Optional[str] = None,
    ):
        self.provider = provider or DEFAULT_CAPITAL_FLOW_EXTRACTION_PROVIDER
        self.model_name = model_name or DEFAULT_CAPITAL_FLOW_EXTRACTION_MODEL
        self.llm_client = llm_client or LLMClient(
            provider=self.provider,
            model=self.model_name,
        )

    def extract_from_artifact(self, artifact: Dict[str, Any]) -> Dict[str, Any]:
        messages = build_capital_flow_extraction_messages(artifact)
        raw_payload = self.llm_client.chat_json(
            messages=messages,
            temperature=0.1,
            max_tokens=1400,
        )
        validated = validate_capital_flow_extraction_payload(raw_payload)
        return {
            "artifact_id": _coerce_string(artifact.get("artifact_id")),
            "source_class": _coerce_string(artifact.get("source_class")),
            "produced_candidates": validated["produced_candidates"],
            "candidates": validated["candidates"],
            "rejection_reason": validated["rejection_reason"],
            "provider_name": self.provider,
            "model_name": self.model_name,
            "prompt_version": CAPITAL_FLOW_EXTRACTION_PROMPT_VERSION,
            "extracted_at": _utc_now_iso(),
        }


def build_capital_flow_signal_batch(
    prefilter_batch: Dict[str, Any],
    *,
    extractor: Optional[CapitalFlowExtractor] = None,
) -> Dict[str, Any]:
    """
    Run zero-context extraction on keep/review artifacts and instrument failures.
    """
    extractor = extractor or CapitalFlowExtractor()
    processed_results: List[Dict[str, Any]] = []
    schema_failures: List[Dict[str, Any]] = []
    extraction_failures: List[Dict[str, Any]] = []

    candidate_count = 0
    produced_candidate_artifact_count = 0
    no_candidate_artifact_count = 0
    review_artifact_count = 0
    review_candidate_artifact_count = 0

    artifacts_to_process: List[Dict[str, Any]] = []
    for item in prefilter_batch.get("kept_artifacts", []):
        item = dict(item)
        item["_prefilter_triage"] = "keep"
        artifacts_to_process.append(item)
    for item in prefilter_batch.get("review_artifacts", []):
        item = dict(item)
        item["_prefilter_triage"] = "review"
        artifacts_to_process.append(item)

    for artifact in artifacts_to_process:
        triage = artifact.get("_prefilter_triage", "")
        if triage == "review":
            review_artifact_count += 1
        try:
            result = extractor.extract_from_artifact(artifact)
        except ValueError as exc:
            schema_failures.append(
                {
                    "artifact_id": artifact.get("artifact_id"),
                    "prefilter_triage": triage,
                    "error_type": "schema_validation_error",
                    "error_message": str(exc),
                }
            )
            continue
        except Exception as exc:  # pragma: no cover - defensive runtime path
            extraction_failures.append(
                {
                    "artifact_id": artifact.get("artifact_id"),
                    "prefilter_triage": triage,
                    "error_type": "extraction_runtime_error",
                    "error_message": str(exc),
                }
            )
            continue

        processed_results.append(
            {
                **result,
                "prefilter_triage": triage,
            }
        )

        if result["produced_candidates"]:
            produced_candidate_artifact_count += 1
            candidate_count += len(result["candidates"])
            if triage == "review":
                review_candidate_artifact_count += 1
        else:
            no_candidate_artifact_count += 1

    return {
        "name": prefilter_batch.get("name", "capital_flow_signal_batch_v1"),
        "source_class": prefilter_batch.get("source_class", ""),
        "prompt_version": CAPITAL_FLOW_EXTRACTION_PROMPT_VERSION,
        "model_name": extractor.model_name,
        "processed_results": processed_results,
        "schema_failures": schema_failures,
        "extraction_failures": extraction_failures,
        "metrics": {
            "artifacts_sent_to_llm": len(artifacts_to_process),
            "successful_extractions": len(processed_results),
            "schema_failure_count": len(schema_failures),
            "extraction_failure_count": len(extraction_failures),
            "produced_candidate_artifact_count": produced_candidate_artifact_count,
            "no_candidate_artifact_count": no_candidate_artifact_count,
            "total_candidate_count": candidate_count,
            "review_artifact_count": review_artifact_count,
            "review_candidate_artifact_count": review_candidate_artifact_count,
        },
    }
