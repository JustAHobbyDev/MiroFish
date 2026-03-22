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

Preferred path:

1. Use your normal logged-in browser session.
2. Open the PressPass results page you want.
3. Run:
   - [businesswire_presspass_console_capture.js](/Users/danielschmidt/dev/MiroFish/scripts/businesswire_presspass_console_capture.js)
   in the browser console.
4. The script downloads a JSON payload containing visible result metadata and
   fetched article HTML from the authenticated browser session.
5. Convert the capture JSON into raw release records with:
   - [build_businesswire_company_release_browser_capture.py](/Users/danielschmidt/dev/MiroFish/scripts/build_businesswire_company_release_browser_capture.py)
6. Feed the resulting records into:
   - [build_company_release_prefilter_batch.py](/Users/danielschmidt/dev/MiroFish/scripts/build_company_release_prefilter_batch.py)

Fallback path:

1. Run:
   - [capture_businesswire_presspass_playwright.mjs](/Users/danielschmidt/dev/MiroFish/scripts/capture_businesswire_presspass_playwright.mjs)
2. Log in manually and prepare the search/filter view you want.
3. Press Enter in the terminal.
4. The script captures visible Business Wire result links and the corresponding
   article HTML into a timestamped raw archive folder.

## Boundaries

This path is intentionally narrow:

1. user mediated
2. no MFA automation
3. no attempt to bypass Business Wire controls
4. captures only the visible result set the user prepares

## Current OAuth Boundary

Business Wire's OAuth flow is currently failing in Playwright-launched browser
sessions from this environment with `ERR_HTTP2_PROTOCOL_ERROR`.

So the preferred path is now:

1. run capture inside the user's normal browser session
2. keep Playwright only as a secondary fallback

## Components

1. [capture_businesswire_presspass_playwright.mjs](/Users/danielschmidt/dev/MiroFish/scripts/capture_businesswire_presspass_playwright.mjs)
2. [businesswire_presspass_console_capture.js](/Users/danielschmidt/dev/MiroFish/scripts/businesswire_presspass_console_capture.js)
3. [build_businesswire_company_release_browser_capture.py](/Users/danielschmidt/dev/MiroFish/scripts/build_businesswire_company_release_browser_capture.py)
4. [businesswire_company_release_collector.py](/Users/danielschmidt/dev/MiroFish/backend/app/services/businesswire_company_release_collector.py)

## Example

Console capture:

1. Open DevTools on the PressPass results page
2. Paste the contents of:
   - [businesswire_presspass_console_capture.js](/Users/danielschmidt/dev/MiroFish/scripts/businesswire_presspass_console_capture.js)
3. Let it download a JSON file

Playwright capture:

```bash
npm run businesswire:capture -- \
  --url "https://www.businesswire.com/portal/site/home/" \
  --maxResults 20
```

Build raw records:

```bash
bash ./scripts/backend-uv.sh run python scripts/build_businesswire_company_release_browser_capture.py \
  ~/Downloads/businesswire-presspass-capture-2026-03-22T12-00-00-000Z.json \
  --output-json research/archive/raw/company_release/businesswire_presspass_raw_v1.json
```

Build the prefilter batch:

```bash
bash ./scripts/backend-uv.sh run python scripts/build_company_release_prefilter_batch.py \
  research/archive/raw/company_release/businesswire_presspass_raw_v1.json \
  --output-json research/archive/normalized/company_release/businesswire_presspass_prefilter_v1.json
```
