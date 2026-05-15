import argparse
import json
from pathlib import Path

from agent import FraudInvestigationAgent
from memory_store import MemoryStore


ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
MEMORY = ROOT / "memory" / "cases.json"


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run PayGuard agent scenarios")
    parser.add_argument(
        "--reset-memory",
        action="store_true",
        help="Clear saved cases before running scenarios for deterministic demo output",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    users = read_json(DATA / "users.json")
    merchant_risk = read_json(DATA / "merchant_risk.json")
    scenarios = read_json(DATA / "scenarios.json")

    memory = MemoryStore(str(MEMORY))
    if args.reset_memory:
        memory.clear()

    agent = FraudInvestigationAgent(users, merchant_risk, memory)

    print("PayGuard Agent MVP - Running scenarios\n")
    print(f"Starting memory case count: {memory.count()}\n")

    for txn in scenarios:
        result = agent.investigate(txn)
        print(f"Scenario: {result.get('scenario', 'unspecified')} | TXN: {result['txn_id']}")
        print("Investigation Trace:")
        for row in result.get("investigation_log", []):
            print(f"  - {row}")
        print(
            f"Final Decision: {result['decision']} "
            f"(risk_score={result['risk_score']}, confidence={result['confidence']})"
        )
        print("Structured Result:")
        print(json.dumps(result, indent=2))
        print("-" * 60)


if __name__ == "__main__":
    main()
