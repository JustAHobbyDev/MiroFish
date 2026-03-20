# Historical Archive

This directory holds frozen mixed historical corpora for blind-run experiments.

Subdirectories:

- `manifests/`
- `runs/`
- `raw/`
- `normalized/`
- `logs/`

The first archive contract is defined in:

- [2026-03-20-mixed-historical-archive-manifest-v1.md](/Users/danielschmidt/dev/MiroFish/docs/research-frameworks/2026-03-20-mixed-historical-archive-manifest-v1.md)
- [2026-03-20-capital-flow-archive-collection-methods-v1.md](/Users/danielschmidt/dev/MiroFish/docs/research-frameworks/2026-03-20-capital-flow-archive-collection-methods-v1.md)
- [2026-03-20-capital-flow-event-form-prefilter-v1.md](/Users/danielschmidt/dev/MiroFish/docs/research-frameworks/2026-03-20-capital-flow-event-form-prefilter-v1.md)

Operational note:

- deterministic prefilter `drop` decisions must be logged and audited during
  early runs before the prefilter is trusted as a stable discovery gate
