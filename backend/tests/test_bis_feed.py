import sys
import types
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SERVICES_ROOT = Path(__file__).resolve().parents[1] / "app" / "services"

app_pkg = types.ModuleType("app")
app_pkg.__path__ = []
services_pkg = types.ModuleType("app.services")
services_pkg.__path__ = [str(SERVICES_ROOT)]
sys.modules["app"] = app_pkg
sys.modules["app.services"] = services_pkg

profiles_full_name = "app.services.federal_register_query_profiles"
profiles_spec = spec_from_file_location(profiles_full_name, SERVICES_ROOT / "federal_register_query_profiles.py")
profiles_module = module_from_spec(profiles_spec)
sys.modules[profiles_full_name] = profiles_module
assert profiles_spec.loader is not None
profiles_spec.loader.exec_module(profiles_module)

relevance_full_name = "app.services.federal_register_relevance"
relevance_spec = spec_from_file_location(relevance_full_name, SERVICES_ROOT / "federal_register_relevance.py")
relevance_module = module_from_spec(relevance_spec)
sys.modules[relevance_full_name] = relevance_module
assert relevance_spec.loader is not None
relevance_spec.loader.exec_module(relevance_module)

full_name = "app.services.bis_feed"
spec = spec_from_file_location(full_name, SERVICES_ROOT / "bis_feed.py")
module = module_from_spec(spec)
sys.modules[full_name] = module
assert spec.loader is not None
spec.loader.exec_module(module)


SAMPLE_HTML = """
<html>
  <body>
    <h2>Special Issues</h2>
    <h4>Section 232 Investigation on Processed Critical Minerals and Derivative Products</h4>
    <p>
      Effective March 4, 2026, BIS opened a Section 232 investigation on processed
      critical minerals, rare earth magnet supply, and downstream derivative products.
      <a href="/section-232-critical-minerals">Read more</a>
    </p>
    <h4>Guidance on Semiconductor Export Controls</h4>
    <p>
      Semiconductor equipment and wafer fabrication controls were updated for advanced
      packaging and foundry supply chains.
      <a href="/semiconductor-guidance">Guidance</a>
    </p>

    <h2>Read the latest News &amp; Updates</h2>
    <a href="/news-updates/2026/export-controls-robotics">BIS Tightens Robotics Export Controls</a>
    <div>March 18, 2026</div>
    <p>Robotics systems and industrial automation exporters face new controls.</p>

    <a href="/news-updates/2026/entity-list-furnaces">Consumer Furnace Labeling Update</a>
    <div>March 12, 2026</div>
    <p>Consumer furnaces and home appliances receive updated efficiency guidance.</p>

    <a href="/news-updates">See more News &amp; Updates</a>
  </body>
</html>
"""


class _FakeHtmlResponse:
    def __init__(self, html: str):
        self._html = html

    def read(self):
        return self._html.encode("utf-8")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False


def test_parse_bis_homepage_items_extracts_special_issues_and_news():
    items = module.parse_bis_homepage_items(SAMPLE_HTML)

    assert len(items) == 4
    assert items[0]["section"] == "special_issue"
    assert items[0]["published_at"] == "2026-03-04"
    assert items[0]["canonical_url"] == "https://media.bis.gov/section-232-critical-minerals"

    assert items[2]["section"] == "news_update"
    assert items[2]["title"] == "BIS Tightens Robotics Export Controls"
    assert items[2]["published_at"] == "2026-03-18"


def test_fetch_bis_policy_feed_normalizes_results(monkeypatch):
    def fake_urlopen(request, timeout=20):
        return _FakeHtmlResponse(SAMPLE_HTML)

    monkeypatch.setattr(module, "urlopen", fake_urlopen)

    payload = module.fetch_bis_policy_feed(
        query="critical minerals",
        target_themes=["critical_materials"],
        focus_process_layers=["Rare Earth Separation"],
        focus_geographies=["China"],
        ticker_refs=["MP"],
        policy_scope=["industrial_policy"],
        minimum_relevance_score=0,
    )

    assert payload["fetch_metadata"]["raw_result_count"] == 4
    assert payload["fetch_metadata"]["candidate_count"] == 1
    assert len(payload["feed_documents"]) == 1

    first = payload["feed_documents"][0]
    assert first["source_target_id"] == "src_target_bis_updates"
    assert first["source_target_name"] == "Bureau of Industry and Security (BIS), U.S. Department of Commerce"
    assert first["publisher"] == "Bureau of Industry and Security"
    assert first["ticker_refs"] == ["MP"]
    assert "critical_materials" in first["theme_refs"]
    assert "Rare Earth Separation" in first["matched_process_layers"]


def test_fetch_bis_policy_feed_with_query_profile(monkeypatch):
    def fake_urlopen(request, timeout=20):
        return _FakeHtmlResponse(SAMPLE_HTML)

    monkeypatch.setattr(module, "urlopen", fake_urlopen)

    payload = module.fetch_bis_policy_feed(
        query_profile="semiconductors",
        minimum_relevance_score=0,
    )

    assert payload["fetch_metadata"]["query_profile"] == "semiconductors"
    assert payload["theme"] == "semiconductors"
    assert len(payload["feed_documents"]) == 1
    assert payload["feed_documents"][0]["title"] == "Guidance on Semiconductor Export Controls"
    assert "NVDA" in payload["feed_documents"][0]["ticker_refs"]


def test_fetch_bis_policy_feed_excludes_adjacent_when_requested(monkeypatch):
    adjacent_html = """
    <html>
      <body>
        <h2>Read the latest News &amp; Updates</h2>
        <a href="/news-updates/2026/supply-chain">Supply Chain Resilience Guidance</a>
        <div>March 18, 2026</div>
        <p>Supply chain disclosure requirements expand for strategic sectors.</p>
      </body>
    </html>
    """

    def fake_urlopen(request, timeout=20):
        return _FakeHtmlResponse(adjacent_html)

    monkeypatch.setattr(module, "urlopen", fake_urlopen)

    payload = module.fetch_bis_policy_feed(
        query="supply chain",
        minimum_relevance_score=0,
        include_adjacent=False,
    )

    assert payload["fetch_metadata"]["candidate_count"] == 1
    assert payload["fetch_metadata"]["result_count"] == 0


def test_fetch_bis_policy_feed_drops_share_and_nav_noise(monkeypatch):
    noisy_html = """
    <html>
      <body>
        <h2>Read the latest News &amp; Updates</h2>
        <a href="/external/external?url=https://www.linkedin.com/company/bis">Share to LinkedIn</a>
        <p>Advancing U.S. national security and export control leadership.</p>
        <a href="/licensing/bis-forms">BIS forms</a>
        <p>BIS forms</p>
        <a href="/news-updates/2026/entity-list-update">Entity List Update for Advanced Computing</a>
        <div>March 18, 2026</div>
        <p>BIS expands export control restrictions for advanced computing items.</p>
      </body>
    </html>
    """

    def fake_urlopen(request, timeout=20):
        return _FakeHtmlResponse(noisy_html)

    monkeypatch.setattr(module, "urlopen", fake_urlopen)

    payload = module.fetch_bis_policy_feed(
        minimum_relevance_score=0,
    )

    titles = [doc["title"] for doc in payload["feed_documents"]]
    assert "Share to LinkedIn" not in titles
    assert "BIS forms" not in titles
    assert "Entity List Update for Advanced Computing" in titles
