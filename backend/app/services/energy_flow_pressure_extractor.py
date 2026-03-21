"""
Zero-context LLM extraction for energy-flow-pressure signals.

This module runs one artifact at a time through a fixed prompt and validates
the returned JSON against the v1 extraction contract.
"""

from __future__ import annotations

import os
from datetime import datetime, timezone
import re
from typing import Any, Dict, List, Optional

from ..config import Config
from ..utils.llm_client import LLMClient


DEFAULT_ENERGY_FLOW_EXTRACTION_MODEL = os.environ.get(
    "ENERGY_FLOW_EXTRACTION_MODEL",
    "gpt-4o-mini",
)
DEFAULT_ENERGY_FLOW_EXTRACTION_PROVIDER = os.environ.get(
    "ENERGY_FLOW_EXTRACTION_PROVIDER",
    Config.LLM_PROVIDER,
)
ENERGY_FLOW_EXTRACTION_PROMPT_VERSION = "energy_flow_pressure_extraction_v1"
ALLOWED_ENERGY_PRESSURE_TYPES = {
    "load_growth",
    "pipeline_pressure",
    "capacity_tightness",
    "infrastructure_response_need",
}
ALLOWED_DIRECTNESS = {"direct", "indirect"}
ALLOWED_RELATIONSHIP_TO_CAPITAL_FLOW = {
    "energy_flow_pressure_only",
    "energy_flow_pressure_and_capital_flow",
}
ALLOWED_CONFIDENCE = {"low", "medium", "high"}
ENERGY_PRESSURE_TYPE_ALIASES = {
    "load_growth": "load_growth",
    "load growth": "load_growth",
    "demand increase": "load_growth",
    "demand pressure": "load_growth",
    "demand growth": "load_growth",
    "increased demand": "load_growth",
    "increased energy demand": "load_growth",
    "increased demand for electricity": "load_growth",
    "anticipated future demand increase": "load_growth",
    "future demand projection": "load_growth",
    "immediate demand pressure": "load_growth",
    "pipeline_pressure": "pipeline_pressure",
    "pipeline pressure": "pipeline_pressure",
    "capacity_tightness": "capacity_tightness",
    "capacity tightness": "capacity_tightness",
    "timing pressure": "capacity_tightness",
    "supply adjustment": "capacity_tightness",
    "supply pressure": "infrastructure_response_need",
    "infrastructure_response_need": "infrastructure_response_need",
    "infrastructure response need": "infrastructure_response_need",
    "capital investment pressure": "infrastructure_response_need",
    "infrastructure enhancement": "infrastructure_response_need",
    "infrastructure development": "infrastructure_response_need",
    "investment in energy production capacity": "infrastructure_response_need",
    "increased demand for energy production capabilities": "infrastructure_response_need",
    "capital investment in energy infrastructure": "infrastructure_response_need",
    "investment-driven demand for energy resources": "infrastructure_response_need",
    "increased demand for energy_related products": "infrastructure_response_need",
    "increased demand for power products": "infrastructure_response_need",
    "increased demand for grid equipment": "infrastructure_response_need",
    "increased demand for transformers": "infrastructure_response_need",
    "increased demand for energy infrastructure": "infrastructure_response_need",
    "demand for energy-efficient production technologies": "infrastructure_response_need",
    "capital investment in energy_intensive manufacturing": "infrastructure_response_need",
    "increased energy supply requirements": "infrastructure_response_need",
    "increased energy usage during construction": "infrastructure_response_need",
    "increased demand for energy capacity": "infrastructure_response_need",
    "increased demand for renewable energy sources": "infrastructure_response_need",
    "demand for energy capacity": "infrastructure_response_need",
    "production capacity pressure": "infrastructure_response_need",
    "increased residential energy demand": "load_growth",
    "future demand escalation": "load_growth",
    "regional demand surge": "load_growth",
    "demand growth expectation": "load_growth",
    "investment in production capacity": "infrastructure_response_need",
    "increased energy consumption": "load_growth",
    "rising energy demand from specific sectors": "load_growth",
    "capital investment in energy production": "infrastructure_response_need",
    "increased demand for energy_intensive production": "infrastructure_response_need",
    "strategic demand": "load_growth",
    "investment_driven demand": "infrastructure_response_need",
    "sustained demand for energy resources": "load_growth",
    "increased local energy consumption": "load_growth",
    "increased energy consumption due to economic growth": "load_growth",
    "investment pressure": "infrastructure_response_need",
    "emerging demand from new sectors": "load_growth",
    "supply adequacy concern": "capacity_tightness",
    "future energy supply increase": "infrastructure_response_need",
    "increased demand for energy inputs": "infrastructure_response_need",
    "increased energy requirements for production": "infrastructure_response_need",
}
RELATIONSHIP_ALIASES = {
    "energy_flow_pressure_only": "energy_flow_pressure_only",
    "energy flow pressure only": "energy_flow_pressure_only",
    "energy_only": "energy_flow_pressure_only",
    "energy_flow_pressure_and_capital_flow": "energy_flow_pressure_and_capital_flow",
    "energy flow pressure and capital flow": "energy_flow_pressure_and_capital_flow",
    "both": "energy_flow_pressure_and_capital_flow",
    "dual_role": "energy_flow_pressure_and_capital_flow",
}

