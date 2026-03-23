# MiroFish vNext Reset Triage v1

Date: March 22, 2026

## Purpose

Define what belongs in the active vNext proof path versus what should be treated
as legacy, archive, or experimental.

## Active Core

Keep in the active core only if a module directly supports one of:

1. real clue capture
2. graph construction
3. node scoring
4. benchmark evaluation

## Legacy Or Archive

Treat as legacy or archive if a module primarily supports:

1. synthetic-era discovery claims
2. lane taxonomy expansion
3. downstream review surface formatting
4. execution or policy handoff formatting
5. benchmark narratives that are not tied to real corpus quality

## Immediate Practical Rule

A new vNext module must answer one question:

- does this increase the chance that we find the right graph node earlier from
  real evidence?

If the answer is not clearly yes, it does not belong in the active core.

## Recommended Repo Boundary

### `vnext/`

Use this for:

1. clean proof-path code
2. minimal docs
3. benchmark-facing experiments

### existing repo root

Treat the existing pipeline as:

1. reference material
2. archive of ideas
3. source of reusable utilities

Not:

1. the default place to extend blindly

## Triage Labels

Use these labels for future cleanup:

1. `active_core`
2. `reusable_utility`
3. `archive_only`
4. `delete_candidate`

## Assumptions

1. A smaller trusted core is more useful than a larger ambiguous system.
2. Some current modules may still be reusable after extraction.
3. Cleanup can be incremental once the vNext boundary exists.

## Open Questions

1. Which current collectors are worth porting into `vnext/` first?
2. Which current scoring logic is still worth preserving?
3. When should the vNext seed become its own repository?
