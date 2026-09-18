# Ambiguities and Resolutions

1. **When to assess fees after backdated events?**
   - Resolution: assess fees only for closed days. As replay advances to a later booked day, close prior day(s). After a backdated money posting, re-evaluate already-closed historical days, but never assess the still-open day.

2. **Does reversal cancel already-booked overdraft fees?**
   - Resolution: no implicit fee-reversal rule is provided; fees remain append-only unless an explicit compensating fee entry is modeled.

3. **Should non-AED accounts receive overdraft fees?**
   - Resolution: no in this exercise. The fee amount is AED-denominated and no FX conversion rule exists.

4. **How to split BHD 10.000 into three equal instalments at 3dp?**
   - Resolution: `3.333, 3.333, 3.334` to conserve total exactly with minimum-unit spread.

5. **Does authorization affect ledger or available balance only?**
   - Resolution: available balance only. Ledger changes only when monetary postings are appended.

6. **Can settlement without prior authorization debit funds?**
   - Resolution: no. Reject with deterministic error and append no monetary posting.

7. **Interest rounding policy**
   - Resolution: round each daily accrual at currency precision with round-half-up; capitalization equals exact sum of rounded daily accruals.

8. **Stream order vs booked day**
   - Resolution: supplied stream order is authoritative. Booked day metadata is not used as a sorting key.

9. **Booked day vs value day**
   - Resolution: booked day controls what is known at decision time (approvals/rejections/errors). Value day controls historical monetary effect on closes, fees, and interest bases.

10. **Fee discovery day vs fee assessment day**
   - Resolution: a backdated event may reveal a historical negative close later in operational time, but the fee posting value day remains the historical day being assessed.

11. **Authorization decisions are non-retroactive**
   - Resolution: later reversals/backdated corrections do not re-decide prior authorizations. Decisions are historical facts at replay position.

12. **How to process E10 after a Day-6 event without reordering**
   - Resolution: process in stream order; E10 may carry earlier booked/value metadata but remains at its stream position. No reordering pass is applied.

13. **Day-6 interest circularity**
   - Resolution: Day-6 accrual uses the Day-6 close before capitalization. Capitalization credit does not earn interest on itself.

14. **Interest basis after historical corrections**
   - Resolution: interest is calculated from the final reconstructed effective day closes after all postings and fees are appended.

15. **Hold amount vs settlement amount mismatch (Auth-A 200 vs 185)**
   - Resolution: full hold is released, but only settled amount is debited from ledger.

16. **Known-red failing test placement**
   - Resolution: keep intentional failing test outside default suite so normal verification remains green while still runnable and genuinely failing.

17. **Duplicate event IDs behavior**
   - Resolution: reject duplicate input IDs deterministically to prevent replay double-application.
