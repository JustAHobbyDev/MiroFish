# Mixed Company Filing Parse V1 Assessment

## Facts
1. `2` Hitachi parent-route filings were parsed from the local archive:
   - `Annual Securities Report FY2025`
   - `Semi-annual Securities Report FY2026`
2. Both documents parsed successfully.

## Strong Evidence
1. FY2025 annual filing:
   - page `64` references steady growth in:
     - `power distribution transformers`
     - `power receiving and transforming equipment`
2. FY2025 annual filing:
   - page `63` states revenues increased due to:
     - `steady conversion of the order backlog into sales`
     - `expanded production capacity at Hitachi Energy`
3. FY2025 annual filing:
   - page `29` links demand growth to:
     - expansion of clean energy
     - development of power grids
     - expansion of microgrids
4. FY2026 semi-annual filing:
   - page `8` again attributes growth in part to:
     - `steady conversion of order backlog into sales in Hitachi Energy Ltd`

## Interpretation
This is useful bounded-lane evidence because it is no longer only external trade-press or release coverage.
The filing layer now supports:
1. transformer-related demand language
2. backlog conversion language
3. production-capacity expansion language
4. explicit power-grid development language

## Limitation
The current deterministic parser extracts keyword-driven snippets.
It is good enough for first-pass evidence surfacing, but analyst review is still needed to select the strongest excerpts.
