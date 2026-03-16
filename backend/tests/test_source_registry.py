import sys
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path


MODULE_PATH = (
    Path(__file__).resolve().parents[1] / "app" / "services" / "source_registry.py"
)
MODULE_SPEC = spec_from_file_location("source_registry", MODULE_PATH)
source_registry = module_from_spec(MODULE_SPEC)
assert MODULE_SPEC.loader is not None
sys.modules[MODULE_SPEC.name] = source_registry
MODULE_SPEC.loader.exec_module(source_registry)


def test_build_source_registry_from_docs():
    payload = source_registry.build_source_registry_from_docs()

    assert payload["registry_version"] == "v1"
    assert payload["row_count"] == len(payload["rows"])
    assert payload["row_count"] >= 40

    rows_by_name = {row["name"]: row for row in payload["rows"]}

    bis = rows_by_name["Bureau of Industry and Security (BIS), U.S. Department of Commerce"]
    assert bis["source_class"] == "government_policy_enforcement"
    assert bis["priority_tier"] == "P0"
    assert bis["role"] == "graph_forming"
    assert bis["canonical_url"] == "https://www.bis.doc.gov/"

    sec = rows_by_name["SEC EDGAR Database (10-K, 10-Q, 8-K, 20-F)"]
    assert sec["source_class"] == "company_filing"
    assert sec["suggested_ingestion_class"] == "company_filing"

    linked_in = rows_by_name["LinkedIn Jobs"]
    assert linked_in["source_class"] == "job_posting_hiring_signal"
    assert linked_in["requires_login"] is True

    assert Path(payload["generated_from"][0]).name == "2026-03-16-source-investigation-list-v1.md"
