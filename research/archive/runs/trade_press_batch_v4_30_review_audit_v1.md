# Trade Press Batch v4 30 Review Audit v1

## Summary
- review artifacts audited: `12`
- `correct_candidate`: `5`
- `borderline_should_review`: `7`
- `false_positive`: `0`

## Correct Candidates
- Jabil picks North Carolina for $500M AI facility
- Power enclosure maker AVL to establish its first US plant
- Hitachi Energy commits $250M to address transformer shortage
- DTE inks first data center deal to grow electric load 25%
- Italy-based Westrafo to build its first US transformer plant

## Borderline Should Review
- Hyundai boosts US investments to $26B through 2028
- PG&E data center pipeline swells to 10GW
- US utility Exelon reports data center pipeline of 33GW
- First Energy data center pipeline surges to 2.6GW by 2029
- PPL Electric's data center pipeline soars to 14GW
- Exelon data center pipeline jumps to 17 GW as load forecast turns positive
- FirstEnergy’s 5-year data center pipeline doubles to 3 GW

## Conclusion
- The review bucket is doing real work.
- It is catching both:
  - valid buildout candidates that lack explicit spend language in the headline
  - planning-stage load and pipeline signals that should stay review-stage
- The current failure mode is not false positives inside review.
- The current failure mode is over-promotion when the extractor treats pipeline articles as direct candidates.
