# Historical Signal Calibration Framework v1

Date: March 20, 2026

## Purpose

Define how to calibrate upstream discovery thresholds against historical cases.

The framework exists to answer two different questions for every case:

1. how much relevant signal existed before the move
2. how much relevant signal the system would have surfaced without already
   knowing the answer

This is a calibration framework.
It is not a production pipeline spec.

## Goal

Use historical cases to determine whether our early discovery workflow can:

1. detect enough signal to justify narrowing
2. do so before the bottleneck explosion is obvious in price

The framework is explicitly designed to calibrate:

- `capital_flow_signal_candidate`
- `structural_pressure_candidate`
- promotion thresholds from broad public flow into bounded universes

It is not designed to calibrate:

- final ticker ranking
- option structure selection
- portfolio construction

## Core Principle

Every historical case must be evaluated in two passes:

1. `blind pass`
2. `oracle pass`

Both are mandatory.

If only one pass is run, the case is incomplete.

## Why Two Passes Are Required

### Blind pass

Measures:

- what the system would realistically have surfaced before knowing the final
  answer

This is the anti-hindsight pass.

### Oracle pass

Measures:

- how much relevant public signal actually existed before the move

This is the knowability pass.

### Why both matter

If we use only the oracle pass:

- we overestimate our discovery ability

If we use only the blind pass:

- we cannot tell whether the case was discoverable at all

## Facts

1. Post-hoc relevance labeling is easier than pre-discovery clustering.

2. A strong historical case may have a large amount of relevant signal that
   would not have been obvious without hindsight.

3. The product does not need to recover every relevant signal.

4. The product does need to recover enough signal to justify narrowing into a
   bounded universe.

5. Therefore, the correct success target is:
   - narrowing justification
   - not full bottleneck proof

## Assumptions

1. Historical public evidence can be reconstructed with acceptable fidelity.

2. Relevant signals can be labeled consistently enough to compare cases.

3. Promotion thresholds should be based on historical signal density and role
   coverage, not intuition alone.

## Non-Goals

This framework is not trying to prove:

1. that the system would exactly reproduce AleaBito’s ticker order
2. that every known winner was discoverable
3. that raw signal count alone is sufficient
4. that one case is enough to set global thresholds

## Canonical Evaluation Question

For every historical case, ask:

- did enough pre-move public signal exist, and would our blind clustering have
  surfaced enough of it to justify narrowing into the right research universe?

That is the primary test.

## Case Structure

Every case must define:

1. `case_name`
2. `case_type`
3. `final_expression_or_bottleneck`
4. `pre_move_cutoff_date`
5. `post_cutoff_outcome_window`
6. `allowed public source universe`

Example fields:

```json
{
  "case_name": "Photonics to AXTI",
  "case_type": "upstream_bottleneck_discovery",
  "final_expression_or_bottleneck": "AXTI / InP chokepoint",
  "pre_move_cutoff_date": "2025-12-22",
  "post_cutoff_outcome_window": "2025-12-23 to 2026-03-02",
  "allowed_source_universe": "public information only"
}
```

## Mandatory Passes

## Pass 1: Blind Pass

### Objective

Simulate what the system would have caught before knowing the final bottleneck
or expression.

### Rules

1. no use of final ticker in query design
2. no use of later bottleneck labels
3. no use of post-cutoff evidence
4. no manual clustering around the known answer

### Allowed clustering inputs

The blind pass may cluster only on upstream-neutral features such as:

1. demand drivers
2. system hints
3. architecture shifts
4. stress language
5. visible-beneficiary recurrence
6. repeated entity adjacency

### Blind pass outputs

Each case must produce:

1. surfaced `capital_flow_signal_candidate`s
2. surfaced cluster candidates
3. surfaced `structural_pressure_candidate`s, if any
4. a decision:
   - `not enough to narrow`
   - `enough to narrow`

### Blind pass success standard

Success is:

- enough surfaced signal to justify narrowing into a bounded universe

Success is not:

- full bottleneck proof
- final ticker certainty

## Pass 2: Oracle Pass

### Objective

Measure how much pre-move relevant signal truly existed.

### Rules

1. still obey the same cutoff date
2. use hindsight only for relevance labeling
3. include all pre-cutoff public signals that are materially relevant to the
   eventual bottleneck or expression

### Oracle pass outputs

Each case must produce:

1. the full labeled relevant signal set
2. role labels for each relevant signal
3. earliest date on which a structural pressure candidate would have been
   justifiable in principle

## Signal Role Taxonomy

Every oracle-labeled signal should be assigned one primary role.

### `demand_pressure`

Signals that show rising demand, capex, adoption, or deployment.

### `system_grounding`

