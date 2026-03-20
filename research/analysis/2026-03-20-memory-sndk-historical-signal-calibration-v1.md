# Memory -> SNDK Historical Signal Calibration v1

Date: March 20, 2026

## Purpose

Apply the two-pass calibration framework to the second benchmark case:

- `Memory -> SNDK`

This is the second worked example.

It is based on:

- the reconstructed AleaBito archive
- the existing replay notes
- pre-cutoff public non-X evidence already collected in the repo

It is not yet a fully automated measurement pipeline.

## Case Definition

### Case Name

- `Memory -> SNDK`

### Case Type

- `cycle_expression_selection`

### Final Expression Or Bottleneck

- `memory supercycle -> SNDK`

### Pre-Move Cutoff Date

- `2026-01-21`

### Post-Cutoff Outcome Window

- `2026-01-22` to `2026-02-02`

### Allowed Public Source Universe

- public information only

### Time Bucket Rule

- `weekly`

## Facts

1. By `2026-01-21`, the archive already showed:
   - repeated memory-cycle discussion
   - anchor names like `MU`, `SK Hynix`, and `Samsung`
   - a weaker but real `SNDK` presence

2. By `2026-01-21`, the archive had explicit `memory supercycle` language, but
   the strongest `SNDK`-specific explanation still lay ahead.

3. Pre-cutoff non-X public evidence already showed:
   - AI-driven HBM and packaging expansion
   - AI-memory-driven record results
   - forward supply tightness
   - Sandisk / Kioxia expansion tied to AI-driven flash demand

## Assumptions

1. Weekly buckets are the right compromise for this multi-month case.

2. For this worked example, the blind pass is intentionally strict and is based
   on archive-visible, upstream-neutral clues rather than broad-web crawling.

3. The oracle pass below should still be treated as a lower bound rather than a
   complete census of all pre-cutoff relevant public evidence.

## Blind Pass

### Objective

- determine whether the system would have surfaced enough signal to justify narrowing into a memory universe without already knowing `SNDK`

### Blind Rules Used

1. no use of `SNDK` as clustering seed
2. no use of post-`2026-01-21` evidence
3. no use of later supply-chain maps or later `SNDK` profitability framing
4. clustering allowed only on demand cues, cycle anchors, memory-system hints,
   and stress language

### Allowed Clustering Inputs

1. repeated `MU`, `SK Hynix`, and `Samsung` recurrence
2. memory and AI-infrastructure references
3. HBM / DRAM / NAND system references
4. forward-demand and supply-commitment language

### Surfaced Signals

1. `2025-10-04`: first serious valuation-driven attention to `MU`
2. `2025-11-04`: memory becomes a tracked sector bucket
3. `2025-12-05`: `Samsung` and `SK Hynix` appear in the AI portfolio
4. `2025-12-14`: first visible `SNDK` awareness
5. `2026-01-07`: `SNDK` enters as an owned expression alongside `MU`
6. `2026-01-21`: explicit `memory supercycle` language appears through `MU`

### Blind Role Coverage

Present in blind pass:

- `demand_pressure`
- `system_grounding`
- `visible_beneficiary`
- `stress_hint`

Partially present in blind pass:

- `upstream_clue`

Not present in blind pass:

- `bottleneck_verification`

### Blind Judgment

- `blind_pass`

### Why

1. The blind pass clearly surfaces a coherent `AI memory` pressure zone.

2. The blind pass provides enough role coverage to justify narrowing:
   - demand pressure is visible
   - the system can be named concretely
   - visible cycle anchors recur
   - stress is implied through supercycle framing and committed supply language

3. Unlike photonics, the blind pass does not need to find a hidden upstream
   clue in order to justify narrowing. The primary narrowing object is the cycle
   itself.

4. `SNDK` is visible in the blind pass, but not strongly enough to count as a
   fully validated preferred expression.

## Oracle Pass

### Objective

- determine how much relevant pre-move signal actually existed before the later `SNDK`-specific acceleration

### Oracle Rules Used

