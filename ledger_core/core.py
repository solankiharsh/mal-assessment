from __future__ import annotations

from collections import defaultdict
from decimal import Decimal, ROUND_FLOOR, ROUND_HALF_UP

WINDOW_DAYS = range(1, 7)
INTEREST_RATE = Decimal("0.0004")
AED_FEE = Decimal("25.00")

PRECISION = {
    "AED": Decimal("0.01"),
    "BHD": Decimal("0.001"),
}


def quantize_currency(amount: Decimal, currency: str) -> Decimal:
    return amount.quantize(PRECISION[currency], rounding=ROUND_HALF_UP)


def split_equal_instalments(total: Decimal, count: int, currency: str) -> list[Decimal]:
    quantum = PRECISION[currency]
    base = (total / Decimal(count)).quantize(quantum, rounding=ROUND_FLOOR)
    amounts = [base for _ in range(count)]
    remainder = quantize_currency(total - sum(amounts), currency)
    if remainder != Decimal("0"):  # always a single minimal-unit remainder in this fixture
        amounts[-1] = quantize_currency(amounts[-1] + remainder, currency)
    return amounts


def replay_ledger(accounts: list[dict], events: list[dict]) -> dict:
    account_map = {
        account["account_id"]: {
            "currency": account["currency"],
            "opening": quantize_currency(account["opening_balance"], account["currency"]),
        }
        for account in accounts
    }
    postings: list[dict] = []
    errors: list[dict] = []
    auths: dict[str, dict] = {}
    seen_event_ids: set[str] = set()
    fee_days: dict[str, set[int]] = defaultdict(set)
    max_booked_day = 0

    for event in events:
        event_id = event["id"]
        booked_day = event["booked_day"]
        max_booked_day = max(max_booked_day, booked_day)

        if event_id in seen_event_ids:
            errors.append(
                {
                    "event_id": event_id,
                    "booked_day": booked_day,
                    "account_id": event.get("account_id"),
                    "code": "DUPLICATE_EVENT_ID",
                    "message": f"Duplicate event ID {event_id}",
                }
            )
            continue
        seen_event_ids.add(event_id)

        event_type = event["type"]
        account_id = event["account_id"]
        currency = account_map[account_id]["currency"]

        if event_type in {"CREDIT", "DEBIT"}:
            sign = Decimal("1") if event_type == "CREDIT" else Decimal("-1")
            amount = quantize_currency(event["amount"], currency)
            postings.append(
                {
                    "account_id": account_id,
                    "value_day": event["value_day"],
                    "amount": quantize_currency(sign * amount, currency),
                    "currency": currency,
                    "kind": event_type,
                    "source_event_id": event_id,
                }
            )
            reconcile_fees(account_id, currency, booked_day, postings, fee_days, account_map)

        elif event_type == "AUTHORIZATION":
            auth_id = event["auth_id"]
            hold_amount = quantize_currency(event["amount"], currency)
            ledger_balance = close_for_day(account_id, event["value_day"], postings, account_map)
            active_holds = total_active_holds(account_id, auths, currency)
            available_after = quantize_currency(ledger_balance - active_holds - hold_amount, currency)
            status = "APPROVED" if available_after >= Decimal("0") else "DECLINED"
            auths[auth_id] = {
                "auth_id": auth_id,
                "account_id": account_id,
                "hold_amount": hold_amount if status == "APPROVED" else quantize_currency(Decimal("0"), currency),
                "status": "ACTIVE" if status == "APPROVED" else "DECLINED",
                "approved": status == "APPROVED",
                "booked_day": booked_day,
                "value_day": event["value_day"],
                "reason": None if status == "APPROVED" else "INSUFFICIENT_AVAILABLE_BALANCE",
                "status_updates": [
                    {
                        "booked_day": booked_day,
                        "status": "ACTIVE" if status == "APPROVED" else "DECLINED",
                        "hold_amount": hold_amount if status == "APPROVED" else quantize_currency(Decimal("0"), currency),
                    }
                ],
            }

        elif event_type == "SETTLEMENT":
            auth_id = event["auth_id"]
            settlement_amount = quantize_currency(event["amount"], currency)
            auth = auths.get(auth_id)
            if not auth or auth["status"] != "ACTIVE" or auth["account_id"] != account_id:
                errors.append(
                    {
                        "event_id": event_id,
                        "booked_day": booked_day,
                        "account_id": account_id,
                        "code": "UNKNOWN_AUTHORIZATION",
                        "message": f"Settlement references unknown or inactive auth {auth_id}",
                    }
                )
            else:
                auth["hold_amount"] = quantize_currency(Decimal("0"), currency)
                auth["status"] = "SETTLED"
                auth["status_updates"].append(
                    {
                        "booked_day": booked_day,
                        "status": "SETTLED",
                        "hold_amount": quantize_currency(Decimal("0"), currency),
                    }
                )
                postings.append(
                    {
                        "account_id": account_id,
                        "value_day": event["value_day"],
                        "amount": quantize_currency(-settlement_amount, currency),
                        "currency": currency,
                        "kind": "SETTLEMENT",
                        "source_event_id": event_id,
                        "auth_id": auth_id,
                    }
                )
                reconcile_fees(account_id, currency, booked_day, postings, fee_days, account_map)

        elif event_type == "REVERSAL":
            target_event_id = event["reversal_of_event_id"]
            target = next((entry for entry in postings if entry["source_event_id"] == target_event_id), None)
            if target is None:
                errors.append(
                    {
                        "event_id": event_id,
                        "booked_day": booked_day,
                        "account_id": account_id,
                        "code": "UNKNOWN_REVERSAL_TARGET",
                        "message": f"Reversal target {target_event_id} not found",
                    }
                )
            else:
                postings.append(
                    {
                        "account_id": account_id,
                        "value_day": event["value_day"],
                        "amount": quantize_currency(-target["amount"], currency),
                        "currency": currency,
                        "kind": "REVERSAL",
                        "source_event_id": event_id,
                        "reversal_of_event_id": target_event_id,
                    }
                )
                reconcile_fees(account_id, currency, booked_day, postings, fee_days, account_map)

        elif event_type == "CREDIT_INSTALMENTS":
            instalments = split_equal_instalments(event["amount"], event["instalments"], currency)
            for index, amount in enumerate(instalments, start=1):
                postings.append(
                    {
                        "account_id": account_id,
                        "value_day": event["value_day"],
                        "amount": amount,
                        "currency": currency,
                        "kind": "CREDIT_INSTALMENT",
                        "source_event_id": event_id,
                        "instalment_index": index,
                    }
                )
            reconcile_fees(account_id, currency, booked_day, postings, fee_days, account_map)

        else:
            errors.append(
                {
                    "event_id": event_id,
                    "booked_day": booked_day,
                    "account_id": account_id,
                    "code": "UNKNOWN_EVENT_TYPE",
                    "message": f"Unknown event type {event_type}",
                }
            )

    daily_interest = {account_id: {} for account_id in account_map}
    interest_capitalization = {account_id: quantize_currency(Decimal("0"), info["currency"]) for account_id, info in account_map.items()}

    for account_id, info in account_map.items():
        currency = info["currency"]
        for day in WINDOW_DAYS:
            pre_interest_close = close_for_day(account_id, day, postings, account_map)
            if pre_interest_close > Decimal("0"):
                accrual = quantize_currency(pre_interest_close * INTEREST_RATE, currency)
            else:
                accrual = quantize_currency(Decimal("0"), currency)
            daily_interest[account_id][day] = accrual
            interest_capitalization[account_id] = quantize_currency(
                interest_capitalization[account_id] + accrual, currency
            )

        if interest_capitalization[account_id] > Decimal("0"):
            postings.append(
                {
                    "account_id": account_id,
                    "value_day": 6,
                    "amount": interest_capitalization[account_id],
                    "currency": currency,
                    "kind": "INTEREST_CAPITALIZATION",
                    "source_event_id": f"INTEREST-{account_id}",
                }
            )

    daily_report = {account_id: {} for account_id in account_map}
    auth_states_by_day = auth_states_timeline(auths)

    for account_id, info in account_map.items():
        currency = info["currency"]
        for day in WINDOW_DAYS:
            daily_report[account_id][day] = {
                "closing_balance": close_for_day(account_id, day, postings, account_map),
                "fee_assessed": quantize_currency(
                    abs(
                        sum(
                            (
                                entry["amount"]
                                for entry in postings
                                if entry["account_id"] == account_id
                                and entry["kind"] == "OVERDRAFT_FEE"
                                and entry["value_day"] == day
                            ),
                            Decimal("0"),
                        )
                    ),
                    currency,
                ),
                "authorizations": auth_states_by_day[account_id][day],
                "errors": [
                    error
                    for error in errors
                    if error["account_id"] == account_id and error["booked_day"] == day
                ],
                "daily_interest": daily_interest[account_id][day],
            }

    return {
        "postings": postings,
        "errors": errors,
        "authorizations": auths,
        "daily_interest": daily_interest,
        "interest_capitalization": interest_capitalization,
        "daily_report": daily_report,
    }


