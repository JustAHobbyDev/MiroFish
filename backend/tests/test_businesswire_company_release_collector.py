import pytest
from pathlib import Path

from app.services.businesswire_company_release_collector import (
    BusinessWireAccessDeniedError,
    build_businesswire_browser_capture_records,
    fetch_businesswire_company_release_records,
    parse_businesswire_article_html,
)


def test_parse_businesswire_article_html_extracts_release_fields() -> None:
    html = """
    <html>
      <head>
        <link rel="canonical" href="https://www.businesswire.com/news/home/example/en/test-release" />
        <meta property="og:title" content="Mitsubishi Electric Invests in Elephantech" />
        <meta property="article:published_time" content="2026-03-22T10:00:00Z" />
        <meta name="keywords" content="Investment, Electronics, Manufacturing" />
        <script type="application/ld+json">
        {
          "@context": "https://schema.org",
          "@type": "NewsArticle",
          "headline": "Mitsubishi Electric Invests in Elephantech",
          "datePublished": "2026-03-22T10:00:00Z",
          "articleBody": "TOKYO--(BUSINESS WIRE)--Mitsubishi Electric Corporation announced a strategic investment in Elephantech."
        }
        </script>
      </head>
      <body>
        <h1>Mitsubishi Electric Invests in Elephantech</h1>
      </body>
    </html>
    """

    record = parse_businesswire_article_html(
        html,
        source_url="https://www.businesswire.com/news/home/example/en/test-release",
    )

    assert record["publisher"] == "Business Wire"
    assert record["issuer_name"] == "Mitsubishi Electric"
    assert record["published_at"] == "2026-03-22T10:00:00Z"
    assert record["title"] == "Mitsubishi Electric Invests in Elephantech"
    assert "strategic investment" in record["body"]
    assert record["categories"] == ["Investment", "Electronics", "Manufacturing"]


def test_parse_businesswire_article_html_raises_on_access_denied() -> None:
    with pytest.raises(BusinessWireAccessDeniedError):
        parse_businesswire_article_html(
            "<html><title>Access Denied</title><body>Access Denied</body></html>",
            source_url="https://www.businesswire.com/news/home/example/en/test-release",
        )


def test_fetch_businesswire_company_release_records_uses_injected_fetcher() -> None:
    records = fetch_businesswire_company_release_records(
        [
            "https://www.businesswire.com/news/home/example/en/one",
            "https://www.businesswire.com/news/home/example/en/two",
        ],
        fetcher=lambda url: {
            "source_url": url,
            "publisher": "Business Wire",
            "issuer_name": "Example Co",
            "published_at": "2026-03-22T00:00:00Z",
            "title": "Example release",
            "headline": "Example release",
            "categories": [],
            "body": "Body",
        },
    )

    assert len(records) == 2
    assert records[0]["source_url"].endswith("/one")
    assert records[1]["source_url"].endswith("/two")


def test_build_businesswire_browser_capture_records_reads_relative_article_paths(
    tmp_path: Path,
) -> None:
    article_path = tmp_path / "articles" / "mitsu.html"
    article_path.parent.mkdir(parents=True, exist_ok=True)
    article_path.write_text(
        """
        <html>
          <head>
            <meta property="og:title" content="Mitsubishi Electric Invests in Elephantech" />
            <meta property="article:published_time" content="2026-03-22T10:00:00Z" />
          </head>
          <body>
            <h1>Mitsubishi Electric Invests in Elephantech</h1>
            <article>
              <p>TOKYO--(BUSINESS WIRE)--Mitsubishi Electric Corporation announced a strategic investment in Elephantech.</p>
            </article>
          </body>
        </html>
        """,
        encoding="utf-8",
    )

    records = build_businesswire_browser_capture_records(
        {
            "results": [
                {
                    "capture_status": "captured",
                    "result_index": 0,
                    "title": "Mitsubishi Electric Invests in Elephantech",
                    "url": "https://www.businesswire.com/news/home/example/en/test-release",
                    "article_final_url": "https://www.businesswire.com/news/home/example/en/test-release",
                    "article_path": "articles/mitsu.html",
                    "published_label": "2026-03-22T10:00:00Z",
                    "teaser": "Strategic investment in Elephantech.",
                }
            ]
        },
        capture_root=tmp_path,
    )

    assert len(records) == 1
    assert records[0]["publisher"] == "Business Wire"
    assert records[0]["title"] == "Mitsubishi Electric Invests in Elephantech"
    assert records[0]["summary"] == "Strategic investment in Elephantech."


def test_build_businesswire_browser_capture_records_skips_failed_results() -> None:
    records = build_businesswire_browser_capture_records(
        {
            "results": [
                {
                    "capture_status": "capture_failed",
                    "url": "https://www.businesswire.com/news/home/example/en/test-release",
                    "article_html": "<html></html>",
                }
            ]
        }
    )

    assert records == []


def test_build_businesswire_browser_capture_records_accepts_inline_article_html() -> None:
    records = build_businesswire_browser_capture_records(
        {
            "results": [
                {
                    "capture_status": "captured",
                    "url": "https://www.businesswire.com/news/home/example/en/test-release",
                    "article_final_url": "https://www.businesswire.com/news/home/example/en/test-release",
                    "published_label": "2026-03-22T10:00:00Z",
                    "article_html": """
                        <html>
                          <head>
                            <meta property=\"og:title\" content=\"Mitsubishi Electric Invests in Elephantech\" />
                          </head>
                          <body>
                            <article>
                              <p>TOKYO--(BUSINESS WIRE)--Mitsubishi Electric Corporation announced a strategic investment in Elephantech.</p>
                            </article>
                          </body>
                        </html>
                    """,
                }
            ]
        }
    )

    assert len(records) == 1
    assert "Elephantech" in records[0]["title"]
