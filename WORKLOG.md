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