ENERGY_SYSTEM_LINKAGE_TERMS = (
    "power",
    "electric",
    "electricity",
    "grid",
    "utility",
    "utilities",
    "generation",
    "generator",
    "transformer",
    "transmission",
    "distribution",
    "switchgear",
    "substation",
    "interconnection",
    "load",
)

DATA_CENTER_BUILDOUT_TERMS = (
    "campus",
    "hyperscale",
    "it capacity",
    "data center development",
    "data center campus",
    "construction",
    "ground",
    "final engineering",
    "engineering phase",
    "buildout",
)

LABOR_ONLY_TERMS = (
    "job",
    "jobs",
    "workforce",
    "hiring",
    "employment",
    "create",
    "creating",
)


SYSTEM_PROMPT = """You are extracting possible energy-system pressure implications from a single public artifact.

Use only the artifact and its provenance.

Do not use prior knowledge about historical winners, bottlenecks, companies, themes, or the broader corpus.

Your job is not to form a thesis.

Your job is to decide whether this artifact alone contains one or more concrete observations that plausibly imply rising pressure on an energy system as a necessary production input.

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


def _coerce_bool(value: Any) -> Optional[bool]:
    if isinstance(value, bool):
        return value
    if isinstance(value, int):
        if value in {0, 1}:
            return bool(value)
        return None
    if isinstance(value, str):
        normalized = value.strip().lower()
        if normalized in {"true", "yes", "y", "1"}:
            return True
        if normalized in {"false", "no", "n", "0"}:
            return False
    return None


def _contains_energy_system_linkage(text: str) -> bool:
    normalized = text.lower()
    if re.search(r"\b\d+\s?(mw|gw)\b", normalized):
        return True
    return any(term in normalized for term in ENERGY_SYSTEM_LINKAGE_TERMS)


def _contains_data_center_buildout_linkage(text: str) -> bool:
    normalized = text.lower()
    if "data center" not in normalized:
        return False
    if re.search(r"\b\d+\s?(mw|gw)\b", normalized):
        return True
    return any(term in normalized for term in DATA_CENTER_BUILDOUT_TERMS)


def _apply_trade_press_energy_postfilter(
    artifact: Dict[str, Any],
    candidates: List[Dict[str, Any]],
) -> tuple[List[Dict[str, Any]], List[str]]:
    artifact_text = " ".join(
        [
            _coerce_string(artifact.get("title")),
            _coerce_string(artifact.get("body_text")),
        ]
    ).lower()
    filtered: List[Dict[str, Any]] = []
    dropped_errors: List[str] = []

    for index, candidate in enumerate(candidates):
        observable = _coerce_string(candidate.get("observable_statement")).lower()

        if any(term in observable for term in LABOR_ONLY_TERMS):
            dropped_errors.append(
                f"candidate[{index}] suppressed as labor-only energy observation"
            )
            continue

        if _contains_energy_system_linkage(artifact_text):
            filtered.append(candidate)
            continue

        if _contains_data_center_buildout_linkage(artifact_text):
            filtered.append(candidate)
            continue

        dropped_errors.append(
            f"candidate[{index}] suppressed for lacking explicit energy-system or data-center-buildout linkage"
        )

    return filtered, dropped_errors


def _normalize_energy_pressure_type(value: Any) -> str:
    normalized = _coerce_string(value).strip().lower().replace("-", "_")
    if normalized in ENERGY_PRESSURE_TYPE_ALIASES:
        return ENERGY_PRESSURE_TYPE_ALIASES[normalized]
    if "pipeline" in normalized:
        return "pipeline_pressure"
    if "load" in normalized:
        return "load_growth"
    if "tight" in normalized or "constraint" in normalized or "shortage" in normalized:
        return "capacity_tightness"
    if "infrastructure" in normalized or "response" in normalized or "generation" in normalized:
        return "infrastructure_response_need"
    return normalized


def _normalize_relationship_to_capital_flow(value: Any) -> str:
    normalized = _coerce_string(value).strip().lower().replace("-", "_")
    if normalized in RELATIONSHIP_ALIASES:
        return RELATIONSHIP_ALIASES[normalized]
    if "both" in normalized or "dual" in normalized:
        return "energy_flow_pressure_and_capital_flow"
    if "capital" in normalized and "energy" in normalized:
        return "energy_flow_pressure_and_capital_flow"
    if "energy" in normalized:
        return "energy_flow_pressure_only"
    return normalized


def _normalize_confidence(value: Any) -> str:
    if isinstance(value, (int, float)):
        if value >= 0.8:
            return "high"
        if value >= 0.5:
            return "medium"
        return "low"
    normalized = _coerce_string(value).strip().lower()
    if normalized in ALLOWED_CONFIDENCE:
        return normalized
    return normalized


def _normalize_directness(value: Any) -> str:
    normalized = _coerce_string(value).strip().lower()
    if normalized in ALLOWED_DIRECTNESS:
        return normalized
    if normalized in {"high", "medium", "explicit", "stated", "announced"}:
        return "direct"
    if normalized in {"low", "inferred", "implicit", "possible", "potential"}:
        return "indirect"
    return normalized


def _normalize_payload_shape(payload: Any) -> Dict[str, Any]:
    if isinstance(payload, list):
        return {
            "produced_candidates": bool(payload),
            "candidates": payload,
            "rejection_reason": None if payload else "No plausible energy-system pressure implication can be inferred from the artifact alone.",
        }
    if not isinstance(payload, dict):
        raise ValueError("Extraction payload must be a JSON object.")

    candidates = payload.get("candidates")
    if candidates is None and isinstance(payload.get("results"), list):
        candidates = payload.get("results")
    if candidates is None and isinstance(payload.get("energy_flow_pressure_signals"), list):
        candidates = payload.get("energy_flow_pressure_signals")
    if candidates is None and isinstance(payload.get("energy_flow_pressure_signal"), list):
        candidates = payload.get("energy_flow_pressure_signal")

    produced_candidates = payload.get("produced_candidates")
    if produced_candidates is None and isinstance(candidates, list):
        produced_candidates = bool(candidates)

    rejection_reason = payload.get("rejection_reason")
    if rejection_reason is None and produced_candidates is False:
        rejection_reason = "No plausible energy-system pressure implication can be inferred from the artifact alone."

    return {
        "produced_candidates": produced_candidates,
        "candidates": candidates,
        "rejection_reason": rejection_reason,
    }


def build_energy_flow_pressure_extraction_messages(artifact: Dict[str, Any]) -> List[Dict[str, str]]:
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
1. Determine whether this artifact alone implies possible pressure on an energy system as a necessary production input.
2. If yes, extract up to 3 energy_flow_pressure_signal objects.
3. Each candidate must contain:
   - observable_statement
   - energy_pressure_type
   - observation_directness
   - energy_flow_implication
   - system_hints
   - physical_implication
   - relationship_to_capital_flow
   - confidence
4. Use relationship_to_capital_flow:
   - energy_flow_pressure_only
   - or energy_flow_pressure_and_capital_flow
5. Do not infer a bottleneck or market mispricing.
6. If the artifact does not plausibly imply energy-system pressure from the artifact alone, return no candidates."""
    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_prompt},
    ]


