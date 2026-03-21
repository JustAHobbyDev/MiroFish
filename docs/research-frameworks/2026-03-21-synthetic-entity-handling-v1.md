# Synthetic Entity Handling v1

Date: March 21, 2026

## Purpose

Prevent synthetic placeholder artifacts from leaking into live downstream queues.

## Facts

1. Some `company_release` fixture corpora use synthetic `example.com` artifacts.
2. Those fixtures remain useful for offline testing.
3. They must not drive:
   - live issuer resolution
   - live filing expansion
   - real company queues

## Rule

Any artifact whose `source_url` resolves to `example.com` should be treated as:

1. `synthetic_example`

Any downstream entity or family supported only by synthetic-example artifacts should
be treated as:

1. `synthetic_only`

And should be excluded from:

1. bounded entity expansion
2. company filing expansion
3. issuer-resolution planning

## Decision

1. Keep synthetic artifacts as offline fixtures where needed.
2. Segregate them explicitly in provenance fields.
3. Exclude synthetic-only downstream candidates from live workflows.

