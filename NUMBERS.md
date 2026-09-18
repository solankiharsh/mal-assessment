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
| Python runtime floor | `>=3.11` | Chosen supported runtime baseline for this assessment; compatibility for older runtimes is intentionally not in scope | A lower supported floor expands compatibility matrix and maintenance surface beyond this deliverable |
| CI Python versions | `3.11`, `3.12` | Matrix validates both declared support floor and next-minor runtime to catch compatibility regressions early | Single-version CI can miss runtime-specific failures |
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
