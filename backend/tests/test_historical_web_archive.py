import sys
import types
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
from urllib.error import HTTPError


APP_ROOT = Path(__file__).resolve().parents[1] / "app"
SERVICES_ROOT = APP_ROOT / "services"

app_pkg = types.ModuleType("app")
app_pkg.__path__ = [str(APP_ROOT)]
services_pkg = types.ModuleType("app.services")
services_pkg.__path__ = [str(SERVICES_ROOT)]
sys.modules["app"] = app_pkg
sys.modules["app.services"] = services_pkg

full_name = "app.services.historical_web_archive"
spec = spec_from_file_location(full_name, SERVICES_ROOT / "historical_web_archive.py")
module = module_from_spec(spec)
sys.modules[full_name] = module
assert spec.loader is not None
spec.loader.exec_module(module)


def test_normalize_historical_web_artifact_preserves_source_class() -> None:
    artifact = module.normalize_historical_web_artifact(
        {
            "source_class": "company_filing",
            "publisher_or_author": "TSMC",
            "issuing_company_name": "TSMC",
            "published_at": "2025-04-17",
            "title": "TSMC 2024 annual report",
            "source_url": "https://example.com/tsmc",
            "body_text": "Strong AI demand boosted advanced packaging.",
            "source_type": "company annual report",
            "corpus_entry_id": "tsmc_ar_2024_1",
        }
    )

    assert artifact["source_class"] == "company_filing"
    assert artifact["title"] == "TSMC 2024 annual report"
    assert artifact["artifact_metadata"]["source_type"] == "company annual report"


def test_build_historical_web_prefilter_batch_returns_mixed_source_classes() -> None:
    batch = module.build_historical_web_prefilter_batch(
        [
            {
                "source_class": "company_release",
                "publisher_or_author": "Micron",
                "issuing_company_name": "Micron",
                "published_at": "2025-01-08",
                "title": "Micron breaks ground on new HBM advanced packaging facility",
                "source_url": "https://example.com/micron",
                "body_text": "Micron breaks ground on a new HBM advanced packaging facility in Singapore.",
                "source_type": "company press release",
                "corpus_entry_id": "micron_1",
            },
                {
                    "source_class": "company_filing",
                    "publisher_or_author": "TSMC",
                    "issuing_company_name": "TSMC",
                    "published_at": "2025-04-17",
                    "title": "TSMC annual report says strong AI demand boosted advanced packaging expansion",
                    "source_url": "https://example.com/tsmc",
                    "body_text": "Strong AI demand boosted advanced packaging and CoWoS, requiring continued capacity expansion and capital investment.",
                    "source_type": "company annual report",
                    "corpus_entry_id": "tsmc_1",
                },
        ],
        batch_name="historical_web_test",
    )

    assert batch["source_classes"] == ["company_filing", "company_release"]
    assert batch["metrics"]["processed_artifact_count"] == 2
    assert batch["metrics"]["kept_count"] >= 1


def test_build_historical_web_prefilter_batch_filing_aware_keeps_filing_capacity_language() -> None:
    batch = module.build_historical_web_prefilter_batch(
        [
            {
                "source_class": "company_filing",
                "publisher_or_author": "TSMC",
                "issuing_company_name": "TSMC",
                "published_at": "2025-04-17",
                "title": "TSMC 2024 Annual Report",
                "source_url": "https://example.com/tsmc",
                "body_text": "Strong AI demand boosted advanced packaging and CoWoS, requiring continued capacity expansion and capital investment.",
                "source_type": "company annual report",
                "corpus_entry_id": "tsmc_1",
            }
        ],
        batch_name="historical_web_filing_aware_test",
        filing_aware=True,
    )

    assert batch["metrics"]["kept_count"] == 1
    assert batch["kept_artifacts"][0]["_prefilter"]["reason"].startswith("Historical filing-aware override")


def test_fetch_historical_web_record_falls_back_to_curl_for_sec_403(monkeypatch) -> None:
    def _raise_http_error(*args, **kwargs):
        raise HTTPError(
            url="https://www.sec.gov/example",
            code=403,
            msg="Forbidden",
            hdrs=None,
            fp=None,
        )

    def _fake_curl(source_url: str) -> str:
        assert "sec.gov" in source_url
        return """
        <html>
          <head>
            <title>AXT 10-Q 2025-03-31</title>
            <meta name="article:published_time" content="2025-05-01" />
          </head>
          <body>
            <article>AXT reported indium phosphide demand tied to AI infrastructure.</article>
          </body>
        </html>
        """

    monkeypatch.setattr(module, "_fetch_via_urllib", _raise_http_error)
    monkeypatch.setattr(module, "_fetch_via_curl", _fake_curl)

    record = module.fetch_historical_web_record(
        {
            "source_class": "company_filing",
            "source_type": "company filing",
            "publisher_or_author": "AXT",
            "issuing_company_name": "AXT",
            "published_at": "2025-03-31",
            "source_url": "https://www.sec.gov/Archives/edgar/data/1051627/example.htm",
            "title_hint": "AXT 10-Q 2025-03-31",
            "corpus_entry_id": "axt_10q_test",
        }
    )

    assert record["title"] == "AXT 10-Q 2025-03-31"
    assert record["published_at"] == "2025-05-01"
    assert "indium phosphide demand" in record["body_text"].lower()
