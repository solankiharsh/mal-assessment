# PR: test/docs: close submission evidence gaps and finalize architecture trade-offs

## Summary
This is a hardening PR on top of the existing ledger implementation.

- No rewrite of ledger architecture.
- No history rewrite/squash.
- No change to canonical final replay outputs.
- Adds missing executable evidence and final submission artifacts.

## What changed

### Test evidence hardening
- Proved `E6` rejected settlement has zero monetary effect by asserting no posting exists with `source_event_id == "E6"`.
- Proved append-only E7/E9 semantics directly through postings:
  - E7 remains `-620.00` at value day 2,
  - E9 is separate `+620.00` at value day 2 with `reversal_of_event_id == "E7"`.
- Proved overdraft fee postings persist after E9 with exact assessment days `{2,4,5}` and amount `-25.00` once/day.
- Locked ACC-002 daily interest and capitalization literals:
  - daily accruals `0.000, 0.000, 0.000, 0.000, 0.004, 0.004`,
  - capitalization `0.008`,
  - Day 6 close `10.008`.
- Retained installment literals `3.333, 3.333, 3.334` and now explicitly assert exact sum `10.000`.

### Numeric/tooling/document consistency
- Removed arbitrary build pin floor (`setuptools>=68` → `setuptools`).
- Centralized six-day bound in code with `WINDOW_END_DAY = 6`.
- Expanded `NUMBERS.md` with runtime/toolchain numeric choices and rationale.
- Expanded `AMBIGUITIES.md` with temporal semantics now critical to behavior.

### Architecture submission artifacts
- Rewrote canonical architecture text in `ARCHITECTURE_DECISIONS.md` with four required sections.
- Corrected lifecycle honesty: implemented non-settlement terminal state is exactly `DECLINED`.
- Added explicit production-gap lifecycle states as non-implemented.
- Updated `docs/approach.html` with synchronized “Production Architecture & Trade-offs” section.
- Generated required PDF: `docs/architecture-tradeoffs.pdf` (4 pages, under 25 MB).

## Regulatory references used (primary CBUAE URLs)
- https://rulebook.centralbank.ae/en/rulebook/article-7-internal-control-system
- https://rulebook.centralbank.ae/en/rulebook/consumer-protection-standards
- https://rulebook.centralbank.ae/en/rulebook/4-record-keeping

## Verification
- `python -m pytest tests` → pass.
- `python -m pytest tests_known_red/test_stream_order_sensitivity.py` → intentional fail (expected).
- `python -m ledger_core` → output inspected.
- `docs/architecture-tradeoffs.pdf` verified:
  - page count: 4,
  - size: < 25 MB,
  - all pages rendered and visually checked.
