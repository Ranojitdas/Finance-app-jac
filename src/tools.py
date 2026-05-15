from datetime import datetime, timedelta
from typing import Any


def parse_ts(ts: str) -> datetime:
    return datetime.fromisoformat(ts)


def get_user_profile(users: dict[str, dict[str, Any]], user_id: str) -> dict[str, Any]:
    return users.get(user_id, {"home_country": "IN", "avg_amount": 1000, "account_age_days": 0})


def velocity_count(
    prior_cases: list[dict[str, Any]],
    user_id: str,
    current_ts: str,
    window_minutes: int = 60,
) -> int:
    now = parse_ts(current_ts)
    lower_bound = now - timedelta(minutes=window_minutes)
    count = 0
    for case in prior_cases:
        if case.get("user_id") != user_id:
            continue
        ts = case.get("timestamp")
        if not ts:
            continue
        case_ts = parse_ts(ts)
        if lower_bound <= case_ts <= now:
            count += 1
    return count


def is_location_mismatch(home_country: str, txn_country: str) -> bool:
    return home_country.upper() != txn_country.upper()


def merchant_risk_level(merchant_risk: dict[str, dict[str, str]], merchant_id: str) -> str:
    return merchant_risk.get(merchant_id, {}).get("risk_level", "medium")


def is_amount_outlier(amount: float, avg_amount: float, factor: float = 3.0) -> bool:
    baseline = max(avg_amount, 1)
    return amount > baseline * factor


def prior_fraud_rate(prior_cases: list[dict[str, Any]]) -> float:
    if not prior_cases:
        return 0.0
    risky = [c for c in prior_cases if c.get("decision") in {"BLOCK", "ESCALATE"}]
    return len(risky) / len(prior_cases)
