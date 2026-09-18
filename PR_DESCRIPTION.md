# PR: Build append-only in-memory ledger core for six-day replay exercise

## Why
This PR implements the requested in-memory ledger core and validates behavior through executable tests and deterministic replay output.

## What changed
- Implemented single public replay seam in `ledger_core/core.py`.
- Added fixture accounts and ordered event stream (E1..E10) in `ledger_core/fixtures.py`.
- Added CLI runner printing daily balances, fees, auth states, errors, and interest in `ledger_core/__main__.py`.
- Added deterministic renderer helpers in `ledger_core/reporting.py`.
- Added acceptance-oriented tests in `tests/test_replay.py`.
- Added one intentionally failing known-red test in `tests_known_red/test_stream_order_sensitivity.py`.
- Added required decision logs: `NUMBERS.md`, `AMBIGUITIES.md`, `REJECTED.md`, `WORKLOG.md`.
- Added CI workflow that runs only the passing suite.
- Added architecture/thought-process artifact in `docs/approach.html`.

## Design reasoning
1. **Replay order and value date are separated intentionally**
   - Decision outcomes (auth approve/decline) are stream-order facts.
   - Monetary closes are value-date projections and can be historically shifted by backdated events.
2. **Ledger is append-only**
   - No event or posting is mutated/deleted.
   - Reversals are compensating entries.
3. **Fees are assessed at most once per account/day**
   - Fee reconciliation is chronological and idempotent by `(account, day)`.
4. **Interest is exact at currency precision**
   - Daily accruals are rounded per-currency and summed exactly into Day-6 capitalization.

## Incorrect acceptance criteria explicitly rejected
See `REJECTED.md` for complete rationale. Rejected criteria:
- “E7 causes exactly one overdraft fee…”
- “After E9, all balances and fees return pre-E7…”
- “All E10 instalments must be 3.334…”
- “Discard remainder if rounded accrual sum mismatches capitalization…”

## How to verify
- Replay output:
  - `python -m ledger_core`
- Passing tests:
  - `python -m pytest tests`
- Required known-red test (must fail):
  - `python -m pytest tests_known_red/test_stream_order_sensitivity.py`

## Reviewer checklist
- [ ] Daily report includes Day 1..Day 6 closes, fees, auth states, errors, interest
- [ ] Auth-A approved then settled; Auth-Z settlement rejected; Auth-B declined in canonical order
- [ ] E10 instalments conserve exactly BHD 10.000 as `3.333, 3.333, 3.334`
- [ ] Interest capitalization equals exact sum of rounded daily accruals
- [ ] `REJECTED.md` includes all incorrect criteria and abandoned approaches
