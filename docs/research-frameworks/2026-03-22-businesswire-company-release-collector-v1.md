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

## Browser-Backed Improvement

That browser-backed path now exists for authenticated PressPass use.

See:

- [2026-03-22-businesswire-presspass-browser-capture-v1.md](/Users/danielschmidt/dev/MiroFish/docs/research-frameworks/2026-03-22-businesswire-presspass-browser-capture-v1.md)

The current design is:

1. Playwright captures visible Business Wire results and article HTML from a
   user-authenticated browser session
2. this collector parses the captured article HTML into raw `company_release`
   records
3. the existing company-release prefilter handles triage
