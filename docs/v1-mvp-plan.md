# V1 MVP Plan

Date: March 19, 2026

## Goal

Define a credible v1 MVP for this repository around the actual end state we
care about: moving from thesis or signal to candidate public-market
expression.

This document treats research artifacts as intermediate machinery, not the
product endpoint.

## Product Standard

The v1 MVP is acceptable only if the artifacts produced by the system
materially help achieve the outcomes that sit beyond "research for its own
sake":

- identify hidden bottlenecks or structural dependencies
- validate whether those dependencies imply real market mispricing
- narrow from thesis to candidate company or security
- produce at least one candidate expression worth follow-up

If the system only produces clean research artifacts but does not improve the
path from thesis to expression, it is still pre-MVP.

## Facts

- The repository already has a dedicated research-mode backend and UI.
- The backend can already:
  - create research projects
  - persist thesis intake
  - ingest live Federal Register policy feeds
  - ingest live BIS policy feeds
  - build and persist `source_bundle`
  - build and persist `structural_parse`
  - persist claims audit, scorecards, and summary artifacts
  - score mispricing candidates through a backend endpoint
- The frontend already has a research workbench that supports:
  - project creation
  - thesis intake
  - BIS and Federal Register source fetch
  - automatic structural-parse generation after fetch
  - manual claims, scorecards, and summary editing
- The repository also contains broader simulation surfaces that are not
  required for the research workflow.
- A deterministic `theme_equity_decomposer` service exists in the backend, but
  it is not yet part of the end-user research workflow.
- The current workbench persists scorecards manually, but it does not yet
  produce a polished thesis-to-expression output for the user.

## Assumptions

- "What AleaBito does" means finding hidden structural dislocations and turning
  them into candidate expressions, not just producing nice research memos.
- v1 does not need to automate execution or provide broker integration.
- v1 can still include analyst judgment in the final narrowing step.
- v1 should optimize for one coherent workflow rather than exposing every
  backend capability.

## Not For V1

- full autonomous trade recommendation
- broker connectivity
- portfolio construction
- polished options-chain analytics
- simulation as the primary required user journey
- broad platform parity across every product surface in the repo

These may matter later, but they are not required to prove the core workflow.

## V1 Definition

### User

- a researcher or analyst trying to turn a bottleneck or policy thesis into a
  candidate public-market expression

### Core Job

- go from `thesis or signal` to `candidate expression`

### User Entry Modes

All of these are acceptable starting points for the product from the user's
perspective. They should be developed one by one, not assumed to work equally
well from day one.

Development order:

1. `broad theme`
2. `policy change`
3. `vague intuition`
4. `company already suspected`

These entry modes mean:

1. `broad theme`
   The user starts with a domain such as rare earths, semiconductors, or
   robotics and needs the system to surface bottlenecks, candidate theses, and
   likely expressions.
2. `policy change`
   The user starts from a concrete trigger such as a BIS rule, Federal Register
   notice, tariff, sanction, or subsidy and needs the system to trace
   propagation into bottlenecks and names.
3. `vague intuition`
   The user starts with a weak hunch rather than a formed thesis and needs the
   system to help sharpen, reject, or reframe it using evidence.
4. `company already suspected`
   The user starts from a company they already think matters and needs the
   system to determine whether that company truly sits on the bottleneck or
   value-capture path.

For v1 development sequencing, `broad theme` is the canonical first entry
mode. The remaining three stay in scope as planned follow-on paths.

### Required End-to-End Workflow

1. Create a research project
2. Define the thesis in structured form
3. Ingest evidence from live policy or uploaded sources
4. Build a source bundle
5. Generate structural parse artifacts
6. Map the thesis to candidate companies or securities
7. Produce a short candidate-expression output with rationale
8. Persist the output so it can be reviewed later

### Required Outputs

- thesis intake
- source bundle
- structural parse
- candidate companies or securities
- candidate expression list
- rationale summary

## MVP Thesis

The system is not a research notebook.

The system is a thesis-to-expression discovery workflow whose internal
artifacts happen to include research outputs.

## What Already Exists

### Usable Today

- project creation and persistence
- thesis intake
- live policy ingestion
- source bundle generation
- structural parse generation
- artifact persistence through the research workbench

### Valuable But Not Yet Surfaced Coherently

- deterministic theme-to-equity decomposition
- backend mispricing candidate scoring
- source-acquisition planning
- source-registry generation

