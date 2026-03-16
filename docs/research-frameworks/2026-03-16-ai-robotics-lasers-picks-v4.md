## AI / Robotics / Lasers Scan v4

This version adds a dedicated `LEAPS bias` layer. That is separate from generic `options_fit`.

Why this matters:

- `options_fit` only says whether options are sensible in principle.
- `LEAPS bias` says whether long-dated calls are attractive enough to beat the stock as the default expression.

The current LEAPS-bias inputs are:

- iv cheapness
- surface staleness
- pre-expiration repricing potential
- stock-vs-call convexity advantage
- long-dated liquidity quality

### Ranked output

1. `MP` -> `leaps_call` (`77.34`)
2. `SIVE` -> `shares` (`73.73`)
3. `HUBB` -> `shares` (`71.81`)
4. `ONTO` -> `shares` (`69.33`)
5. `MU` -> `shares` (`68.87`)
6. `VRT` -> `shares` (`68.01`)
7. `COHR` -> `shares` (`65.90`)
8. `POET` -> `reject` (`54.73`)
9. `FN` -> `reject` (`50.54`)
10. `LITE` -> `reject` (`47.44`)

### Why this is better

This is the first batch that separates:

- strong bottleneck equity
- from a true long-dated optionality candidate

`MP` now flips to `leaps_call` because the engine finally recognizes:

- the options fit is already high
- the LEAPS bias is very high
- the pre-expiration resale/repricing path is materially better than for the other scanned names

At the same time:

- `MU` stays `shares`
- `VRT` stays `shares`
- `SIVE` stays `shares`

That is the correct behavior under the current evidence set.

### Main takeaway

The missing piece was not more bottleneck scoring. It was a dedicated layer for:

- cheapness of long-dated optionality
- likelihood of pre-expiration repricing
- whether the call actually beats simply owning the stock

This does not solve options evaluation completely, but it is the first version that produces a mixed expression set instead of defaulting almost everything to stock.
