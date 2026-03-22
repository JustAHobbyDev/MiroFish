import pytest

from app.services.businesswire_company_release_collector import (
    BusinessWireAccessDeniedError,
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
