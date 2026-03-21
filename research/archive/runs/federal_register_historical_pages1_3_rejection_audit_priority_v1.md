# Priority Rejection Audit Set

- Source audit set: `federal_register_historical_pages1_3_rejection_audit_v1.json`
- Priority item count: `6`

## Review Labels

- `correct_rejection`
- `borderline_should_review`
- `false_negative`

## Items

- [HEURISTIC] 2026-02-27 | openai / gpt-4o-mini | Prospective Grant of an Exclusive Patent License: Powered Gait Assistance Systems and Gait Assistance Systems and Methods of Control Thereof
  Label: `correct_rejection`
  Reason: exclusive patent license notice without concrete buildout; outside the current rising-demand structural-pressure workflow.
- [KEYWORD] 2026-02-25 | openai / gpt-4o-mini | Agency Information Collection Activities; Comment Request; Report of Construction Contractor's Wage Rates
  Label: `correct_rejection`
  Reason: paperwork extension only; “construction” is part of the form title, not evidence of current capital deployment.
- [KEYWORD] 2026-02-25 | groq / openai/gpt-oss-20b | Agency Information Collection Activities; Comment Request; Report of Construction Contractor's Wage Rates
  Label: `correct_rejection`
  Reason: paperwork extension only; no rising-demand or physical-buildout signal.
- [KEYWORD] 2026-02-26 | groq / openai/gpt-oss-20b | Clean Air Act Operating Permit Program; Order on Petition for Objection to State Operating Permit for Platteville Natural Gas Processing Plant
  Label: `correct_rejection`
  Reason: permit continuity may matter operationally, but this notice does not itself indicate planned capital deployment or new buildout.
- [KEYWORD] 2026-02-27 | openai / gpt-4o-mini | Prospective Grant of an Exclusive Patent License: In Vivo Manufactured Anti-CD19 Chimeric Antigen Receptor (CAR) Products for the Treatment or Prevention of B Cell Mediated Autoimmune Diseases; Correction
  Label: `correct_rejection`
  Reason: correction notice only; no new capital-flow or buildout evidence.
- [KEYWORD] 2026-02-27 | groq / openai/gpt-oss-20b | Prospective Grant of an Exclusive Patent License: Powered Gait Assistance Systems and Gait Assistance Systems and Methods of Control Thereof
  Label: `correct_rejection`
  Reason: exclusive patent license notice without concrete buildout; outside the current rising-demand structural-pressure workflow.