def auth_states_timeline(auths: dict[str, dict]) -> dict[str, dict[int, list[dict]]]:
    result: dict[str, dict[int, list[dict]]] = defaultdict(lambda: {day: [] for day in WINDOW_DAYS})

    for day in WINDOW_DAYS:
        for auth_id, auth in sorted(auths.items()):
            updates = [update for update in auth["status_updates"] if update["booked_day"] <= day]
            if updates:
                latest = updates[-1]
                result[auth["account_id"]][day].append(
                    {
                        "auth_id": auth_id,
                        "status": latest["status"],
                        "hold_amount": latest["hold_amount"],
                    }
                )

    return result


def total_active_holds(account_id: str, auths: dict[str, dict], currency: str) -> Decimal:
    return quantize_currency(
        sum(
            (
                auth["hold_amount"]
                for auth in auths.values()
                if auth["account_id"] == account_id and auth["status"] == "ACTIVE"
            ),
            Decimal("0"),
        ),
        currency,
    )


def close_for_day(account_id: str, day: int, postings: list[dict], account_map: dict[str, dict]) -> Decimal:
    currency = account_map[account_id]["currency"]
    opening = account_map[account_id]["opening"]
    amount = opening + sum(
        (
            posting["amount"]
            for posting in postings
            if posting["account_id"] == account_id and posting["value_day"] <= day
        ),
        Decimal("0"),
    )
    return quantize_currency(amount, currency)


def reconcile_fees(
    account_id: str,
    currency: str,
    up_to_booked_day: int,
    postings: list[dict],
    fee_days: dict[str, set[int]],
    account_map: dict[str, dict],
) -> None:
    if currency != "AED":
        return

    for day in range(1, min(6, up_to_booked_day) + 1):
        if day in fee_days[account_id]:
            continue
        close = close_for_day(account_id, day, postings, account_map)
        if close < Decimal("0"):
            postings.append(
                {
                    "account_id": account_id,
                    "value_day": day,
                    "amount": quantize_currency(-AED_FEE, currency),
                    "currency": currency,
                    "kind": "OVERDRAFT_FEE",
                    "source_event_id": f"FEE-{account_id}-D{day}",
                }
            )
            fee_days[account_id].add(day)
