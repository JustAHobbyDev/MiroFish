# Structural Pressure Narrowing v1

## Purpose

Deterministically narrow broad structural-pressure lanes into smaller bounded
sub-lanes when the underlying artifact titles support a concrete narrower
equipment or supply-layer story.

## Initial Use

The first target is:

1. `power generation and backup equipment`

## Current Narrowing Rule

Create a narrower candidate only when at least two supporting artifacts point
to a common backup-power equipment manufacturing lane such as:

1. generator packages
2. generator modules
3. large engines for backup power
4. power enclosures for generator systems

## Provenance Guard

The narrowed lane must be supported by `real_only` artifact provenance.
Synthetic-only support does not qualify the lane for downstream work.

## Boundary

This step does not make the narrowed lane promotion-ready.
It only makes it bounded enough for exploratory downstream work.
