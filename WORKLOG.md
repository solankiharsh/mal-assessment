# Worklog

## 2026-09-18 13:46 +04:00
- Initialized repository scaffolding (`pyproject.toml`, package layout, pytest config).
- Added `.gitignore` entry for `ledger-spec-pack/` as requested.

## 2026-09-18 13:52 +04:00
- Implemented append-only replay engine in `ledger_core/core.py`.
- Added authorization, settlement validation, reversal handling, overdraft fee reconciliation, and interest capitalization.
- Chose stream-order decisions + value-date balance model to satisfy scenario constraints.

## 2026-09-18 13:58 +04:00
- Added deterministic fixture stream and runnable report entrypoint (`python -m ledger_core`).
- Added report renderer for daily outputs including balances, fees, auth states, errors, and daily interest.

## 2026-09-18 14:03 +04:00
- Added passing tests for golden outcomes and determinism in `tests/test_replay.py`.
- Added one intentional known-red test in `tests_known_red/test_stream_order_sensitivity.py` with inline explanatory annotation.

## 2026-09-18 14:06 +04:00
- Authored `README.md`, `NUMBERS.md`, `AMBIGUITIES.md`, and `REJECTED.md` with final rule decisions and rejected criteria.
- Abandoned and documented three alternative approaches in `REJECTED.md`.

## 2026-09-18 14:11 +04:00
- Fixed auth timeline reporting so Day 2 shows `ACTIVE` and Day 4+ shows `SETTLED` for Auth-A.
- Corrected fee/day reporting to avoid negative zero formatting artifacts.
- Validated commands: `python -m pytest` passes, and known-red test fails as intended.

## 2026-09-18 14:32 +04:00
- Added CI workflow in `.github/workflows/ci.yml` to run passing tests on push/PR.
- Authored `PR_DESCRIPTION.md` with design rationale and reviewer checklist.
- Added visual architecture/thought-process artifact at `docs/approach.html`.
- Updated `README.md` with CI and artifact references.

## 2026-09-18 14:37 +04:00
- Re-ran baseline verification before semantic changes:
  - `python -m pytest tests` => pass.
  - `python -m pytest tests_known_red/test_stream_order_sensitivity.py` => intentional fail.

## 2026-09-18 14:38 +04:00
- Added minimal fee-timing counterexample test showing transient intraday negative should not trigger overdraft fee.
- Observed failure before fix: final Day 1 close was `25.00` instead of `50.00`, confirming premature fee assessment.
- Refactored fee timing to assess only closed day(s), while still reconciling already-closed historical days after backdated postings.
- Added generic replay checkpoints and asserted E7 pre-fee closes: Day2 `-370.00`, Day3 `30.00`, Day4 `-155.00`, Day5 `-155.00`.
- Re-ran passing suite; all passing tests green after fix.

## 2026-09-18 14:51 +04:00
- Created follow-up branch `pr/followup-ledger-hardening` to raise a formal PR into `main`.
- Added `PR_NOTES.md` and linked it in `README.md` for reviewer context.
- No domain logic changes in this branch; metadata/documentation touch only.

## 2026-09-18 14:52 +04:00
- Added `ARCHITECTURE_DECISIONS.md` covering architecture trade-offs and production-readiness considerations.
- Linked the document in `README.md` artifact section.
