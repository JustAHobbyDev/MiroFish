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

full_name = "app.services.energy_flow_pressure_extractor"
spec = spec_from_file_location(full_name, SERVICES_ROOT / "energy_flow_pressure_extractor.py")
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


class _FailingLLMClient:
    def chat(self, messages, temperature=0.0, max_tokens=0, response_format=None):
        raise RuntimeError("simulated runtime failure")

    @staticmethod
    def parse_json_text(response):
        raise AssertionError("parse_json_text should not be called on runtime failure")


def _sample_trade_press_pipeline_artifact():
    return {
        "artifact_id": "trade_energy_1",
        "source_class": "trade_press",
        "publisher_or_author": "Utility Dive",
        "published_at": "2026-02-01",
        "title": "PG&E data center pipeline swells to 10GW",
        "source_url": "https://example.com/trade/pgande",
        "body_text": "The utility said its data center pipeline continues to grow as load forecasts rise.",
    }


def _sample_trade_press_dual_role_artifact():
    return {
        "artifact_id": "trade_energy_2",
        "source_class": "trade_press",
        "publisher_or_author": "Utility Dive",
        "published_at": "2026-02-20",
        "title": "As load grows, Southern raises spending plan to $81B",
        "source_url": "https://example.com/trade/southern",
        "body_text": "Southern Company raised its five-year spending plan to $81 billion and is working on adding 10GW of approved new generation.",
    }


def test_validate_energy_flow_pressure_payload_accepts_valid_no_candidate():
    payload = {
        "produced_candidates": False,
        "candidates": [],
        "rejection_reason": "No plausible energy-system pressure implication can be inferred from the artifact alone.",
    }
    validated = module.validate_energy_flow_pressure_extraction_payload(payload)
    assert validated["produced_candidates"] is False
    assert validated["candidates"] == []


def test_validate_energy_flow_pressure_payload_accepts_aliases():
    payload = {
        "energy_flow_pressure_signals": [
            {
                "observable_statement": "The utility pipeline has risen materially.",
                "energy_pressure_type": "pipeline pressure",
                "observation_directness": "high",
                "energy_flow_implication": "Future electricity demand is likely rising.",
                "system_hints": "utility grid",
                "physical_implication": "More generation and grid infrastructure may be needed.",
                "relationship_to_capital_flow": "both",
                "confidence": 0.8,
            }
        ]
    }
    validated = module.validate_energy_flow_pressure_extraction_payload(payload)
    assert validated["produced_candidates"] is True
    assert validated["candidates"][0]["energy_pressure_type"] == "pipeline_pressure"
    assert validated["candidates"][0]["observation_directness"] == "direct"
    assert validated["candidates"][0]["relationship_to_capital_flow"] == "energy_flow_pressure_and_capital_flow"
    assert validated["candidates"][0]["confidence"] == "high"


def test_validate_energy_flow_pressure_payload_accepts_observed_smoke_aliases():
    payload = {
        "energy_flow_pressure_signals": [
            {
                "observable_statement": "Southern raised its spending plan.",
                "energy_pressure_type": "capital investment pressure",
                "observation_directness": "direct",
                "energy_flow_implication": "More generation investment is likely needed.",
                "system_hints": ["utility generation"],
                "physical_implication": "New generation capacity may be added.",
                "relationship_to_capital_flow": "energy_flow_pressure_and_capital_flow",
                "confidence": "high"
            },
            {
                "observable_statement": "Large-load demand is rising.",
                "energy_pressure_type": "demand pressure",
                "observation_directness": "direct",
                "energy_flow_implication": "Load growth is increasing.",
                "system_hints": ["utility load"],
                "physical_implication": "More grid capacity may be needed.",
                "relationship_to_capital_flow": "energy_flow_pressure_only",
                "confidence": "medium"
            },
            {
                "observable_statement": "The company is adding new generation.",
                "energy_pressure_type": "supply pressure",
                "observation_directness": "direct",
                "energy_flow_implication": "New infrastructure is needed to meet demand.",
                "system_hints": ["generation capacity"],
                "physical_implication": "Generation buildout may occur.",
                "relationship_to_capital_flow": "energy_flow_pressure_and_capital_flow",
                "confidence": "high"
            }
        ]
    }
    validated = module.validate_energy_flow_pressure_extraction_payload(payload)
    assert validated["produced_candidates"] is True
    assert validated["candidates"][0]["energy_pressure_type"] == "infrastructure_response_need"
    assert validated["candidates"][1]["energy_pressure_type"] == "load_growth"
    assert validated["candidates"][2]["energy_pressure_type"] == "infrastructure_response_need"


