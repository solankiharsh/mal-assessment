from .core import replay_ledger
from .fixtures import default_accounts, default_events
from .reporting import render_report


def main() -> None:
    report = replay_ledger(default_accounts(), default_events())
    print(render_report(report))


if __name__ == "__main__":
    main()
