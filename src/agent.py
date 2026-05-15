from typing import Any

from memory_store import MemoryStore
from tools import (
    get_user_profile,
    is_amount_outlier,
    is_location_mismatch,
    merchant_risk_level,
    prior_fraud_rate,
    velocity_count,
)


class FraudInvestigationAgent:
    def __init__(
        self,
        users: dict[str, dict[str, Any]],
        merchant_risk: dict[str, dict[str, str]],
        memory: MemoryStore,
    ) -> None:
        self.users = users
        self.merchant_risk = merchant_risk
        self.memory = memory

    def build_plan(self, txn: dict[str, Any]) -> list[str]:
        # Simple deterministic planning so demo behavior is easy to explain.
        plan = ["user_profile", "velocity", "merchant_risk", "amount_outlier"]
        if txn.get("amount", 0) > 5000:
            plan.append("location_mismatch")
        return plan

    def investigate(self, txn: dict[str, Any]) -> dict[str, Any]:
        user_id = txn["user_id"]
        prior_cases = self.memory.get_cases_for_user(user_id)
        profile = get_user_profile(self.users, user_id)
        investigation_log: list[str] = []

        plan = self.build_plan(txn)
        investigation_log.append(f"PLAN: {', '.join(plan)}")
        observations: dict[str, Any] = {}

        if "user_profile" in plan:
            observations["account_age_days"] = profile["account_age_days"]
            investigation_log.append(
                f"TOOL user_profile -> account_age_days={observations['account_age_days']}, "
                f"avg_amount={profile['avg_amount']}, home_country={profile['home_country']}"
            )

        if "velocity" in plan:
            observations["velocity_60m"] = velocity_count(prior_cases, user_id, txn["timestamp"]) + 1
            investigation_log.append(f"TOOL velocity -> velocity_60m={observations['velocity_60m']}")

        if "merchant_risk" in plan:
            observations["merchant_risk"] = merchant_risk_level(self.merchant_risk, txn["merchant_id"])
            investigation_log.append(f"TOOL merchant_risk -> merchant_risk={observations['merchant_risk']}")

        if "amount_outlier" in plan:
            observations["amount_outlier"] = is_amount_outlier(txn["amount"], profile["avg_amount"])
            investigation_log.append(f"TOOL amount_outlier -> amount_outlier={observations['amount_outlier']}")

        if "location_mismatch" in plan:
            observations["location_mismatch"] = is_location_mismatch(profile["home_country"], txn["country"])
            investigation_log.append(f"TOOL location_mismatch -> location_mismatch={observations['location_mismatch']}")

        observations["prior_fraud_rate"] = round(prior_fraud_rate(prior_cases), 2)
        investigation_log.append(f"MEMORY prior_fraud_rate -> {observations['prior_fraud_rate']}")

        score, reasons = self.score(observations)
        decision = self.decide(score)
        investigation_log.append(f"DECISION score={score} -> {decision}")

        result = {
            "txn_id": txn["txn_id"],
            "user_id": user_id,
            "scenario": txn.get("scenario", "unspecified"),
            "plan": plan,
            "observations": observations,
            "risk_score": score,
            "decision": decision,
            "confidence": self.confidence(score),
            "reasons": reasons[:3],
            "investigation_log": investigation_log,
            "timestamp": txn["timestamp"],
        }

        self.memory.save_case(result)
        return result

    def score(self, obs: dict[str, Any]) -> tuple[int, list[str]]:
        score = 0
        reasons: list[str] = []

        if obs.get("velocity_60m", 0) >= 3:
            score += 30
            reasons.append("High transaction velocity in last 60 minutes")

        risk = obs.get("merchant_risk")
        if risk == "high":
            score += 30
            reasons.append("High-risk merchant")
        elif risk == "medium":
            score += 15
            reasons.append("Medium-risk merchant")

        if obs.get("amount_outlier"):
            score += 25
            reasons.append("Amount is high compared to user average")

        if obs.get("location_mismatch"):
            score += 20
            reasons.append("Transaction location differs from home country")

        if obs.get("account_age_days", 9999) < 30:
            score += 10
            reasons.append("New account has higher uncertainty")

        prior = obs.get("prior_fraud_rate", 0.0)
        if prior >= 0.5:
            score += 10
            reasons.append("User has risky prior outcomes")

        return min(score, 100), reasons

    @staticmethod
    def decide(score: int) -> str:
        if score >= 70:
            return "BLOCK"
        if score >= 40:
            return "ESCALATE"
        return "ALLOW"

    @staticmethod
    def confidence(score: int) -> float:
        # Convert risk score into a simple confidence metric for the demo UI/logs.
        return round(0.5 + (score / 200), 2)