### Product Problem

The current user-visible path can stop at:

- claims audit
- scorecards
- summary

without delivering a clean, explicit answer to:

- "What names or expressions should I actually look at next?"

That gap is the core reason the current state is not yet a true v1 MVP for the
stated goal.

## What To Cut

Cut from the v1 success definition:

- simulation-driven narrative outputs as a required deliverable
- options-chain capture
- detailed vol-mispricing analytics
- source-registry and source-acquisition-plan UI
- broad graph exploration features that do not directly improve thesis-to-name
  narrowing
- rebrand execution
- generalized platform messaging

These can remain in the repository, but they should not control the v1
critical path.

## What To Build Next

### P0

1. Surface a thesis-to-company or thesis-to-expression output in the research
   workflow
2. Use existing structured artifacts to produce candidate names deterministically
3. Make the result visible and reviewable in the workbench
4. Preserve the supporting rationale behind each candidate

### P1

1. Add a decomposition or candidate-output tab to the research workbench
2. Integrate `theme_equity_decomposer` into the stored project workflow
3. Show linked process layers, materials, and expression readiness signals
4. Allow the user to promote or reject candidate expressions manually

### P2

1. Expose backend mispricing screening as an optional narrowing layer
2. Add export/download for the final candidate package
3. Improve error handling for empty or weak ingestion results

## Minimum Acceptance Criteria

v1 is achieved only if all of the following are true:

1. A user can create a project from the UI
2. A user can enter a thesis
3. A user can fetch live policy evidence or import equivalent source input
4. The system can generate a structural parse without developer intervention
5. The system can produce a visible list of candidate companies or expressions
6. Each candidate has enough rationale for a user to understand why it appears
7. The project can be reopened later with all artifacts preserved

## Canonical Happy Path

For one domain case, a user should be able to do this end to end:

1. define a bottleneck or policy thesis
2. fetch BIS and/or Federal Register evidence
3. generate `source_bundle`
4. generate `structural_parse`
5. derive candidate companies or expressions
6. save a short final view of the best follow-up ideas

If that path works reliably for one strong case, v1 is defensible.

## Recommended Scope Statement

The strongest honest v1 statement is:

"MiroFish v1 helps an analyst go from bottleneck or policy thesis to a short
list of candidate public-market expressions, backed by structured evidence."

The wrong v1 statement is:

"MiroFish v1 fully automates structural-market discovery and trading."

## Milestones

### Milestone 1: Lock the Product Claim

- declare v1 as thesis-to-expression discovery
- explicitly demote research artifacts to intermediate outputs
- choose one canonical thesis domain
- make `broad theme` the first supported user entry mode

### Milestone 2: Candidate Output

- integrate decomposition into the project workflow
- expose candidate companies or expressions in the UI
- store the output as a persisted artifact

### Milestone 3: Rationale and Review

- show why each candidate appears
- allow analyst review, curation, and summary
- make the final output reusable

### Milestone 4: Demo Proof

- run one fully documented live case
- confirm end-to-end repeatability
- validate that the result is actually useful for follow-up research or
  expression selection

## Proposed Canonical V1 Artifact Chain

1. `thesis_intake`
2. `source_bundle`
3. `structural_parse`
4. `theme_equity_decomposition` or equivalent candidate output
5. curated `summary`

This is the shortest chain in the current repository that can plausibly lead
to AleaBito-style outcome generation.

## Suggested Immediate Implementation Priority

Build a first-class candidate-output step in research mode by connecting
existing structured artifacts to deterministic company or expression
generation.

That is the smallest missing link between:

- "we can do research"

and:

- "we can narrow toward investable follow-up"

## Speculative Ideas

- A `ranked company list with rationale` may be enough for v1 even if explicit
  option structures are deferred to v1.5.
- The cleanest first domain may be policy-heavy themes because live BIS and
  Federal Register ingestion already exists.
- The simulation layer may be better treated as a downstream amplifier rather
  than a v1 requirement.

## Open Questions

1. For v1, is a ranked company list enough, or must the output include explicit
   common-stock or options-expression suggestions?
2. Which first domain should anchor v1:
   - critical materials
   - semiconductors
   - robotics
   - another domain
3. Should candidate generation remain deterministic in v1, or should LLM-based
   reasoning enter the critical path?
4. What is the minimum rationale a candidate must include to be actionable?
