import sys
import types
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path


APP_ROOT = Path(__file__).resolve().parents[1] / "app"
UTILS_ROOT = APP_ROOT / "utils"

app_pkg = types.ModuleType("app")
app_pkg.__path__ = [str(APP_ROOT)]
utils_pkg = types.ModuleType("app.utils")
utils_pkg.__path__ = [str(UTILS_ROOT)]
sys.modules["app"] = app_pkg
sys.modules["app.utils"] = utils_pkg

full_name = "app.utils.llm_client"
spec = spec_from_file_location(full_name, UTILS_ROOT / "llm_client.py")
module = module_from_spec(spec)
sys.modules[full_name] = module
assert spec.loader is not None
spec.loader.exec_module(module)


def test_resolve_openai_provider_settings_uses_explicit_values():
    settings = module.resolve_llm_provider_settings(
        provider="openai",
        api_key="openai-key",
        base_url="https://api.openai.example/v1",
        model="gpt-4o-mini",
    )

    assert settings["provider"] == "openai"
    assert settings["api_key"] == "openai-key"
    assert settings["base_url"] == "https://api.openai.example/v1"
    assert settings["model"] == "gpt-4o-mini"


def test_resolve_groq_provider_settings_uses_explicit_values():
    settings = module.resolve_llm_provider_settings(
        provider="groq",
        api_key="groq-key",
        base_url="https://api.groq.example/openai/v1",
        model="llama-3.1-8b-instant",
    )

    assert settings["provider"] == "groq"
    assert settings["api_key"] == "groq-key"
    assert settings["base_url"] == "https://api.groq.example/openai/v1"
    assert settings["model"] == "llama-3.1-8b-instant"


def test_resolve_provider_settings_rejects_unsupported_provider():
    try:
        module.resolve_llm_provider_settings(
            provider="not-a-provider",
            api_key="x",
            base_url="https://example.com",
            model="m",
        )
    except ValueError as exc:
        assert "Unsupported LLM provider" in str(exc)
    else:  # pragma: no cover - defensive safety
        raise AssertionError("Expected ValueError for unsupported provider")
