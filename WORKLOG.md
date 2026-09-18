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

## 2026-09-18 14:56 +04:00
- Created branch `pr/final-submission-hardening` from latest `main` (`e12f0c9`).
- Ran baseline checks before new changes:
  - `python -m pytest tests -q` => `4 passed`.
  - `python -m pytest tests_known_red/test_stream_order_sensitivity.py -q` => intentional fail.
  - `python -m ledger_core` => replay output inspected; canonical day-by-day output unchanged.

## 2026-09-18 15:01 +04:00
- Added executable invariants in `tests/test_replay.py`:
  - E6 has zero monetary effect (`source_event_id == "E6"` absent from postings).
  - Explicit append-only E7/E9 compensating-entry assertions.
  - Fee postings persisted with day set `{2,4,5}` at `-25.00` each.
  - ACC-002 daily interest literals and capitalization `0.008`.
  - Explicit E10 instalment sum assertion `10.000`.
- Ran `python -m pytest tests -q` => `5 passed`.

## 2026-09-18 15:05 +04:00
- Updated numeric/toolchain decisions:
  - removed arbitrary `setuptools>=68` floor from `pyproject.toml`.
  - introduced `WINDOW_END_DAY = 6` constant in `ledger_core/core.py` to remove repeated literal bounds.
  - expanded `NUMBERS.md` to include Python/CI/version/toolchain rationale.

## 2026-09-18 15:08 +04:00
- Expanded `AMBIGUITIES.md` with temporal semantics (stream order vs booked day, booked vs value day, fee discovery vs assessment day, non-retroactive authorization decisions, day-6 interest circularity, E10 ordering semantics).
- Rewrote `ARCHITECTURE_DECISIONS.md` with explicit implemented-vs-production lifecycle boundaries and four required sections.
- Regulatory source checks (CBUAE primary URLs):
  - https://rulebook.centralbank.ae/en/rulebook/article-7-internal-control-system
  - https://rulebook.centralbank.ae/en/rulebook/consumer-protection-standards
  - https://rulebook.centralbank.ae/en/rulebook/4-record-keeping
  Used indexed metadata for status/effective-date confirmation in this environment.

## 2026-09-18 15:09 +04:00
- Updated `docs/approach.html` to add `Production Architecture & Trade-offs` while preserving existing visual style.
- Generated `docs/architecture-tradeoffs.pdf` from `ARCHITECTURE_DECISIONS.md`.
- Verified PDF requirements:
  - page count: `3` pages;
  - size: `9,059` bytes (< 25 MB);
  - rendered and visually inspected all pages via `docs/pdf-previews/page-1.png`, `page-2.png`, `page-3.png` before cleanup.
- Re-ran verification:
  - `python -m pytest tests -q` => pass;
  - `python -m pytest tests_known_red/test_stream_order_sensitivity.py -q` => intentional fail.

## 2026-09-18 15:11 +04:00
- Normalized remaining day-bound magic numbers in code (`WINDOW_END_DAY` usage).
- Updated architecture references with current CBUAE metadata wording and removed unsupported effective-date precision where source metadata was not explicit.
- Regenerated and revalidated the PDF after text corrections.

## 2026-09-18 15:12 +04:00
- Pushed branch `pr/final-submission-hardening` and captured PR creation URL.
- Checked GitHub Actions run history via GitHub API.
- Observed no push-triggered run for this branch because workflow push trigger targets `main` only; branch CI will execute once PR is opened (`pull_request` on `main`).
