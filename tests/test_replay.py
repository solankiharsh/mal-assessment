from decimal import Decimal

from ledger_core.core import replay_ledger
from ledger_core.fixtures import default_accounts, default_events


def test_replay_golden_results() -> None:
    report = replay_ledger(default_accounts(), default_events())

    acc1 = report["daily_report"]["ACC-001"]
    acc2 = report["daily_report"]["ACC-002"]

    assert acc1[1]["closing_balance"] == Decimal("250.00")
    assert acc1[2]["closing_balance"] == Decimal("225.00")
    assert acc1[3]["closing_balance"] == Decimal("625.00")
    assert acc1[4]["closing_balance"] == Decimal("415.00")
    assert acc1[5]["closing_balance"] == Decimal("390.00")
    assert acc1[6]["closing_balance"] == Decimal("390.93")

    assert acc1[2]["fee_assessed"] == Decimal("25.00")
    assert acc1[4]["fee_assessed"] == Decimal("25.00")
    assert acc1[5]["fee_assessed"] == Decimal("25.00")

    assert acc1[4]["errors"][0]["code"] == "UNKNOWN_AUTHORIZATION"

    assert report["authorizations"]["Auth-A"]["status"] == "SETTLED"
    assert report["authorizations"]["Auth-B"]["status"] == "DECLINED"
    assert acc1[2]["authorizations"] == [{"auth_id": "Auth-A", "status": "ACTIVE", "hold_amount": Decimal("200.00")}]
    assert acc1[4]["authorizations"] == [{"auth_id": "Auth-A", "status": "SETTLED", "hold_amount": Decimal("0.00")}]
    assert acc1[5]["authorizations"] == [
        {"auth_id": "Auth-A", "status": "SETTLED", "hold_amount": Decimal("0.00")},
        {"auth_id": "Auth-B", "status": "DECLINED", "hold_amount": Decimal("0.00")},
    ]

    assert report["daily_interest"]["ACC-001"] == {
        1: Decimal("0.10"),
        2: Decimal("0.09"),
        3: Decimal("0.25"),
        4: Decimal("0.17"),
        5: Decimal("0.16"),
        6: Decimal("0.16"),
    }
    assert report["interest_capitalization"]["ACC-001"] == Decimal("0.93")

    assert acc2[1]["closing_balance"] == Decimal("0.000")
    assert acc2[4]["closing_balance"] == Decimal("0.000")
    assert acc2[5]["closing_balance"] == Decimal("10.000")
    assert acc2[6]["closing_balance"] == Decimal("10.008")

    instalments = [
        entry["amount"]
        for entry in report["postings"]
        if entry["source_event_id"] == "E10"
    ]
    assert instalments == [Decimal("3.333"), Decimal("3.333"), Decimal("3.334")]


def test_replay_is_deterministic() -> None:
    first = replay_ledger(default_accounts(), default_events())
    second = replay_ledger(default_accounts(), default_events())
    assert first == second


def test_overdraft_fee_uses_closed_day_not_transient_intraday_negative() -> None:
    accounts = [
        {"account_id": "ACC-X", "currency": "AED", "opening_balance": Decimal("0.00")},
    ]
    events = [
        {
            "id": "X1",
            "booked_day": 1,
            "value_day": 1,
            "type": "DEBIT",
            "account_id": "ACC-X",
            "amount": Decimal("50.00"),
        },
        {
            "id": "X2",
            "booked_day": 1,
            "value_day": 1,
            "type": "CREDIT",
            "account_id": "ACC-X",
            "amount": Decimal("100.00"),
        },
    ]

    report = replay_ledger(accounts, events)

    assert report["daily_report"]["ACC-X"][1]["closing_balance"] == Decimal("50.00")
    assert report["daily_report"]["ACC-X"][1]["fee_assessed"] == Decimal("0.00")


def test_e7_checkpoint_exposes_pre_fee_historical_closes() -> None:
    report = replay_ledger(default_accounts(), default_events())

    checkpoint = next(
        item
        for item in report["checkpoints"]
        if item["kind"] == "PRE_FEE_RECONCILIATION" and item["event_id"] == "E7"
    )

    assert checkpoint["closes"][2] == Decimal("-370.00")
    assert checkpoint["closes"][3] == Decimal("30.00")
    assert checkpoint["closes"][4] == Decimal("-155.00")
    assert checkpoint["closes"][5] == Decimal("-155.00")
