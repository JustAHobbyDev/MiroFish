import sys
import types
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path


APP_ROOT = Path(__file__).resolve().parents[1] / "app"
SERVICES_ROOT = APP_ROOT / "services"
UTILS_ROOT = APP_ROOT / "utils"

app_pkg = types.ModuleType("app")
app_pkg.__path__ = [str(APP_ROOT)]
services_pkg = types.ModuleType("app.services")
services_pkg.__path__ = [str(SERVICES_ROOT)]
utils_pkg = types.ModuleType("app.utils")
utils_pkg.__path__ = [str(UTILS_ROOT)]
sys.modules["app"] = app_pkg
sys.modules["app.services"] = services_pkg
sys.modules["app.utils"] = utils_pkg

llm_full_name = "app.utils.llm_client"
llm_spec = spec_from_file_location(llm_full_name, UTILS_ROOT / "llm_client.py")
llm_module = module_from_spec(llm_spec)
sys.modules[llm_full_name] = llm_module
assert llm_spec.loader is not None
llm_spec.loader.exec_module(llm_module)

full_name = "app.services.capital_flow_extractor"
spec = spec_from_file_location(full_name, SERVICES_ROOT / "capital_flow_extractor.py")
module = module_from_spec(spec)
sys.modules[full_name] = module
assert spec.loader is not None
spec.loader.exec_module(module)


class _FakeLLMClient:
    def __init__(self, payload):
        self.payload = payload
        self.calls = []

    def chat(self, messages, temperature=0.0, max_tokens=0, response_format=None):
        self.calls.append(
            {
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens,
                "response_format": response_format,
            }
        )
        return self.payload

    @staticmethod
    def parse_json_text(response):
        import json

        return json.loads(response)


def _sample_artifact():
    return {
        "artifact_id": "art_1",
        "source_class": "company_release",
        "publisher_or_author": "Business Wire",
        "published_at": "2026-01-10T00:00:00Z",
        "title": "Factory Co breaks ground on new battery materials plant",
        "source_url": "https://example.com/release/1",
        "body_text": "Factory Co announced construction of a new plant to expand output.",
    }


def test_validate_capital_flow_extraction_payload_accepts_valid_no_candidate():
    payload = {
        "produced_candidates": False,
        "candidates": [],
        "rejection_reason": "No plausible directional capital-flow implication can be inferred from the artifact alone.",
    }
    validated = module.validate_capital_flow_extraction_payload(payload)
    assert validated["produced_candidates"] is False
    assert validated["candidates"] == []


def test_validate_capital_flow_extraction_payload_coerces_string_boolean_and_null_candidates():
    payload = {
        "produced_candidates": "false",
        "candidates": None,
        "rejection_reason": "No direct buildout signal.",
    }
    validated = module.validate_capital_flow_extraction_payload(payload)
    assert validated["produced_candidates"] is False
    assert validated["candidates"] == []


def test_validate_capital_flow_extraction_payload_accepts_top_level_candidate_list():
    payload = [
        {
            "observable_statement": "The company announced a new plant.",
            "capital_flow_implication_type": "physical buildout",
            "observation_directness": "direct",
            "capital_flow_implication": "Capital is moving into capacity expansion.",
            "system_hints": ["industrial plant"],
            "physical_implication": "New manufacturing capacity is being added.",
            "confidence": 0.82,
        }
    ]
    validated = module.validate_capital_flow_extraction_payload(payload)
    assert validated["produced_candidates"] is True
    assert validated["candidates"][0]["capital_flow_implication_type"] == "capacity_response"
    assert validated["candidates"][0]["confidence"] == "high"


def test_validate_capital_flow_extraction_payload_infers_produced_candidates_from_candidates():
    payload = {
        "candidates": [
            {
                "observable_statement": "The company announced a new contract.",
                "capital_flow_implication_type": "procurement_pull",
                "observation_directness": "direct",
                "capital_flow_implication": "Committed demand is increasing.",
                "system_hints": ["industrial components"],
                "physical_implication": "Suppliers may need to raise throughput.",
                "confidence": 0.6,
            }
        ],
        "rejection_reason": None,
    }
    validated = module.validate_capital_flow_extraction_payload(payload)
    assert validated["produced_candidates"] is True
    assert validated["candidates"][0]["capital_flow_implication_type"] == "procurement_or_commitment_pull"
    assert validated["candidates"][0]["confidence"] == "medium"


