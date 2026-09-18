# In-Memory Ledger Core

Append-only, in-memory ledger replay for the six-day exercise window.

## Run

Optional isolated setup:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install pytest
```

```bash
python -m ledger_core
```

This prints, per account and per day, closing ledger balance, fee assessed, authorization states, errors, and daily interest.

## Test Commands

Passing suite:

```bash
python -m pytest
```

Known-red suite (required intentional failure):

```bash
python -m pytest tests_known_red/test_stream_order_sensitivity.py
```

## Notes

- Stream order is authoritative for decisions.
- Value date is authoritative for effective balances.
- Fees are append-only and are not implicitly reversed when E7 is reversed by E9.
