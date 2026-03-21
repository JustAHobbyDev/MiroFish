# Trade-Press Source Shortlist v1

Date: March 20, 2026

## Purpose

Define the first concrete `trade_press` source shortlist for the current
workflow:

1. detect directional capital movement
2. infer rising-demand structural pressure
3. narrow into affected systems before company-specific deepening

## Facts

1. `company_release` is cleaner than broad government feeds, but it is too
   issuer-local to serve as the main early-discovery source.

2. Broad government feeds contain some valid project/buildout signals, but they
   are noisy enough that they should remain secondary.

3. `trade_press` is the best next source class because it can carry:
   - cross-company demand commentary
   - capacity and buildout updates
   - supplier and bottleneck discussion
   - architecture shifts that change material intensity

## Assumptions

1. The first shortlist should be broad enough to surface cross-system pressure,
   but narrow enough to remain operationally collectible.

2. The first shortlist should prefer publications that frequently report on:
   - construction
   - capacity
   - manufacturing
   - power
   - cooling
   - supply chain
   - semiconductor packaging / photonics

3. We should not optimize for perfect sector coverage in v1.

## Core Shortlist

### 1. Manufacturing Dive

Why:

1. Good fit for plant expansion, supplier reshoring, automation, and production
   buildout.
2. Broad enough to surface signals outside one narrow sector.

Use for:

1. manufacturing expansion
2. industrial automation demand
3. supply-chain restructuring

### 2. Data Center Dynamics

Why:

1. High signal for data-center construction, power, cooling, and capacity
   bottlenecks.
2. Good fit for early AI infrastructure physical-stress detection.

Use for:

1. data-center campus construction
2. power availability
3. cooling buildout
4. colocation and hyperscaler capacity additions

### 3. Utility Dive

Why:

1. Strong fit for grid constraints, transformer demand, interconnection, and
   utility-scale buildout.
2. Useful for pressure zones created by electrification and AI load growth.

Use for:

1. transformer manufacturing
2. transmission buildout
3. grid equipment bottlenecks
4. interconnection constraints

### 4. Semiconductor Engineering

Why:

1. Strong fit for supply-chain depth in semis, packaging, photonics, and
   manufacturing constraints.
2. Better than company releases for cross-layer technical context.

Use for:

1. advanced packaging
2. photonics and optical interconnect
3. process bottlenecks
4. tool and materials dependency

### 5. EE Times

Why:

1. Broad electronics and component coverage with better cross-company context
   than issuer-authored releases.
2. Good complement to Semiconductor Engineering, especially for component and
   subsystem demand signals.

Use for:

1. component supply and demand
2. electronics manufacturing shifts
3. subsystem-level architecture changes

## Holdouts

These are useful, but not first-wave:

### IndustryWeek

Reason:

1. Broad industrial coverage is useful.
2. But it is more mixed between management/operations commentary and hard
   buildout signal than the core shortlist above.

## First Batch Recommendation

Start with a small curated batch from the core shortlist:

1. `Manufacturing Dive`
2. `Data Center Dynamics`
3. `Utility Dive`
4. `Semiconductor Engineering`
5. `EE Times`

The first batch should include a mix of:

1. clear `keep` candidates
2. plausible `review` candidates
3. obvious `drop` items

Reason:

1. we want to test both prefilter precision and extractor behavior
2. we do not want a batch made only of obvious positives

## Non-Goals

This shortlist is not trying to:

1. define the permanent trade-press universe
2. rank publications globally
3. solve committee/testimony sourcing

## Open Questions

1. Which core shortlist source should get the first live collector?
2. Do we need separate prefilter tuning for trade press, or can the current
   deterministic filter stay shared across source classes for now?