def test_validate_energy_flow_pressure_payload_accepts_singular_key_and_trimmed_field_names():
    payload = {
        "energy_flow_pressure_signal": [
            {
                "observable_statement": "A plant is being established for power-generator infrastructure.",
                "energy_pressure_type": "increased demand for energy infrastructure",
                " observation_directness": "direct",
                "energy_flow_implication": "Power infrastructure demand is increasing.",
                "system_hints": "power generators",
                "physical_implication": "More supporting infrastructure may be needed.",
                "relationship_to_capital_flow": "energy_flow_pressure_and_capital_flow",
                "confidence": "high"
            }
        ]
    }
    validated = module.validate_energy_flow_pressure_extraction_payload(payload)
    assert validated["produced_candidates"] is True
    assert validated["candidates"][0]["energy_pressure_type"] == "infrastructure_response_need"
    assert validated["candidates"][0]["observation_directness"] == "direct"


def test_validate_energy_flow_pressure_payload_accepts_full_batch_aliases():
    payload = {
        "energy_flow_pressure_signals": [
            {
                "observable_statement": "Facility upgrades imply more on-site power draw.",
                "energy_pressure_type": "increased energy consumption",
                "observation_directness": "direct",
                "energy_flow_implication": "Electricity demand is likely to rise at the upgraded sites.",
                "system_hints": ["manufacturing facilities"],
                "physical_implication": "More grid capacity may be needed.",
                "relationship_to_capital_flow": "energy_flow_pressure_and_capital_flow",
                "confidence": "high",
            },
            {
                "observable_statement": "Data-center demand is rising in a defined sector.",
                "energy_pressure_type": "rising energy demand from specific sectors",
                "observation_directness": "direct",
                "energy_flow_implication": "Sector-specific electricity demand is increasing.",
                "system_hints": ["data centers"],
                "physical_implication": "Generation and transmission needs may grow.",
                "relationship_to_capital_flow": "energy_flow_pressure_only",
                "confidence": "medium",
            },
            {
                "observable_statement": "Regional supply could become strained.",
                "energy_pressure_type": "supply adequacy concern",
                "observation_directness": "indirect",
                "energy_flow_implication": "Existing energy supply may be insufficient.",
                "system_hints": ["regional grid"],
                "physical_implication": "Capacity tightness may emerge.",
                "relationship_to_capital_flow": "energy_flow_pressure_only",
                "confidence": "medium",
            },
            {
                "observable_statement": "Production growth will require more energy inputs.",
                "energy_pressure_type": "increased energy requirements for production",
                "observation_directness": "direct",
                "energy_flow_implication": "Industrial production is likely to increase power demand.",
                "system_hints": ["factory production"],
                "physical_implication": "More electricity infrastructure may be needed.",
                "relationship_to_capital_flow": "energy_flow_pressure_and_capital_flow",
                "confidence": "high",
            },
        ]
    }
    validated = module.validate_energy_flow_pressure_extraction_payload(payload)
    assert validated["produced_candidates"] is True
    assert validated["candidates"][0]["energy_pressure_type"] == "load_growth"
    assert validated["candidates"][1]["energy_pressure_type"] == "load_growth"
    assert validated["candidates"][2]["energy_pressure_type"] == "capacity_tightness"
    assert validated["candidates"][3]["energy_pressure_type"] == "infrastructure_response_need"


def test_validate_energy_flow_pressure_payload_drops_invalid_secondary_candidates():
    payload = {
        "produced_candidates": True,
        "candidates": [
            {
                "observable_statement": "The utility pipeline has risen materially.",
                "energy_pressure_type": "pipeline pressure",
                "observation_directness": "direct",
                "energy_flow_implication": "Future electricity demand is likely rising.",
                "system_hints": "utility grid",
                "physical_implication": "More generation and grid infrastructure may be needed.",
                "relationship_to_capital_flow": "energy_flow_pressure_only",
                "confidence": "high",
            },
            {
                "observable_statement": "The project will create many jobs.",
                "energy_pressure_type": "job creation in energy sectors",
                "observation_directness": "indirect",
                "energy_flow_implication": "Hiring may support future production.",
                "system_hints": "energy manufacturing",
                "physical_implication": "More labor may be needed.",
                "relationship_to_capital_flow": "energy_flow_pressure_only",
                "confidence": "medium",
            },
        ],
    }
    validated = module.validate_energy_flow_pressure_extraction_payload(payload)
    assert validated["produced_candidates"] is True
    assert len(validated["candidates"]) == 1
    assert validated["candidates"][0]["energy_pressure_type"] == "pipeline_pressure"
    assert len(validated["dropped_candidate_errors"]) == 1
    assert "job creation in energy sectors" in validated["dropped_candidate_errors"][0]