def _validate_candidate(candidate: Dict[str, Any], index: int) -> Dict[str, Any]:
    normalized_candidate = {
        _coerce_string(key).strip(): value
        for key, value in candidate.items()
    }
    observable_statement = _coerce_string(normalized_candidate.get("observable_statement"))
    pressure_type = _normalize_energy_pressure_type(normalized_candidate.get("energy_pressure_type"))
    directness = _normalize_directness(normalized_candidate.get("observation_directness"))
    implication = _coerce_string(normalized_candidate.get("energy_flow_implication"))
    system_hints = _normalize_system_hints(normalized_candidate.get("system_hints"))
    physical_implication = _coerce_string(normalized_candidate.get("physical_implication"))
    relationship = _normalize_relationship_to_capital_flow(normalized_candidate.get("relationship_to_capital_flow"))
    confidence = _normalize_confidence(normalized_candidate.get("confidence"))

    if not observable_statement:
        raise ValueError(f"candidate[{index}] missing observable_statement")
    if pressure_type not in ALLOWED_ENERGY_PRESSURE_TYPES:
        raise ValueError(f"candidate[{index}] has invalid energy_pressure_type: {pressure_type!r}")
    if directness not in ALLOWED_DIRECTNESS:
        raise ValueError(f"candidate[{index}] has invalid observation_directness: {directness!r}")
    if not implication:
        raise ValueError(f"candidate[{index}] missing energy_flow_implication")
    if not system_hints:
        raise ValueError(f"candidate[{index}] missing system_hints")
    if not physical_implication:
        raise ValueError(f"candidate[{index}] missing physical_implication")
    if relationship not in ALLOWED_RELATIONSHIP_TO_CAPITAL_FLOW:
        raise ValueError(f"candidate[{index}] has invalid relationship_to_capital_flow: {relationship!r}")
    if confidence not in ALLOWED_CONFIDENCE:
        raise ValueError(f"candidate[{index}] has invalid confidence: {confidence!r}")

    return {
        "observable_statement": observable_statement,
        "energy_pressure_type": pressure_type,
        "observation_directness": directness,
        "energy_flow_implication": implication,
        "system_hints": system_hints,
        "physical_implication": physical_implication,
        "relationship_to_capital_flow": relationship,
        "confidence": confidence,
    }


