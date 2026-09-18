# Numbers and Constants

This file records numeric values that are either domain rules or deliberate implementation/tooling choices.

| Constant / choice | Value | Why this value | Why not materially smaller? |
|---|---:|---|---|
| Replay window length | 6 days | Required exercise window (Day 1–Day 6) | 3 days omits required behavior and events |
| AED precision | 2 decimal places | Required by exercise | 1 decimal violates currency precision rule |
| BHD precision | 3 decimal places | Required by exercise | 2 decimals violates currency precision rule |
| Overdraft fee | AED 25.00 | Required business rule | AED 12.50 is a different policy |
| Daily interest rate | 0.04% (`0.0004`) | Required business rule | 0.02% is a different policy |
| E10 instalments | 3 | Required by input event | Not a tuning parameter |
| E10 total | BHD 10.000 | Required by input event | Smaller total changes fixture |
| BHD remainder quantum | 0.001 | Smallest representable BHD unit | 0.0005 is unrepresentable at 3dp |
| Python runtime floor | `>=3.11` | Uses modern typing syntax (`list[dict]`, `int | None`) and keeps local/runtime matrix small | Lower floor (3.10 or below) would require backports or syntax changes |
| CI Python version | 3.12 | Single stable CI interpreter above minimum floor; catches regressions while staying close to local tooling | 3.11-only CI gives less forward-compatibility signal |
| Project version | `0.1.0` | Pre-1.0 assessment artifact with non-stable public API expectations | `0.0.x` obscures that this is an end-to-end working slice |

## Deliberately removed arbitrary pin

- Build dependency floor `setuptools>=68` was removed.
- Reason: no implementation behavior depends on that specific floor; plain `setuptools` is sufficient for this assessment package.

## Six-day bounds in code

- The implementation now centralizes day-window bounds using `WINDOW_END_DAY = 6` and `WINDOW_DAYS = range(1, WINDOW_END_DAY + 1)`.
- Reason: removes repeated magic `6` literals while keeping the fixed window explicit.

## Money equality policy

- Monetary comparisons remain exact at currency precision.
- No epsilon/tolerance constants are used.
