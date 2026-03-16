## AI / Robotics / Lasers Scan v2

This rerun uses a more aggressive scoring posture than v1.

Changes versus v1:

- increased weight on:
  - hiddenness
  - crowding inverse
  - valuation nonlinearity
- reduced the rank advantage from:
  - market accessibility
  - implementation simplicity
- added an explicit asymmetry bonus based on:
  - hiddenness
  - crowding inverse
  - valuation nonlinearity

### Ranked output

1. `MP` -> `shares` (`78.50`)
2. `HUBB` -> `shares` (`75.82`)
3. `SIVE` -> `shares` (`74.26`)
4. `MU` -> `shares` (`72.50`)
5. `ONTO` -> `shares` (`72.49`)
6. `VRT` -> `shares` (`70.68`)
7. `COHR` -> `shares` (`68.34`)
8. `POET` -> `reject` (`55.26`)
9. `FN` -> `reject` (`53.45`)
10. `LITE` -> `reject` (`49.94`)

### What improved

- `SIVE` moved from rank `6` to rank `3`.
- `POET` moved from rank `10` to rank `8`.
- `LITE` stayed low, which is desirable if the goal is hidden asymmetry rather than recognized winners.

### Read

The engine is still conservative, but it is now closer to the intended target.

- `MP` remains the strongest overall combination of structural bottleneck and public-market expression.
- `SIVE` now gets rewarded more like a legitimate asymmetric bottleneck pick instead of a messy small-cap afterthought.
- `HUBB` still ranks very highly because the stock expression is unusually clean and the AI power bottleneck is durable.

### Remaining gap

The model still prefers sturdy equity expressions over the messier small-cap photonics names. That means it is improving, but it is still not behaving like a full AleaBito-style discovery engine.

The next iteration should likely increase sensitivity to:

- ecosystem centrality
- customer quality asymmetry
- rerating potential from tiny current market cap
- hidden supplier importance relative to downstream names
