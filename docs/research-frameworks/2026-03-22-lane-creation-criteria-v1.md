# Lane Creation Criteria v1

Purpose:
- decide when a new lane should be created
- keep lane formation recursive but bounded
- prevent taxonomy growth that does not improve capital-flow or supply-chain tracking

## Core Principle

Create a new lane only when doing so improves the ability to:
1. track capital flow
2. track supply chains affected by that capital flow
3. produce cleaner downstream research targets

If a proposed lane does not improve those three things, it should not exist.

## Facts

Every new lane adds cost:
1. more rules
2. more audits
3. more routing logic
4. more maintenance

So the default should be:
- do not create a new lane

A lane must earn its existence.

## Recursive Decision Rule

Given a current lane `L`:

1. Ask whether `L` is too broad for downstream work.
2. If `no`, stop.
3. If `yes`, inspect the current real artifact/entity support inside `L`.
4. Ask whether a tighter sub-pattern `L'` already exists in the current corpus.
5. If `no`, stop and keep using `L`.
6. If `yes`, ask whether `L'` improves downstream decisions materially.
7. If `no`, stop and keep using `L`.
8. If `yes`, create `L'` and allow the same test to be applied again later.

This is recursive, but only on real observed sub-patterns.

## Base Case

The recursion stops when any of these becomes true:

1. The current lane is already bounded enough for downstream use.
2. No tighter real-only sub-pattern exists in the current corpus.
3. A tighter split would not change:
   - entity queues
   - support routing
   - review ranking
   - or supply-chain interpretation
4. The remaining difference is wording-level noise, not a real economic distinction.
5. The proposed child lane would have too little real support to stand on its own.

That is the base case:
- no further narrowing produces a better downstream object

## Required Conditions For A New Lane

All of these must be true:

1. Parent-lane problem exists
- the parent lane mixes materially different concepts

2. Real sub-pattern exists now
- supported by current real artifacts
- not hypothetical
- not dependent on future collection

3. Narrower meaning is cleaner
- more specific economic mechanism
- more specific capital-flow interpretation
- more specific supply-chain implications

4. Real-only support
- synthetic-only support cannot justify lane creation

5. Downstream consequence exists
- the new lane changes at least one of:
  - entity queue
  - public/private route mix
  - evidence support path
  - review-surface ranking
  - bounded market handoff later

6. Naming is stable
- the lane can be named clearly enough that future artifacts can be tested against it

## Do Not Create A Lane When

Any of these is true:

1. One interesting artifact exists, but no repeated pattern does
2. The difference is conceptual but not operational
3. The proposed lane would just duplicate the parent lane
4. The proposed lane is too broad to improve downstream routing
5. The proposed lane is too narrow to matter
6. The proposal is driven by ontology neatness rather than research usefulness

## Practical Heuristic

A proposed lane is usually worth creating if it does all of the following:

1. removes real ambiguity from the parent lane
2. preserves a coherent real-only artifact set
3. yields a cleaner follow-up queue
4. yields cleaner public/private support routing
5. improves review-surface usefulness without requiring immediate new collection

If it misses any of those, default to keeping the parent lane.

## Examples

### Lane Creation Was Justified

1. `power generation and backup equipment pressure`
-> `data center backup-power equipment buildout`

Why:
- recurring real pattern
- clearer equipment/supplier queue
- cleaner public/private split

2. `utility and large-load power buildout`
-> `data center utility response buildout`

Why:
- repeated explicit data-center-linked utility response artifacts
- cleaner operator/private mix
- better downstream review surface

### Lane Creation Was Not Justified

1. Pulling `Southern` into `data center utility response buildout`

Why not:
- real capital-flow implication exists
- but the artifact is broader than the narrowed lane definition
- better handled in parent lane unless a separate broader child lane is later justified

## Current Policy

1. New lanes should be formed from current evidence, not anticipated evidence.
2. Lane creation should usually happen before widening source collection.
3. Once a new lane exists, it should immediately reuse existing downstream machinery:
   - support attachment
   - priority scoring
   - review surfaces
4. If the new lane cannot reuse downstream machinery cleanly, it is probably not ready.

## Quantitative Thresholds

Not required in `v1`.

Reason:
- current corpus is still evolving
- hard thresholds would be premature

Possible future additions:
1. minimum real-only artifact count
2. minimum distinct entity count
3. minimum route divergence from parent lane
4. minimum downstream ranking change

These are deferred until they become clearly useful.

## Open Questions

1. Should future versions require a minimum count of:
   - real-only artifacts
   - distinct entities
   before a lane can be created?
2. Should lane creation later require a demonstrated change in:
   - public/private route mix
   - or bounded market handoff behavior?
