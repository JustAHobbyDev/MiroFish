# Business Wire PressPass Browser Capture v1

Date: March 22, 2026

## Purpose

Use a user-mediated browser session to turn authenticated `businesswire.com`
PressPass search results into raw `company_release` records.

## Why This Exists

Plain HTTP fetches against Business Wire are blocked in this environment.

PressPass gives us:

1. authenticated search
2. advanced filters
3. a practical way to capture article HTML from a real browser context

## Workflow

1. Run:
   - [capture_businesswire_presspass_playwright.mjs](/Users/danielschmidt/dev/MiroFish/scripts/capture_businesswire_presspass_playwright.mjs)
2. Log in manually and prepare the search/filter view you want.
3. Press Enter in the terminal.
4. The script captures visible Business Wire result links and the corresponding
   article HTML into a timestamped raw archive folder.
5. Convert the capture summary into raw release records with:
   - [build_businesswire_company_release_browser_capture.py](/Users/danielschmidt/dev/MiroFish/scripts/build_businesswire_company_release_browser_capture.py)
6. Feed the resulting records into:
   - [build_company_release_prefilter_batch.py](/Users/danielschmidt/dev/MiroFish/scripts/build_company_release_prefilter_batch.py)

## Boundaries

This path is intentionally narrow:

1. user mediated
2. no MFA automation
3. no attempt to bypass Business Wire controls
4. captures only the visible result set the user prepares

## Components

1. [capture_businesswire_presspass_playwright.mjs](/Users/danielschmidt/dev/MiroFish/scripts/capture_businesswire_presspass_playwright.mjs)
2. [build_businesswire_company_release_browser_capture.py](/Users/danielschmidt/dev/MiroFish/scripts/build_businesswire_company_release_browser_capture.py)
3. [businesswire_company_release_collector.py](/Users/danielschmidt/dev/MiroFish/backend/app/services/businesswire_company_release_collector.py)

## Example

Capture:

```bash
npm run businesswire:capture -- \
  --url "https://www.businesswire.com/portal/site/home/" \
  --maxResults 20
```

Build raw records:

```bash
bash ./scripts/backend-uv.sh run python scripts/build_businesswire_company_release_browser_capture.py \
  research/archive/raw/company_release/businesswire_presspass/2026-03-22T12-00-00-000Z/capture-summary.json \
  --output-json research/archive/raw/company_release/businesswire_presspass_raw_v1.json
```

Build the prefilter batch:

```bash
bash ./scripts/backend-uv.sh run python scripts/build_company_release_prefilter_batch.py \
  research/archive/raw/company_release/businesswire_presspass_raw_v1.json \
  --output-json research/archive/normalized/company_release/businesswire_presspass_prefilter_v1.json
```
