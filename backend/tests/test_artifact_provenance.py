import sys
import types
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path


APP_ROOT = Path(__file__).resolve().parents[1] / "app"
SERVICES_ROOT = APP_ROOT / "services"

app_pkg = types.ModuleType("app")
app_pkg.__path__ = [str(APP_ROOT)]
services_pkg = types.ModuleType("app.services")
services_pkg.__path__ = [str(SERVICES_ROOT)]
sys.modules["app"] = app_pkg
sys.modules["app.services"] = services_pkg

full_name = "app.services.artifact_provenance"
spec = spec_from_file_location(full_name, SERVICES_ROOT / "artifact_provenance.py")
module = module_from_spec(spec)
sys.modules[full_name] = module
assert spec.loader is not None
spec.loader.exec_module(module)


def test_classify_artifact_provenance_detects_example_dot_com():
    artifact = {"source_url": "https://example.com/releases/foo"}
    assert module.classify_artifact_provenance(artifact) == "synthetic_example"


def test_support_provenance_status_detects_real_only():
    artifacts = [{"source_url": "https://www.manufacturingdive.com/news/foo"}]
    assert module.support_provenance_status(artifacts) == "real_only"
