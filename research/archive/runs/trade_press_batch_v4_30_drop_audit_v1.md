# Trade Press Batch v4 30 Drop Audit v1

## Summary
- dropped artifacts audited: `3`
- `correct_rejection`: `0`
- `borderline_should_review`: `1`
- `false_negative`: `2`

## False Negatives
- Eaton invests $340M in US transformer production
- As load grows, Southern raises spending plan to $81B

## Borderline Should Review
- FirstEnergy expects peak load to grow 45% by 2035 on data centers

## Conclusion
- The current `trade_press` prefilter still under-recalls a small but important class of utility and transformer-capex headlines.
- The next patch should target:
  - `invests ... production`
  - `raises spending plan`
  - `peak load grows`
