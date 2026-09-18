# Numbers and Constants

| Constant | Value | Why this value | Why not half? |
|---|---:|---|---|
| Window length | 6 days | Required by statement | 3 days omits required events |
| AED precision | 2 dp | Required by statement | 1 dp violates currency precision |
| BHD precision | 3 dp | Required by statement | 2 dp violates currency precision |
| Overdraft fee | AED 25.00 | Required by statement | AED 12.50 is a different rule |
| Daily interest rate | 0.04% (0.0004) | Required by statement | 0.02% is a different rule |
| E10 instalments | 3 | Required by event E10 | Not tunable |
| E10 total | BHD 10.000 | Required by event E10 | BHD 5.000 changes fixture |
| BHD residual quantum | 0.001 | Smallest representable BHD unit | 0.0005 cannot be represented |
