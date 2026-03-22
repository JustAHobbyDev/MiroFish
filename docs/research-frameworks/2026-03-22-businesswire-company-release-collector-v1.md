# Business Wire Company Release Collector v1

Date: March 22, 2026

## Purpose

Bring direct `businesswire.com` article pages into the existing
`company_release` lane.

## Current Boundary

This collector is URL-driven.

Business Wire's newsroom index is access-controlled for plain programmatic
clients in this environment, so v1 does not claim full live newsroom discovery.

What v1 does support:

1. known Business Wire article URLs
2. direct page fetch
3. Business Wire page parsing into raw `company_release` records
4. explicit access-denied detection

## Components

1. [businesswire_company_release_collector.py](/Users/danielschmidt/dev/MiroFish/backend/app/services/businesswire_company_release_collector.py)
2. [fetch_businesswire_company_release_urls.py](/Users/danielschmidt/dev/MiroFish/scripts/fetch_businesswire_company_release_urls.py)

## Next Logical Improvement

If Business Wire changes its access controls or if a browser-backed collection
path is added later, this collector can become the parser/fetch layer beneath a
true discovery layer instead of only a URL-ingestion layer.
