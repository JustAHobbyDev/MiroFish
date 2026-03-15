# Playwright Options Capture POC

Date: March 15, 2026

## Purpose

This is a fallback path for collecting enough options-chain data to test the
mispricing workflow before we commit to a paid market-data API or a broker API
integration.

This path is intentionally narrow:

- research only
- user mediated
- no auto-trading
- no attempt to bypass broker controls
- output is saved as local chain snapshots

## Why This Exists

We need enough repeatable chain data to evaluate the top mispricing candidates:

- `MP`
- `MU`
- `VRT`

The clean long-term solution is a stable API. The fast proof path is a
Playwright-assisted capture workflow that exports visible chain data into a
stable local schema.

## POC Workflow

1. User logs into the broker manually.
2. User opens the options-chain page for one underlying.
3. Playwright reads the visible chain rows or exported table data.
4. Captured rows are saved as CSV or JSON.
5. The normalization script converts the capture to the canonical snapshot
   format.
6. Later analysis compares term structure, skew, spreads, and open interest.

## Canonical Output

Use the normalized snapshot format in:

- [options-chain-snapshot-template.json](/home/d/codex/MiroFish/research/templates/options-chain-snapshot-template.json)

Minimal capture rows can start from:

- [options-chain-capture-rows-template.csv](/home/d/codex/MiroFish/research/templates/options-chain-capture-rows-template.csv)

Normalization is handled by:

- [normalize_options_chain_snapshot.py](/home/d/codex/MiroFish/scripts/normalize_options_chain_snapshot.py)

Example:

```bash
python3 scripts/normalize_options_chain_snapshot.py \
  research/templates/options-chain-capture-rows-template.csv \
  --output-json research/options-data/2026-03-15/MU-chain.json \
  --provider schwab-playwright-manual \
  --source-page https://client.schwab.com/app/trade/options \
  --note "User authenticated manually" \
  --note "POC snapshot from visible chain rows"
```

## Required Fields

Per contract, the POC should capture:

- `option_symbol`
- `underlying`
- `expiry`
- `right`
- `strike`
- `bid`
- `ask`
- `last`
- `mark`
- `volume`
- `open_interest`

Nice to have:

- `implied_volatility`
- `delta`
- `gamma`
- `theta`
- `vega`
- `in_the_money`

Per snapshot:

- capture timestamp
- underlying price
- source page
- provider label
- freeform notes

## Playwright Strategy

The first implementation should prefer stability over automation ambition.

Preferred order:

1. Use broker export/download if available.
2. If no export exists, extract visible HTML table rows.
3. Only capture a small set of expiries per symbol:
   - near dated
   - medium dated
   - long dated

Avoid:

- full-account navigation automation
- MFA automation
- auto-order entry
- hidden or unsupported endpoints

## POC Success Criteria

This fallback is good enough if it lets us:

1. capture `MP`, `MU`, and `VRT` chains on the same day
2. normalize them into one consistent schema
3. compare spreads, open interest, and IV by expiry
4. define one candidate expression per symbol

## Risks

- Broker DOM changes will break capture scripts.
- Manual login/session handling is fragile.
- Some fields may not be visible without extra clicks.
- This should not be treated as a durable production data pipeline.

## Next Step

If Schwab API access fails or is delayed, the next implementation slice should
be:

1. add a small Playwright capture script for one symbol page
2. export rows to CSV
3. normalize with the Python script
4. analyze `MP` first before generalizing
