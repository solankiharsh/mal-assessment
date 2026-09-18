# Ambiguities and Resolutions

1. **When to assess fees after backdated events?**
   - Resolution: assess fees only for closed days. As replay advances to a later booked day, close prior day(s). After a backdated money posting, re-evaluate already-closed historical days, but never assess the still-open day.

2. **Does reversal cancel already-booked overdraft fees?**
   - Resolution: no implicit fee reversal rule is provided; fees remain append-only.

3. **Should non-AED accounts receive overdraft fees?**
   - Resolution: no. Rule gives an AED-denominated fee with no FX rule, so fee applies only to AED account in this fixture.

4. **How to split BHD 10.000 into three equal instalments at 3dp?**
   - Resolution: `3.333, 3.333, 3.334` to conserve exact total with minimal-unit spread.

5. **Does authorization affect ledger or available balance only?**
   - Resolution: available balance only; ledger changes only on booked monetary entries.

6. **Can settlement without prior authorization debit funds?**
   - Resolution: no. Reject with deterministic error and append no posting.

7. **Interest rounding policy**
   - Resolution: round each daily accrual at currency precision using half-up; capitalization equals exact sum of rounded daily accruals.

8. **Decision time semantics for authorization**
   - Resolution: evaluate at replay position using data known at that point; do not retroactively re-decide.

9. **Where should the intentional failing test live?**
   - Resolution: outside default pytest discovery in `tests_known_red/`, with a dedicated command.

10. **Duplicate event IDs behavior**
   - Resolution: reject duplicates as deterministic replay input errors.
