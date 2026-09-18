from decimal import Decimal


def default_accounts() -> list[dict]:
    return [
        {"account_id": "ACC-001", "currency": "AED", "opening_balance": Decimal("0.00")},
        {"account_id": "ACC-002", "currency": "BHD", "opening_balance": Decimal("0.000")},
    ]


def default_events() -> list[dict]:
    return [
        {
            "id": "E1",
            "booked_day": 1,
            "value_day": 1,
            "type": "CREDIT",
            "account_id": "ACC-001",
            "amount": Decimal("1200.00"),
        },
        {
            "id": "E2",
            "booked_day": 1,
            "value_day": 1,
            "type": "DEBIT",
            "account_id": "ACC-001",
            "amount": Decimal("950.00"),
        },
        {
            "id": "E3",
            "booked_day": 2,
            "value_day": 2,
            "type": "AUTHORIZATION",
            "account_id": "ACC-001",
            "auth_id": "Auth-A",
            "amount": Decimal("200.00"),
        },
        {
            "id": "E4",
            "booked_day": 3,
            "value_day": 3,
            "type": "CREDIT",
            "account_id": "ACC-001",
            "amount": Decimal("400.00"),
        },
        {
            "id": "E5",
            "booked_day": 4,
            "value_day": 4,
            "type": "SETTLEMENT",
            "account_id": "ACC-001",
            "auth_id": "Auth-A",
            "amount": Decimal("185.00"),
        },
        {
            "id": "E6",
            "booked_day": 4,
            "value_day": 4,
            "type": "SETTLEMENT",
            "account_id": "ACC-001",
            "auth_id": "Auth-Z",
            "amount": Decimal("180.00"),
        },
        {
            "id": "E7",
            "booked_day": 5,
            "value_day": 2,
            "type": "DEBIT",
            "account_id": "ACC-001",
            "amount": Decimal("620.00"),
        },
        {
            "id": "E8",
            "booked_day": 5,
            "value_day": 5,
            "type": "AUTHORIZATION",
            "account_id": "ACC-001",
            "auth_id": "Auth-B",
            "amount": Decimal("90.00"),
        },
        {
            "id": "E9",
            "booked_day": 6,
            "value_day": 2,
            "type": "REVERSAL",
            "account_id": "ACC-001",
            "reversal_of_event_id": "E7",
        },
        {
            "id": "E10",
            "booked_day": 5,
            "value_day": 5,
            "type": "CREDIT_INSTALMENTS",
            "account_id": "ACC-002",
            "amount": Decimal("10.000"),
            "instalments": 3,
        },
    ]
