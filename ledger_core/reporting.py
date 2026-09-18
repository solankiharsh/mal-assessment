from __future__ import annotations

import json
from decimal import Decimal

from .core import WINDOW_DAYS


def render_report(report: dict) -> str:
    first_day = min(WINDOW_DAYS)
    last_day = max(WINDOW_DAYS)
    lines = []
    lines.append(f"Ledger Replay Report (Day {first_day} to Day {last_day})")
    for account_id, days in report["daily_report"].items():
        lines.append(f"\n{account_id}")
        for day in WINDOW_DAYS:
            row = days[day]
            auth_states = ", ".join(f"{auth['auth_id']}:{auth['status']}" for auth in row["authorizations"]) or "-"
            error_codes = ", ".join(error["code"] for error in row["errors"]) or "-"
            lines.append(
                " ".join(
                    [
                        f"Day {day}",
                        f"close={row['closing_balance']}",
                        f"fee={row['fee_assessed']}",
                        f"auth={auth_states}",
                        f"errors={error_codes}",
                        f"interest={row['daily_interest']}",
                    ]
                )
            )
    return "\n".join(lines)


def _json_default(value: object) -> str:
    if isinstance(value, Decimal):
        return format(value, "f")
    raise TypeError(f"Unserializable value: {value!r}")


def render_report_json(report: dict) -> str:
    return json.dumps(report, indent=2, sort_keys=True, default=_json_default)