Signals that make the affected physical system concrete.

### `visible_beneficiary`

Signals that identify obvious exposed downstream or system-anchor names.

### `stress_hint`

Signals that suggest scarcity, lead-time risk, sold-out capacity, qualification
difficulty, or similar stress.

### `upstream_clue`

Signals that point toward a less-obvious supplier, material, or process layer.

### `bottleneck_verification`

Signals that strongly support concentration, scarcity, or chokepoint status.

This taxonomy is for calibration and analysis.
It is not yet a production ontology requirement.

## Metrics

Every case must record both oracle and blind metrics.

## Oracle Metrics

1. `oracle_observed_signal_count`
2. `oracle_independent_signal_count`
3. `oracle_source_count`
4. `oracle_source_class_count`
5. `oracle_time_bucket_count`
6. `oracle_role_coverage`
7. `oracle_earliest_narrowing_date`

## Blind Metrics

1. `blind_surfaced_signal_count`
2. `blind_independent_signal_count`
3. `blind_source_count`
4. `blind_source_class_count`
5. `blind_time_bucket_count`
6. `blind_role_coverage`
7. `blind_structural_pressure_candidate_formed`
8. `blind_narrowing_justified`

## Derived Comparison Metrics

1. `blind_recall_ratio`
   - `blind_independent_signal_count / oracle_independent_signal_count`

2. `blind_role_coverage_ratio`
   - surfaced oracle roles / total oracle roles

3. `narrowing_gap_days`
   - difference between oracle earliest narrowing date and blind narrowing date

## Independence Rules

Raw counts are not enough.

Every case must distinguish:

1. `observed signal`
   - every captured signal instance

2. `independent signal`
   - deduped by underlying event or materially distinct observation

### Deduping guidance

Treat these as one independent signal:

1. multiple posts paraphrasing the same announcement on the same day
2. multiple headlines summarizing the same company release
3. repeated commentary about the same exact event without new information

Treat these as separate independent signals:

1. distinct company disclosures
2. distinct time-separated observations showing persistence
3. a demand signal and a manufacturing response signal
4. a visible-beneficiary signal and an upstream-clue signal

## Time-Bucket Rules

Each case must define time buckets.

Recommended default:

- `weekly` buckets for multi-month cases

Why:

- daily buckets are often too noisy
- monthly buckets are often too coarse

The exact bucket size should be recorded per case.

## Case Outcome Labels

Each case must finish with one outcome label.

### `blind_fail`

- not enough surfaced signal to justify narrowing

### `blind_partial`

- some relevant signal surfaced, but not enough to justify narrowing cleanly

### `blind_pass`

- enough signal surfaced to justify narrowing into the correct bounded universe

### `oracle_fail`

- too little relevant signal existed even with hindsight

This outcome should be rare.
If it happens, the case may be unsuitable for threshold calibration.

## Success Standard

The primary standard is:

- `blind_pass`

Defined as:

1. a coherent structural-pressure candidate forms in the blind pass
2. the candidate is grounded in a real physical system
3. the candidate has enough role coverage to justify narrowing

Role coverage for narrowing should usually include at least:

1. `demand_pressure`
2. `system_grounding`
3. one of:
   - `visible_beneficiary`
   - `stress_hint`

Upstream-candidate naming is desirable, but not required for a blind pass to
count as successful.

## Calibration Use

Once several cases are labeled with this framework, we can estimate:

1. how many signals usually exist before a valid narrowing point
2. how much role coverage is typically needed
3. how much source diversity matters
4. how far behind the oracle pass the blind pass tends to be

Only then should we set production promotion thresholds.

## Recommended First Cases

Start with:

1. `Photonics -> AXTI`
2. `Memory -> SNDK`
3. one non-AleaBito industrial case

Then add:

4. one failed or mediocre case as a control

## Failure Modes

1. `Oracle inflation`
   - labeling too many signals as relevant after knowing the answer

2. `Blind cheating`
   - letting final ticker or later bottleneck labels influence the blind pass

3. `Count obsession`
   - using raw counts without independence, diversity, or time persistence

4. `Wrong target`
   - demanding full bottleneck proof instead of narrowing justification

## Implementation Guidance

### Build first

1. case template
2. blind-pass rules
3. oracle-pass rules
4. signal-role labeling sheet
5. per-case metric table

### Do not build first

1. global thresholds
2. ranking heuristics
3. production automation

Thresholds should be downstream of calibration.

## Open Questions

1. What should be the default `time_bucket` size for the first three cases?

2. Should one strong filing count as more than one weak investor-post signal in
   the calibration table, or should weighting wait until after the first cases
   are complete?

3. Which non-AleaBito industrial case should be used first as the third case?
