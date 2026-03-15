# LEAPS Comparison V1

Date: March 15, 2026

## Scope

This is the first side-by-side comparison of the three public delayed LEAPS-style
chain captures gathered for:

- `MP`
- `MU`
- `VRT`

All three snapshots come from Yahoo Finance public delayed options pages and are
normalized into the same JSON schema. The comparison is restricted to the
January 15, 2027 call chain for each name.

## Method

This comparison uses two layers:

1. Chain-level quality:
   - median implied volatility across liquid calls
   - median relative bid/ask spread across liquid calls
   - maximum open interest in the captured expiry
2. Candidate-call selection:
   - use a recent public delayed spot reference only to target an approximately
     `10% OTM` strike
   - then choose the nearest strike with usable spread and at least moderate
     open interest

Reference spots used for strike targeting:

- `MP`: `63.013`
- `MU`: `401.10`
- `VRT`: `243.00`

These are not live spot prices. They are recent public delayed references noted
earlier in the live mispricing memo and used only as strike-selection anchors.

## Selected Candidate Calls

- `MP 2027-01-15 70c`
  - bid `10.55`
  - ask `11.10`
  - open interest `7,947`
  - implied volatility `72.14%`
  - relative spread `5.08%`

- `MU 2027-01-15 440c`
  - bid `106.05`
  - ask `109.10`
  - open interest `892`
  - implied volatility `73.56%`
  - relative spread `2.84%`

- `VRT 2027-01-15 270c`
  - bid `56.55`
  - ask `59.30`
  - open interest `1,040`
  - implied volatility `66.47%`
  - relative spread `4.75%`

## Comparison Read

### Cheapest Volatility

`VRT` looks cheapest on the far-dated call chain.

- Candidate-call IV: `66.47%`
- Chain median IV on liquid calls is lower than `MP` and materially lower than
  `MU`

### Tightest Spreads

`MU` looks best on spread quality.

- Candidate relative spread: `2.84%`
- Nearby 2027 call strikes around the candidate are also tight by public-page
  standards

### Strongest Liquidity At A Plausible OTM Strike

`MP` looks strongest on the combination of thesis alignment and open interest.

- Candidate `70c` sits close to the 10% OTM target
- Open interest is `7,947`
- Nearby strikes like `65c` and `75c` are also liquid

## Practical Ranking

### Chain-Only Ranking

Using only the captured Jan 15, 2027 chain characteristics, the current
mechanical ordering is:

1. `MP`
   Best balance of candidate liquidity and acceptable far-dated volatility.
2. `MU`
   Strongest spread quality and generally cleaner market structure than `VRT`.
3. `VRT`
   Cheapest candidate volatility, but weaker candidate-spread quality than `MU`.

### Thesis-Overlay Read

If the chain data is combined with the earlier structural-thesis work, my
qualitative read is still:

1. `MP`
2. `VRT`
3. `MU`

Reason:

- `MP` still looks like the best intersection of bottleneck thesis and listed
  optionality.
- `VRT` looks cheaper on candidate IV than `MU`, even though `MU` has tighter
  spreads.
- `MU` still looks like the cleanest market, but also the richest far-dated
  optionality of the three.

## Caveats

- This is delayed public data, not executable live pricing.
- The comparison is call-only and does not inspect puts or skew in both wings.
- The candidate selection heuristic uses approximate delayed spot references,
  not captured real-time spot from the same page load.
- Yahoo can omit fields or show stale `last` prints, so bid/ask and OI matter
  more than `last`.

## Next Step

The next useful step is to translate these three candidates into explicit
expression hypotheses and save them as a small watchlist:

- `MP 2027-01-15 70c`
- `VRT 2027-01-15 270c`
- `MU 2027-01-15 440c`

Then track:

- midpoint changes
- IV changes
- thesis milestone updates
