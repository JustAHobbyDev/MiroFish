# Prefilter Drop Audit

- Source audit set: `federal_register_historical_pages1_3_rejection_audit_v1`
- Source batch: `federal_register_historical_pages1_3_prefilter_v1`
- Reviewed scope: `25` sampled deterministic prefilter drops

## Summary

- `correct_rejection`: `24`
- `borderline_should_review`: `1`
- `false_negative`: `0`

Overall judgment:
The deterministic prefilter sample was mostly clean, but one dropped policy notice should have been surfaced for review rather than dropped outright.

## Important Scope Boundary

These labels are only for the current workflow:

- detect directional capital movement
- infer rising-demand structural pressure
- defer constrained-access and exclusivity workflows

This audit tests whether the title-level deterministic prefilter is too aggressive.

## Main Finding

- The sampled prefilter drops were mostly valid.
- One item should likely move from `drop` to `review`:
  - `policy_feed_43e47ef2865c42a1`
  - `Notice of Availability of the 2025 Record of Decision for the Final Environmental Impact Statement for the National Petroleum Reserve-Alaska, Integrated Activity Plan`

Why:
- it is still not a direct capital-flow proof
- but it is sufficiently tied to resource-development enablement that the prefilter should not discard it at the title stage

## Reviewed Artifacts

1. `policy_feed_5e371424743a74c8`
   - Label: `correct_rejection`
   - Note: Meeting notice only. No directional capital-flow implication.
2. `policy_feed_03a37dd6adb7bceb`
   - Label: `correct_rejection`
   - Note: Information-collection renewal only. No demand-led buildout or directional capital deployment signal.
3. `policy_feed_ea4b54506ece1d9f`
   - Label: `correct_rejection`
   - Note: Paperwork-renewal notice without current or planned physical buildout implications.
4. `policy_feed_43e47ef2865c42a1`
   - Label: `borderline_should_review`
   - Note: This is policy-enabling rather than demand-proving, but it concerns petroleum reserve planning and could plausibly precede resource-development capital deployment. The title-level prefilter should likely surface this for review instead of dropping it.
5. `policy_feed_8da43a2ac810265d`
   - Label: `correct_rejection`
   - Note: Eligibility-matching/privacy program notice only. No capital-flow signal.
6. `policy_feed_82b3a4fb5bb83ba1`
   - Label: `correct_rejection`
   - Note: Records-system modification notice only. No directional capital-flow implication.
7. `policy_feed_08893b3c7841ab48`
   - Label: `correct_rejection`
   - Note: Survey/data-collection extension only. No evidence of material capital deployment.
8. `policy_feed_86645418b5eac10b`
   - Label: `correct_rejection`
   - Note: OMB review and accreditation-process paperwork only. No directional capital-flow signal.
9. `policy_feed_af5c6af3b1d7f578`
   - Label: `correct_rejection`
   - Note: Compliance and emissions-plan rulemaking context, not direct evidence of rising-demand capital deployment.
10. `policy_feed_ac3e57f5db8e9716`
   - Label: `correct_rejection`
   - Note: Trade-review result with no direct directional capital-flow implication for the current workflow.
11. `policy_feed_dd464ccc33c7f0e2`
   - Label: `correct_rejection`
   - Note: Ownership/control notice for a financial institution, not a physical-system capital-flow signal relevant to structural-pressure discovery.
12. `policy_feed_12df69b556d95598`
   - Label: `correct_rejection`
   - Note: Trade-remedy determination that could matter later as policy context, but the artifact alone does not indicate current or planned demand-led capital deployment.
13. `policy_feed_41d9d22bf939d42d`
   - Label: `correct_rejection`
   - Note: Patent-extension determination only. No directional capital-flow implication for the current workflow.
14. `policy_feed_c0733abbebfa1349`
   - Label: `correct_rejection`
   - Note: Patent-extension determination only. No current or planned physical buildout signal.
15. `policy_feed_3e90113116e42999`
   - Label: `correct_rejection`
   - Note: Defense acquisition paperwork extension only. No actual procurement, construction, or capacity signal in the artifact.
16. `policy_feed_abf53f6d3d69992a`
   - Label: `correct_rejection`
   - Note: Advisory-committee meeting notice only. No directional capital-flow implication.
17. `policy_feed_477fbbb60340ce93`
   - Label: `correct_rejection`
   - Note: Supplier-registration paperwork renewal only. No procurement or buildout event is being signaled.
18. `policy_feed_d4ace14c67c704ab`
   - Label: `correct_rejection`
   - Note: Survey revision only. No capital-flow or physical buildout implication.
19. `policy_feed_3b08b5435c2d56cd`
   - Label: `correct_rejection`
   - Note: Patent/import investigation notice. This is litigation/trade enforcement context, not a directional capital-flow signal for rising-demand structural pressure.
20. `policy_feed_dc6600fce2d77976`
   - Label: `correct_rejection`
   - Note: Decommissioning-timeline exemption for an existing plant. Not evidence of new demand-led capital deployment.
21. `policy_feed_33dbbe37b20cbf1e`
   - Label: `correct_rejection`
   - Note: Potentially relevant to a constrained-access or drug-exclusivity workflow later, but out of scope for the current rising-demand capital-flow workflow.
22. `policy_feed_c30918e19ffbfd9b`
   - Label: `correct_rejection`
   - Note: Board meeting notice only. No directional capital-flow implication.
23. `policy_feed_9dad61f770560804`
   - Label: `correct_rejection`
   - Note: Administrative notice about a negotiated service agreement. No capital-flow or physical-system buildout signal.
24. `policy_feed_9d359c97ae6a69c1`
   - Label: `correct_rejection`
   - Note: ITC complaint/public-interest notice only. No directional capital-flow implication.
25. `policy_feed_78a6cc50b88fec20`
   - Label: `correct_rejection`
   - Note: Labor-rule withdrawal may matter as general policy context, but the artifact itself is not a direct signal of demand-led capital deployment.
