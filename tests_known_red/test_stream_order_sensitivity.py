from ledger_core.core import replay_ledger
from ledger_core.fixtures import default_accounts, default_events


def test_authorization_is_order_invariant_but_this_intentionally_fails() -> None:
    baseline = replay_ledger(default_accounts(), default_events())

    reordered_events = default_events()
    event_lookup = {event["id"]: event for event in reordered_events}
    variant = [
        event_lookup["E1"],
        event_lookup["E2"],
        event_lookup["E3"],
        event_lookup["E4"],
        event_lookup["E5"],
        event_lookup["E6"],
        event_lookup["E7"],
        event_lookup["E9"],
        event_lookup["E8"],
        event_lookup["E10"],
    ]
    variant_report = replay_ledger(default_accounts(), variant)

    # This failure reveals that decisions are intentionally stream-order-sensitive.
    # Monetary value dates can be corrected later, but auth decisions are historical facts.
    assert (
        baseline["authorizations"]["Auth-B"]["status"]
        == variant_report["authorizations"]["Auth-B"]["status"]
    )
