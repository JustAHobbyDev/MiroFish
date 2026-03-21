# LLM No-Candidate Audit

- Source audit set: `federal_register_historical_pages1_3_rejection_audit_v1`
- Source batch: `federal_register_historical_pages1_3_prefilter_v1`
- Reviewed scope: `29` LLM no-candidate items
- Unique artifacts reviewed: `17`

## Summary

- `correct_rejection`: `17`
- `borderline_should_review`: `0`
- `false_negative`: `0`

Overall judgment:
All unique LLM no-candidate artifacts were valid rejections for the current `rising-demand structural-pressure` workflow.

## Important Scope Boundary

These labels are only for the current workflow:

- detect directional capital movement
- infer rising-demand structural pressure
- defer constrained-access and exclusivity workflows

Some artifacts could still matter later as:

- policy context
- system background
- constrained-access signals

They still remain correct rejections for this stage.

## Notable Edge Cases

- `policy_feed_4b2e13b06c9906f8`
  - TVA / NEPA categorical exclusions order
  - kept rejected because it is policy-enabling context, not evidence of current or planned demand-led capital deployment in the artifact itself
- `policy_feed_d3426979d9550bb1`
  - FERC inverter-based resource modeling reliability standards
  - kept rejected because it is standards context, not a direct capital-flow signal

## Reviewed Artifacts

1. `policy_feed_4b2e13b06c9906f8`
   - Label: `correct_rejection`
   - Note: Policy-enabling notice that may reduce future review friction, but the artifact itself does not evidence current or planned demand-led capital deployment or physical buildout.
2. `policy_feed_6d6ba56a42dfcd82`
   - Label: `correct_rejection`
   - Note: Paperwork and benefits administration notice with no plausible directional capital-flow implication.
3. `policy_feed_d3426979d9550bb1`
   - Label: `correct_rejection`
   - Note: Reliability-standards approval could matter later as system context, but the artifact alone does not signal current or planned directional capital movement.
4. `policy_feed_08c2cec38f38c0df`
   - Label: `correct_rejection`
   - Note: Information-collection notice only. No demand-led buildout or directional capital deployment signal.
5. `policy_feed_4d34bc54c4bfa31e`
   - Label: `correct_rejection`
   - Note: Exchange market-structure rule change, not a capital-flow or physical buildout signal.
6. `policy_feed_ae8423eef3b90cc9`
   - Label: `correct_rejection`
   - Note: Construction appears only inside a paperwork-renewal context. The artifact does not indicate new construction activity or rising-demand capital deployment.
7. `policy_feed_c04e10c8143d48bb`
   - Label: `correct_rejection`
   - Note: Exchange order-type rule change with no plausible directional capital-flow implication for the current workflow.
8. `policy_feed_d4c584a01a37f3d8`
   - Label: `correct_rejection`
   - Note: Exchange market-structure filing only. No physical-system stress or directional capital movement evidence.
9. `policy_feed_d82c2d55d29b7ab7`
   - Label: `correct_rejection`
   - Note: Exchange market-structure filing only. No directional capital-flow implication for rising-demand structural-pressure discovery.
10. `policy_feed_313e87f5ee6bcd9f`
   - Label: `correct_rejection`
   - Note: Broker-dealer exemption order concerns regulatory thresholds, not directional capital deployment into a physical system.
11. `policy_feed_e2aa283fbc50515b`
   - Label: `correct_rejection`
   - Note: Permit-objection order for an existing facility. The artifact does not indicate new demand-led buildout or current capital movement.
12. `policy_feed_2ceb2d252849b7da`
   - Label: `correct_rejection`
   - Note: Monitoring/reporting renewal tied to already-financed projects, not a fresh signal of directional capital flow in the artifact itself.
13. `policy_feed_3d1962f60f69e27b`
   - Label: `correct_rejection`
   - Note: Exclusive licensing notice without concrete evidence of current or planned physical buildout. This remains out of scope for the current rising-demand workflow.
14. `policy_feed_e0766c57e71e1a35`
   - Label: `correct_rejection`
   - Note: OMB review and paperwork-renewal notice only. No directional capital-flow implication.
15. `policy_feed_e361f10f17cb11ef`
   - Label: `correct_rejection`
   - Note: Exchange options market-structure rule matter, not evidence of directional capital deployment into a physical system.
16. `policy_feed_e380bf5295f244ee`
   - Label: `correct_rejection`
   - Note: Correction to a licensing notice. No buildout or capital-flow evidence in the artifact.
17. `policy_feed_fe05aeb686c503b3`
   - Label: `correct_rejection`
   - Note: Contract-audit paperwork review only. No evidence of directional capital movement or demand-led physical buildout.
