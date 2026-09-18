# Rejected Acceptance Criteria and Abandoned Approaches

## Rejected Criteria

1. **Rejected:** “E7 causes exactly one overdraft fee to be assessed, on Day 2.”
   - Reason: with value-date replay and per-day closing evaluation, E7 makes Day 2, Day 4, and Day 5 closes negative, so exactly three fees are assessed once each day.

2. **Rejected:** “After E9, all balances and fees return to their pre-E7 values.”
   - Reason: E9 is a compensating reversal entry and does not mutate history; previously assessed fees remain unless an explicit fee-reversal rule exists.

3. **Rejected:** “The three BHD instalments in E10 must each be BHD 3.334.”
   - Reason: `3.334 * 3 = 10.002`, which violates conservation of E10 total `10.000`.

4. **Rejected:** “If rounded daily interest accruals do not sum to the capitalized total, the remainder is discarded.”
   - Reason: non-negotiable rule requires rounded daily accruals to sum exactly to capitalization, so discard logic is invalid.

## Criteria Not Rejected

- “Day 2 closing ledger balance, evaluated at end of Day 5 and before any fee is assessed, is AED -370.00.” is accepted.
- “The Day 4 settlement of Auth-A must be accepted.” is accepted.
- “Unknown authorization settlement must be rejected with no funds movement.” is accepted.
- “If Auth-B is approved, hold reduces available but not ledger.” is conditionally true but in this fixture Auth-B is declined.

## Abandoned Mid-Build Approaches

1. **Abandoned:** retroactively deleting fee entries after reversal E9.
   - Why abandoned: violates append-only ledger rule.

2. **Abandoned:** equal fixed instalments `3.333, 3.333, 3.333` plus dropped remainder.
   - Why abandoned: violates strict amount conservation to `10.000`.

3. **Abandoned:** single-pass fee calculation without chronological cascading.
   - Why abandoned: misses Day 4/Day 5 negatives induced by earlier fee postings.
