# Private-Company Diligence Parser v1

## Purpose
- Parse locally collected private-company diligence documents into deterministic evidence snippets.

## Scope
- Current primary use:
  - `CyrusOne`
- Supported file types:
  - `html`
  - `htm`

## Output Objects
- `private_company_diligence_parse_batch`
- `private_company_diligence_evidence_batch`

## Current Evidence Families
- `component_specific`
- `pressure_or_capacity`
- `expansion_or_capex`
- `financing_or_capital`
- `system_context`

## Current Boundary
- This is a lightweight parser.
- It is intended for:
  - official company pages
  - official press releases
  - financing announcements
- It is not yet a full document-cleaning pipeline.
- Repeated site-navigation text may still appear in low-strength snippets.

## Intended Use
- Preserve private-company diligence evidence without forcing private issuers into public filing workflows.
