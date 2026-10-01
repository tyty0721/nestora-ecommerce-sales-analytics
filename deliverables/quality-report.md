# Data quality

Synthetic demo data. Unresolved rows are excluded.

- orders: {'retained': 2691, 'pending': 14, 'deduplicated': 10}
- products: {'retained': 20, 'deduplicated': 1}
- refunds: {'retained': 175, 'pending': 3, 'deduplicated': 1}
- excluded_orders: 8

Pending reasons: {
  "R01-unmatched-valid-sale": 2,
  "R03-cumulative-refund-exceeds-sale": 1,
  "J01-unknown-or-conflicted-SKU": 1,
  "O02-whole-order-excluded": 4,
  "V01-invalid_discount": 1,
  "V01-missing_amount": 1,
  "V01-invalid_quantity": 1,
  "V01-ambiguous_or_invalid_date": 1,
  "V01-invalid_country": 1,
  "K02-same-key-conflict": 2,
  "O01-order-attribute-conflict": 2
}

Every source row is accounted for in row-ledger.csv. Approved changes are in normalizations.csv. Refund overages exclude the complete refund group. Missing values are not imputed. See validation/ for independently generated controls. Human spot-check remains pending until performed by the owner.