def validate_energy_flow_pressure_extraction_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    normalized_payload = _normalize_payload_shape(payload)

    produced_candidates = _coerce_bool(normalized_payload.get("produced_candidates"))
    candidates = normalized_payload.get("candidates")
    rejection_reason = normalized_payload.get("rejection_reason")

    if not isinstance(produced_candidates, bool):
        raise ValueError("produced_candidates must be a boolean.")
    if candidates is None:
        candidates = []
    if not isinstance(candidates, list):
        raise ValueError("candidates must be a list.")

    validated_candidates: List[Dict[str, Any]] = []
    dropped_candidate_errors: List[str] = []
    for index, candidate in enumerate(candidates):
        try:
            validated_candidates.append(_validate_candidate(candidate, index))
        except ValueError as exc:
            dropped_candidate_errors.append(str(exc))

    normalized_rejection_reason = None
    if rejection_reason is not None:
        normalized_rejection_reason = _coerce_string(rejection_reason) or None

    if produced_candidates and not validated_candidates:
        if dropped_candidate_errors:
            raise ValueError(dropped_candidate_errors[0])
        raise ValueError("produced_candidates=true requires at least one valid candidate.")
    if not produced_candidates and validated_candidates:
        raise ValueError("produced_candidates=false cannot include candidates.")
    if not produced_candidates and not normalized_rejection_reason:
        raise ValueError("produced_candidates=false requires a rejection_reason.")

    return {
        "produced_candidates": produced_candidates,
        "candidates": validated_candidates,
        "rejection_reason": normalized_rejection_reason,
        "dropped_candidate_errors": dropped_candidate_errors,
    }


