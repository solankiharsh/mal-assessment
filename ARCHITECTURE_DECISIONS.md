# Architecture Decisions and Production Considerations

## Append-only at scale

The first breakage point at 100× volume is read amplification, not write throughput. The current implementation recomputes balances and fee eligibility by scanning append-only postings repeatedly, so latency grows with ledger age. Memory pressure follows because all postings are held in-process and never compacted.

Unbounded state accumulates in three places:
- posting history per account;
- replay checkpoints used for audit assertions;
- authorization/status history retained for full-window reporting.

The cheapest structural change that defers this is to introduce **materialized daily snapshots** per account (`closing_balance`, `fees_assessed`, `interest_base`, `active_holds_total`) and replay deltas from the latest snapshot instead of from genesis. This preserves append-only semantics while reducing balance lookup from O(total_postings) toward O(postings_since_snapshot). It also creates a natural retention boundary for hot memory while keeping immutable history in colder storage tiers.

## Value-dated entries in production

Value-dated entries expand both operational and regulatory surface in a UAE-licensed bank because they can alter historical effective balances after customer-visible statements, fees, and controls have already been emitted.

Operationally, this creates:
- retroactive impact to daily closes, fee eligibility, and derived analytics;
- reconciliation complexity across channels that observed different provisional states;
- customer-dispute risk when timeline understanding differs from posting sequence.

Regulatory/compliance impact includes:
- need to evidence deterministic treatment of backvalued entries;
- need for robust audit trail showing booking time vs value date vs assessment effects;
- potential conduct risk if retroactive charging appears inconsistent.

One control I would add before go-live: **a mandatory backvalue-impact control gate** that computes and records a signed impact report before acceptance (affected days, accounts, fees/interest delta, and reason code), with maker-checker approval for high-impact cases. This creates pre-booking governance and post-hoc auditability without violating append-only history.

## Authorization lifecycle

Beyond matching settlement, an authorization can end in several ways in this model and in production semantics:

- **Declined at request time**
  - Real-world scenario: insufficient available funds, risk rule breach, or velocity limit.
  - Mandated behavior: return deterministic decline reason; create no hold; persist decision/audit event.

- **Expired (hold timeout window elapsed)**
  - Real-world scenario: merchant never captures or submits too late.
  - Mandated behavior: auto-release hold at timeout; emit lifecycle event; notify channels that available balance increased.

- **Reversed/voided by merchant or network**
  - Real-world scenario: cancelled checkout, terminal reversal, duplicate auth correction.
  - Mandated behavior: release hold immediately; preserve original auth and reversal events; no silent overwrite.

- **Partially captured then remainder released**
  - Real-world scenario: final settlement lower than authorized amount (tips, fuel, hotel).
  - Mandated behavior: settle captured amount, transition remainder to released state, preserve full chain.

- **Force-completed without prior linked auth (stand-in/late presentment handling path)**
  - Real-world scenario: network or merchant submits financial message without a valid open hold.
  - Mandated behavior: route to exception workflow; apply policy-driven posting decision; generate compliance and ops alerts.

## What we cut and why

The implementation intentionally constrained scope to keep core correctness demonstrable. Key simplifications and deferred production risks:

- **Single-process in-memory state**
  - Deferred risk: crash recovery, horizontal scaling, and consistency across nodes.

- **No persistence/event store partitioning**
  - Deferred risk: long-horizon replay cost, retention controls, forensic query performance.

- **No idempotency keys beyond duplicate event IDs**
  - Deferred risk: at-least-once delivery duplicates across distributed ingestion paths.

- **No FX or multi-currency conversion path**
  - Deferred risk: fee/interest policy across cross-currency products and rounding governance.

- **No cut-off calendar/holiday/time-zone engine**
  - Deferred risk: day-boundary correctness under market calendars, daylight shifts, and channel cut-offs.

- **No partial authorization amendments/increments**
  - Deferred risk: real card-present/card-not-present lifecycle complexity and customer-available-balance volatility.

- **No dispute/chargeback lifecycle**
  - Deferred risk: downstream reversals and representment interactions with historical fee/interest consequences.

- **No access control, dual control, or approvals workflow**
  - Deferred risk: operational fraud and unauthorized high-impact backvalue operations.

- **No observability SLOs/alerts**
  - Deferred risk: delayed detection of reconciliation drift, ingestion lag, and policy misapplication.

- **No legal disclosure/customer-communication layer**
  - Deferred risk: conduct and complaint exposure when retroactive effects occur.
