# Upstream Intake Policy

Date: March 19, 2026

## Policy

This repository should treat upstream as a selective input source, not a
default synchronization target.

## Decision Rule

Upstream changes are adopted only when they clearly improve this project's
stability, security, or leverage without distorting its product direction.

## Accept By Default

- Security fixes
- Clear bug fixes in shared infrastructure
- Low-risk utility improvements
- Dependency or environment fixes that reduce maintenance burden

## Review Carefully

- Changes that alter core workflows
- Major UI or routing changes
- Architecture refactors that assume upstream product priorities
- Naming and branding changes
- Behavior changes in simulation layers that affect research-mode assumptions

## Reject By Default

- Changes that pull this repository back toward upstream product identity
- Broad merges performed only for parity
- Refactors that increase coupling to upstream concepts without product value

## Preferred Integration Method

Use the narrowest mechanism that captures the desired value:

1. cherry-pick isolated fixes
2. manually port small changes
3. merge only when the affected surface is still materially shared

## Operational Guidance

- Keep the `upstream` remote configured while it remains useful.
- Do not treat `npm run sync:upstream` as a routine maintenance obligation.
- Record notable upstream intake decisions in commit messages or docs when the
  rationale is not obvious.

## Trigger To Revisit This Policy

Revisit when:

- upstream still provides high leverage in core modules, or
- divergence becomes large enough that keeping `upstream` configured no longer
  adds practical value