class EnergyFlowPressureExtractor:
    """Thin zero-context extraction wrapper with strict validation."""

    def __init__(
        self,
        *,
        llm_client: Optional[LLMClient] = None,
        provider: Optional[str] = None,
        model_name: Optional[str] = None,
    ):
        self.provider = provider or DEFAULT_ENERGY_FLOW_EXTRACTION_PROVIDER
        self.model_name = model_name or DEFAULT_ENERGY_FLOW_EXTRACTION_MODEL
        self.llm_client = llm_client or LLMClient(
            provider=self.provider,
            model=self.model_name,
        )

    def extract_from_artifact(self, artifact: Dict[str, Any]) -> Dict[str, Any]:
        messages = build_energy_flow_pressure_extraction_messages(artifact)
        raw_response_text = self.llm_client.chat(
            messages=messages,
            temperature=0.1,
            max_tokens=1400,
        )
        try:
            raw_payload = self.llm_client.parse_json_text(raw_response_text)
        except ValueError as exc:
            setattr(exc, "raw_payload", raw_response_text)
            raise
        try:
            validated = validate_energy_flow_pressure_extraction_payload(raw_payload)
        except ValueError as exc:
            setattr(exc, "raw_payload", raw_payload)
            raise

        dropped_candidate_errors = list(validated["dropped_candidate_errors"])
        candidates = list(validated["candidates"])
        if _coerce_string(artifact.get("source_class")) == "trade_press":
            candidates, postfilter_errors = _apply_trade_press_energy_postfilter(
                artifact,
                candidates,
            )
            dropped_candidate_errors.extend(postfilter_errors)

        produced_candidates = bool(candidates)
        rejection_reason = validated["rejection_reason"]
        if not produced_candidates:
            rejection_reason = (
                rejection_reason
                or "No candidate retained after energy-flow postfilter."
            )

        return {
            "artifact_id": _coerce_string(artifact.get("artifact_id")),
            "source_class": _coerce_string(artifact.get("source_class")),
            "produced_candidates": produced_candidates,
            "candidates": candidates,
            "rejection_reason": rejection_reason,
            "dropped_candidate_errors": dropped_candidate_errors,
            "provider_name": self.provider,
            "model_name": self.model_name,
            "prompt_version": ENERGY_FLOW_EXTRACTION_PROMPT_VERSION,
            "extracted_at": _utc_now_iso(),
        }


def build_energy_flow_pressure_signal_batch(
    prefilter_batch: Dict[str, Any],
    *,
    extractor: Optional[EnergyFlowPressureExtractor] = None,
) -> Dict[str, Any]:
    """
    Run zero-context extraction on keep/review artifacts and instrument failures.
    """
    extractor = extractor or EnergyFlowPressureExtractor()
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
                    "raw_payload": getattr(exc, "raw_payload", None),
                }
            )
            continue
        except Exception as exc:  # pragma: no cover - defensive runtime path
            extraction_failures.append(
                {
                    "artifact_id": artifact.get("artifact_id"),
                    "prefilter_triage": triage,
                    "error_type": "extraction_runtime_error",
                    "exception_type": type(exc).__name__,
                    "error_message": str(exc),
                    "error_repr": repr(exc),
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
        "name": prefilter_batch.get("name", "energy_flow_pressure_signal_batch_v1"),
        "source_class": prefilter_batch.get("source_class", ""),
        "prompt_version": ENERGY_FLOW_EXTRACTION_PROMPT_VERSION,
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
