## AI / Robotics / Lasers Scan v3

This version adds explicit asymmetry inputs for the type of setup the project is actually trying to find:

- ecosystem centrality
- downstream valuation gap
- microcap rerating potential

These sit on top of the existing hiddenness / crowding / valuation-nonlinearity signals.

### Ranked output

1. `MP` -> `shares` (`81.25`)
2. `SIVE` -> `shares` (`78.27`)
3. `HUBB` -> `shares` (`76.59`)
4. `ONTO` -> `shares` (`73.88`)
5. `MU` -> `shares` (`73.46`)
6. `VRT` -> `shares` (`72.49`)
7. `COHR` -> `shares` (`70.18`)
8. `POET` -> `reject` (`58.71`)
9. `FN` -> `reject` (`54.56`)
10. `LITE` -> `reject` (`51.28`)

### What changed

- `SIVE` moved to rank `2`, ahead of `HUBB`.
- `POET` improved again, but still stayed out of the final pick set.
- `LITE` remained rejected, which is desirable if the goal is hidden supplier asymmetry rather than already-recognized AI optics winners.

### Why v3 is better

This run finally rewards the pattern that was missing:

- obscure upstream supplier
- connected to much larger downstream names
- small enough to rerate violently if validated

That makes the output more aligned with the AleaBito-style approach without simply hardcoding specific tickers.

### Current read

- `MP` is still the strongest overall pick because it combines structural importance, public-market accessibility, and real asymmetry.
- `SIVE` now looks like the clearest photonics / laser example of the style we want the engine to catch.
- `POET` is still too messy to graduate into the final pick set under the current rules, which is probably appropriate.

### Remaining gap

The engine still prefers `shares` nearly everywhere. That means the next improvement should not be more candidate scoring alone. It should be a tighter rule for when a name deserves a true `LEAPS` bias rather than a stock bias.