def test_energy_flow_extractor_returns_pipeline_pressure_candidate():
    llm = _FakeLLMClient(
        """
        {
          "produced_candidates": true,
          "candidates": [
            {
              "observable_statement": "PG&E's data center pipeline has grown to 10GW.",
              "energy_pressure_type": "pipeline_pressure",
              "observation_directness": "direct",
              "energy_flow_implication": "Expected data-center demand is likely to place substantial pressure on the utility power system.",
              "system_hints": ["utility grid", "data center power demand"],
              "physical_implication": "Generation, transmission, and transformer capacity may need to expand.",
              "relationship_to_capital_flow": "energy_flow_pressure_only",
              "confidence": "medium"
            }
          ],
          "rejection_reason": null
        }
        """
    )
    extractor = module.EnergyFlowPressureExtractor(
        llm_client=llm,
        provider="openai",
        model_name="gpt-4o-mini",
    )

    result = extractor.extract_from_artifact(_sample_trade_press_pipeline_artifact())

    assert result["produced_candidates"] is True
    assert result["candidates"][0]["relationship_to_capital_flow"] == "energy_flow_pressure_only"
    assert llm.calls[0]["response_format"] is None


def test_energy_flow_extractor_returns_dual_role_candidate():
    llm = _FakeLLMClient(
        """
        {
          "produced_candidates": true,
          "candidates": [
            {
              "observable_statement": "Southern raised its spending plan to $81 billion as load grows.",
              "energy_pressure_type": "load_growth",
              "observation_directness": "direct",
              "energy_flow_implication": "Rising load is putting pressure on the energy system.",
              "system_hints": ["utility generation", "data center demand"],
              "physical_implication": "New generation and grid capacity will be required.",
              "relationship_to_capital_flow": "energy_flow_pressure_and_capital_flow",
              "confidence": "high"
            }
          ],
          "rejection_reason": null
        }
        """
    )
    extractor = module.EnergyFlowPressureExtractor(
        llm_client=llm,
        provider="openai",
        model_name="gpt-4o-mini",
    )

    result = extractor.extract_from_artifact(_sample_trade_press_dual_role_artifact())

    assert result["produced_candidates"] is True
    assert result["candidates"][0]["relationship_to_capital_flow"] == "energy_flow_pressure_and_capital_flow"


def test_build_energy_flow_pressure_signal_batch_counts_review_candidates():
    llm = _FakeLLMClient(
        """
        {
          "produced_candidates": true,
          "candidates": [
            {
              "observable_statement": "The utility's pipeline has grown substantially.",
              "energy_pressure_type": "pipeline_pressure",
              "observation_directness": "direct",
              "energy_flow_implication": "Future energy demand is rising.",
              "system_hints": ["utility grid"],
              "physical_implication": "The grid may need upgrades.",
              "relationship_to_capital_flow": "energy_flow_pressure_only",
              "confidence": "medium"
            }
          ],
          "rejection_reason": null
        }
        """
    )
    extractor = module.EnergyFlowPressureExtractor(
        llm_client=llm,
        provider="openai",
        model_name="gpt-4o-mini",
    )
    artifact = _sample_trade_press_pipeline_artifact()
    batch = {
        "name": "prefilter_batch",
        "source_class": "trade_press",
        "kept_artifacts": [],
        "review_artifacts": [artifact],
    }

    result = module.build_energy_flow_pressure_signal_batch(batch, extractor=extractor)

    assert result["metrics"]["review_artifact_count"] == 1
    assert result["metrics"]["review_candidate_artifact_count"] == 1
    assert result["processed_results"][0]["prefilter_triage"] == "review"


def test_build_energy_flow_pressure_signal_batch_captures_runtime_exception_metadata():
    extractor = module.EnergyFlowPressureExtractor(
        llm_client=_FailingLLMClient(),
        provider="openai",
        model_name="gpt-4o-mini",
    )
    batch = {
        "name": "prefilter_batch",
        "source_class": "trade_press",
        "kept_artifacts": [_sample_trade_press_pipeline_artifact()],
        "review_artifacts": [],
    }

    result = module.build_energy_flow_pressure_signal_batch(batch, extractor=extractor)

    assert result["metrics"]["extraction_failure_count"] == 1
    failure = result["extraction_failures"][0]
    assert failure["exception_type"] == "RuntimeError"
    assert failure["error_repr"] == "RuntimeError('simulated runtime failure')"
