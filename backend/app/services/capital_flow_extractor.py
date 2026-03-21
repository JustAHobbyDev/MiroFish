"""
Zero-context LLM extraction for capital-flow signal candidates.

This module runs one artifact at a time through a fixed prompt and validates the
returned JSON against the v1 extraction contract.
"""

from __future__ import annotations

import os
import re
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
IMPLICATION_TYPE_ALIASES = {
    "direct_capital_allocation": "direct_capital_allocation",
    "capital_inflow": "direct_capital_allocation",
    "procurement_or_commitment_pull": "procurement_or_commitment_pull",
    "procurement_pull": "procurement_or_commitment_pull",
    "procurement pull": "procurement_or_commitment_pull",
    "commitment_pull": "procurement_or_commitment_pull",
    "capacity_response": "capacity_response",
    "capacity expansion": "capacity_response",
    "physical_buildout": "capacity_response",
    "physical buildout": "capacity_response",
    "architecture_induced_intensity": "architecture_induced_intensity",
    "architecture_induced_intensity_increase": "architecture_induced_intensity",
    "policy_enabled_buildout": "policy_enabled_buildout",
}


SYSTEM_PROMPT = """You are extracting possible capital-flow implications from a single public artifact.

Use only the artifact and its provenance.

Do not use prior knowledge about historical winners, bottlenecks, companies, themes, or the broader corpus.

Your job is not to form a thesis.

Your job is to decide whether this artifact alone contains one or more concrete observations that plausibly imply directional capital flow, procurement pull, capacity response, or physical buildout in a real system.

If no such implication is plausible from the artifact alone, return no candidates.

For this workflow, treat the following as no-candidate by default unless the artifact explicitly describes physical construction, facility expansion, equipment purchases, financing, contracted procurement, land opening for development, or similar concrete buildout:

- information collection renewals
- comment requests
- form/disclosure paperwork
- hearings or meetings
- administrative corrections
- exchange rule filings
- procedural regulatory maintenance notices
- patent or exclusive license notices without concrete buildout or committed spend

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


def _normalize_implication_type(value: Any) -> str:
    normalized = _coerce_string(value).strip().lower().replace("-", "_")
    if normalized in IMPLICATION_TYPE_ALIASES:
        return IMPLICATION_TYPE_ALIASES[normalized]
    if "procurement" in normalized or "commitment" in normalized or "order" in normalized:
        return "procurement_or_commitment_pull"
    if "capacity" in normalized or "buildout" in normalized or "build_out" in normalized:
        return "capacity_response"
    if "policy" in normalized:
        return "policy_enabled_buildout"
    if "architecture" in normalized or "intensity" in normalized:
        return "architecture_induced_intensity"
    if "capital" in normalized or "investment" in normalized:
        return "direct_capital_allocation"
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
            "rejection_reason": None if payload else "No plausible directional capital-flow implication can be inferred from the artifact alone.",
        }
    if not isinstance(payload, dict):
        raise ValueError("Extraction payload must be a JSON object.")

    candidates = payload.get("candidates")
    if candidates is None and isinstance(payload.get("results"), list):
        candidates = payload.get("results")
    if candidates is None and isinstance(payload.get("capital_flow_signal_candidates"), list):
        candidates = payload.get("capital_flow_signal_candidates")

    produced_candidates = payload.get("produced_candidates")
    if produced_candidates is None and isinstance(candidates, list):
        produced_candidates = bool(candidates)

    rejection_reason = payload.get("rejection_reason")
    if rejection_reason is None and produced_candidates is False:
        rejection_reason = "No plausible directional capital-flow implication can be inferred from the artifact alone."

    return {
        "produced_candidates": produced_candidates,
        "candidates": candidates,
        "rejection_reason": rejection_reason,
    }


POST_FILTER_ADMIN_NOISE_PATTERNS = (
    r"\binformation collection\b",
    r"\bsubmission for omb review\b",
    r"\bcomment request\b",
    r"\bsubmission for review\b",
    r"\bsunshine act meeting(?:s)?\b",
    r"\bnotice of filing\b",
    r"\bproposed rule change\b",
    r"\bimmediate effectiveness\b",
    r"\bposition and exercise limits\b",
    r"\badd liquidity order\b",
    r"\bpeg order\b",
    r"\bappraisals? for higher[- ]priced mortgage loans\b",
    r"\bhome loan cash[- ]out refinance loan comparison disclosure\b",
    r"\breport of construction contractor'?s wage rates\b",
    r"\breinstatement of disability annuity\b",
    r"\bexamination of records by comptroller general and contract audit\b",
)

POST_FILTER_OUT_OF_SCOPE_PATTERNS = (
    r"\bexclusive patent license\b",
    r"\bprospective grant of an exclusive patent license\b",
)

POST_FILTER_STRONG_BUILDOUT_PATTERNS = (
    r"\bconstruction permit\b",
    r"\blimited work authorization\b",
    r"\bbreaks? ground\b",
    r"\bconstruction\b",
    r"\bdemolition\b",
    r"\bnew plant\b",
    r"\bnew facility\b",
    r"\bmanufacturing\b",
    r"\bcommissioning\b",
    r"\bfinancing package\b",
    r"\bequipment purchases?\b",
    r"\bsite development\b",
    r"\bprocess-line installation\b",
    r"\bsupply agreement\b",
    r"\bproduction ramp\b",
    r"\bpublic land order\b",
    r"\bmineral and resource development\b",
    r"\bopened? .* land[s]? .* development\b",
)

TRADE_PRESS_REVIEW_STAGE_PRESSURE_PATTERNS = (
    r"\bpipeline\b",
    r"\bload growth\b",
    r"\bload increase\b",
    r"\bpeak load\b",
    r"\bload forecast\b",
    r"\bforecast turns positive\b",
    r"\bgrow(?:ing)? electric load\b",
    r"\bload to grow\b",
)

TRADE_PRESS_REVIEW_STAGE_CONCRETE_BUILDOUT_PATTERNS = (
    r"\bconstruction\b",
    r"\bbreaks? ground\b",
    r"\bbuild(?:ing|out)?\b",
    r"\bsite selection\b",
    r"\bselected site\b",
    r"\bpicks? .* location\b",
    r"\bconfirms? .* location\b",
    r"\bnew (?:facility|plant|factory|site)\b",
    r"\bfinancing\b",
    r"\bfunded\b",
    r"\bsecures? \$?\d",
    r"\binvest(?:s|ed|ing|ment|ments)?\b",
    r"\bspending plan\b",
    r"\bcapex\b",
    r"\bdeal\b",
    r"\bagreement\b",
    r"\bofftake\b",
    r"\binks?\b",
    r"\bsigns?\b",
)


def _artifact_text_for_post_filter(artifact: Dict[str, Any]) -> str:
    parts = [
        _coerce_string(artifact.get("title")),
        _coerce_string(artifact.get("body_text")),
    ]
    return "\n".join(part for part in parts if part).lower()


def _matches_any_pattern(text: str, patterns: tuple[str, ...]) -> bool:
    return any(re.search(pattern, text) for pattern in patterns)


def _should_force_no_candidate_after_extraction(artifact: Dict[str, Any]) -> Optional[str]:
    source_class = _coerce_string(artifact.get("source_class")).lower()
    text = _artifact_text_for_post_filter(artifact)
    title_text = _coerce_string(artifact.get("title")).lower()
    if "government" in source_class:
        has_strong_buildout = _matches_any_pattern(text, POST_FILTER_STRONG_BUILDOUT_PATTERNS)
        has_admin_noise = _matches_any_pattern(text, POST_FILTER_ADMIN_NOISE_PATTERNS)
        has_out_of_scope = _matches_any_pattern(text, POST_FILTER_OUT_OF_SCOPE_PATTERNS)

        if has_admin_noise and not has_strong_buildout:
            return "Administrative or procedural policy notice without concrete buildout or committed capital."
        if has_out_of_scope and not has_strong_buildout:
            return "Constrained-access or licensing notice without concrete rising-demand buildout evidence."

    if source_class == "trade_press" and _coerce_string(artifact.get("_prefilter_triage")).lower() == "review":
        title_has_pressure_signal = _matches_any_pattern(title_text, TRADE_PRESS_REVIEW_STAGE_PRESSURE_PATTERNS)
        title_has_concrete_buildout = _matches_any_pattern(title_text, TRADE_PRESS_REVIEW_STAGE_CONCRETE_BUILDOUT_PATTERNS)
        has_pressure_signal = _matches_any_pattern(text, TRADE_PRESS_REVIEW_STAGE_PRESSURE_PATTERNS)
        has_concrete_buildout = _matches_any_pattern(text, TRADE_PRESS_REVIEW_STAGE_CONCRETE_BUILDOUT_PATTERNS)
        if title_has_pressure_signal and not title_has_concrete_buildout:
            return "Planning-stage utility pipeline or load-forecast article without explicit spend, financing, siting, or construction."
        if has_pressure_signal and not has_concrete_buildout:
            return "Planning-stage utility pipeline or load-forecast article without explicit spend, financing, siting, or construction."
    return None


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
    implication_type = _normalize_implication_type(candidate.get("capital_flow_implication_type"))
    directness = _normalize_directness(candidate.get("observation_directness"))
    implication = _coerce_string(candidate.get("capital_flow_implication"))
    system_hints = _normalize_system_hints(candidate.get("system_hints"))
    physical_implication = _coerce_string(candidate.get("physical_implication"))
    confidence = _normalize_confidence(candidate.get("confidence"))

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
            validated = validate_capital_flow_extraction_payload(raw_payload)
        except ValueError as exc:
            setattr(exc, "raw_payload", raw_payload)
            raise
        heuristic_filter_reason = None
        if validated["produced_candidates"]:
            heuristic_filter_reason = _should_force_no_candidate_after_extraction(artifact)
            if heuristic_filter_reason:
                validated = {
                    "produced_candidates": False,
                    "candidates": [],
                    "rejection_reason": heuristic_filter_reason,
                }
        return {
            "artifact_id": _coerce_string(artifact.get("artifact_id")),
            "source_class": _coerce_string(artifact.get("source_class")),
            "produced_candidates": validated["produced_candidates"],
            "candidates": validated["candidates"],
            "rejection_reason": validated["rejection_reason"],
            "heuristic_filter_applied": bool(heuristic_filter_reason),
            "heuristic_filter_reason": heuristic_filter_reason,
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
