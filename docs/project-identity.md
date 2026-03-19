# Project Identity

Date: March 19, 2026

## Purpose

This document defines the intended identity of this repository as it diverges
from its upstream origin.

The goal is to make product direction explicit before technical and branding
drift become confusing for users or contributors.

## Current Read

### Facts

- The repository originated as a fork of `666ghj/MiroFish`.
- The codebase now includes a research-first workflow centered on:
  - source-bundle ingestion
  - policy-feed connectors
  - structural parsing
  - scorecards and mispricing workflows
  - a dedicated research workbench UI
- Upstream simulation capabilities still exist in the repo.
- Upstream sync remains technically possible and may still provide value.

### Implication

This repository is no longer just an alternative packaging of the upstream
project. It is evolving into a research and policy-intelligence system with its
own workflow and artifact model.

## Identity Statement

This project should be understood as a bottleneck-research and structural
information-arbitrage platform that can ingest live source evidence, transform
it into structured artifacts, and support downstream thesis development,
scoring, and simulation-adjacent analysis.

Upstream lineage is a historical input, not the product identity.

## Target User

- Researcher investigating industrial bottlenecks
- Analyst building structural theses from sparse public evidence
- Operator tracking policy, supply-chain, and process-layer changes

## Primary Workflow

1. Define a thesis
2. Ingest source evidence
3. Build a source bundle
4. Generate structural parse artifacts
5. Audit claims and score candidates
6. Advance into research reporting or simulation-driven follow-up

## What This Project Is Not

- Not only a generic multi-agent simulation demo
- Not only an upstream fork kept current for parity
- Not only a UI wrapper around the original simulation flow

## Divergence Criteria

Treat divergence as official when at least 4 of these 5 are true:

1. The primary user journey is no longer the upstream project's main journey.
2. The core architecture is organized around this repository's research
   workflows rather than upstream defaults.
3. The product can be described clearly without referencing upstream.
4. Most new development value comes from this roadmap, not routine upstream sync.
5. A new contributor would be misled by assuming this repo is "basically upstream."

## Immediate Direction

### Product

- Prioritize research ingestion, evidence structuring, and bottleneck analysis.
- Preserve simulation capabilities where they extend the research workflow.

### Technical

- Continue building explicit research-mode surfaces.
- Avoid forcing new work into upstream-shaped abstractions when they no longer
  fit the product.

### Identity

- Move user-facing messaging toward independent product description.
- Keep attribution to upstream, but stop using upstream as the organizing frame.

## Open Questions

1. What should the final standalone project name be?
2. Should simulation remain a core pillar or become a subordinate capability?
3. At what milestone should visible repo and UI rebranding occur?
4. Which upstream components still justify regular intake?