def test_validate_capital_flow_extraction_payload_accepts_candidate_alias_key_and_directness_alias():
    payload = {
        "capital_flow_signal_candidates": [
            {
                "observable_statement": "A company broke ground on a new plant.",
                "capital_flow_implication_type": "capital investment",
                "observation_directness": "high",
                "capital_flow_implication": "Spending is moving into plant construction.",
                "system_hints": "industrial plant",
                "physical_implication": "new facility construction",
                "confidence": "medium",
            }
        ]
    }
    validated = module.validate_capital_flow_extraction_payload(payload)
    assert validated["produced_candidates"] is True
    assert validated["candidates"][0]["capital_flow_implication_type"] == "direct_capital_allocation"
    assert validated["candidates"][0]["observation_directness"] == "direct"


def test_validate_capital_flow_extraction_payload_fills_missing_rejection_reason_for_explicit_no_candidate():
    payload = {
        "produced_candidates": False,
        "candidates": [],
        "rejection_reason": None,
    }
    validated = module.validate_capital_flow_extraction_payload(payload)
    assert validated["produced_candidates"] is False
    assert validated["rejection_reason"]


def test_extractor_returns_valid_candidate_batch():
    llm = _FakeLLMClient(
        """
        {
            "produced_candidates": true,
            "candidates": [
                {
                    "observable_statement": "The company is building a new manufacturing plant.",
                    "capital_flow_implication_type": "capacity_response",
                    "observation_directness": "direct",
                    "capital_flow_implication": "The release implies active capital deployment into manufacturing capacity.",
                    "system_hints": ["battery materials"],
                    "physical_implication": "More physical production capacity is being added to this manufacturing layer.",
                    "confidence": "high"
                }
            ],
            "rejection_reason": null
        }
        """
    )
    extractor = module.CapitalFlowExtractor(
        llm_client=llm,
        provider="openai",
        model_name="gpt-4o-mini",
    )

    result = extractor.extract_from_artifact(_sample_artifact())

    assert result["produced_candidates"] is True
    assert len(result["candidates"]) == 1
    assert result["provider_name"] == "openai"
    assert result["model_name"] == "gpt-4o-mini"
    assert llm.calls[0]["temperature"] == 0.1
    assert llm.calls[0]["response_format"] is None


def test_build_capital_flow_signal_batch_instruments_schema_failures():
    llm = _FakeLLMClient(
        """
        {
            "produced_candidates": true,
            "candidates": [],
            "rejection_reason": null
        }
        """
    )
    extractor = module.CapitalFlowExtractor(
        llm_client=llm,
        provider="openai",
        model_name="gpt-4o-mini",
    )
    batch = {
        "name": "prefilter_batch",
        "source_class": "company_release",
        "kept_artifacts": [_sample_artifact()],
        "review_artifacts": [],
    }

    result = module.build_capital_flow_signal_batch(batch, extractor=extractor)

    assert result["metrics"]["schema_failure_count"] == 1
    assert result["metrics"]["successful_extractions"] == 0
    assert result["schema_failures"][0]["error_type"] == "schema_validation_error"


def test_build_capital_flow_signal_batch_counts_review_candidates():
    llm = _FakeLLMClient(
        """
        {
            "produced_candidates": true,
            "candidates": [
                {
                    "observable_statement": "The release announces a supply agreement for new production.",
                    "capital_flow_implication_type": "procurement_or_commitment_pull",
                    "observation_directness": "direct",
                    "capital_flow_implication": "The agreement implies committed directional demand into this production system.",
                    "system_hints": ["industrial components"],
                    "physical_implication": "Committed procurement may pull additional capacity into the supply chain.",
                    "confidence": "medium"
                }
            ],
            "rejection_reason": null
        }
        """
    )
    extractor = module.CapitalFlowExtractor(
        llm_client=llm,
        provider="openai",
        model_name="gpt-4o-mini",
    )
    artifact = _sample_artifact()
    batch = {
        "name": "prefilter_batch",
        "source_class": "company_release",
        "kept_artifacts": [],
        "review_artifacts": [artifact],
    }

    result = module.build_capital_flow_signal_batch(batch, extractor=extractor)

    assert result["metrics"]["review_artifact_count"] == 1
    assert result["metrics"]["review_candidate_artifact_count"] == 1
    assert result["processed_results"][0]["prefilter_triage"] == "review"