1. same cutoff date: `2026-01-21`
2. hindsight allowed only for relevance labeling
3. all pre-cutoff public signals materially relevant to the eventual memory-cycle / `SNDK` thesis are included

### Oracle Relevant Signals

Archive-visible signals:

1. initial `MU` valuation attention
2. memory becomes a tracked bucket
3. `Samsung` and `SK Hynix` become anchor memory names in the AI portfolio
4. first `SNDK` awareness
5. `SNDK` enters as an owned expression with `MU`
6. explicit `memory supercycle` labeling

Pre-cutoff non-X public signals:

7. Micron HBM packaging expansion tied directly to AI demand
8. Micron HBM4 samples shipped to major customers
9. SK hynix reported AI-memory-driven record results
10. SK hynix prepared HBM4 mass production
11. SK hynix said next-year HBM supply was effectively spoken for
12. Sandisk / Kioxia expanded flash capacity to meet AI-driven demand
13. Sandisk positioned flash as critical AI infrastructure

### Oracle Role Coverage

Present in oracle pass:

- `demand_pressure`
- `system_grounding`
- `visible_beneficiary`
- `stress_hint`
- `upstream_clue`
- `bottleneck_verification`

### Earliest Oracle Narrowing Date

- `2025-11-04`

Reason:

- by then memory had already become a concrete monitored sector
- the system was no longer generic `AI`; it was a distinct memory universe
- the bounded universe becomes materially stronger by `2025-12-05`
- it is compelling by `2026-01-21`

## Metrics

### Blind Metrics

- `blind_surfaced_signal_count`: `6`
- `blind_independent_signal_count`: `6`
- `blind_source_count`: `1`
- `blind_source_class_count`: `1`
- `blind_time_bucket_count`: `6`
- `blind_role_coverage`: `4.5 / 6`
- `blind_structural_pressure_candidate_formed`: `true`
- `blind_narrowing_justified`: `true`

### Oracle Metrics

- `oracle_observed_signal_count`: `13`
- `oracle_independent_signal_count`: `13`
- `oracle_source_count`: `7`
- `oracle_source_class_count`: `4`
- `oracle_time_bucket_count`: `7`
- `oracle_role_coverage`: `6 / 6`
- `oracle_earliest_narrowing_date`: `2025-11-04`

### Derived Comparison Metrics

- `blind_recall_ratio`: `0.46`
- `blind_role_coverage_ratio`: `0.75`
- `narrowing_gap_days`: `0`

## Calibration Judgment

### What This Case Says

1. A valid narrowing decision can happen through cycle recognition even before a
   standout sub-expression is obvious.

2. The blind pass again recovers less than half of oracle-independent signals,
   but still justifies narrowing.

3. `visible_beneficiary` / anchor coverage mattered heavily here:
   - `MU`
   - `SK Hynix`
   - `Samsung`
   created the memory universe before `SNDK` became well-explained.

4. This case differs from photonics:
   - photonics narrowed through a visible-beneficiary-to-upstream path
   - memory narrowed through cycle recognition first, then expression selection

### Threshold Implication

1. Promotion into a structural pressure candidate should not require an
   upstream clue in every case.

2. Role coverage still appears more important than raw count.

3. For cycle-selection cases, the minimum viable role set may be:
   - demand pressure
   - system grounding
   - visible beneficiary
   - stress hint

4. `upstream_clue` may be optional for narrowing in some cases, even if it is
   common in upstream bottleneck discovery cases.

### Caveats

1. The blind pass here is again based on one reconstructed archive source, so
   source diversity is artificially low.

2. The oracle pass is a lower bound because it includes only the pre-cutoff
   public evidence already reconstructed in the repo.

3. This case is a different subtype from photonics, so it helps compare
   patterns but still does not justify hard production thresholds on its own.

## Open Questions

1. Does a control case show similar anchor-heavy role coverage without
   deserving narrowing?

2. Should the calibration framework split success patterns into:
   - `upstream_bottleneck_discovery`
   - `cycle_expression_selection`

3. Should `upstream_clue` be mandatory only for the former, not the latter?
