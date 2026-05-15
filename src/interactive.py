#!/usr/bin/env python
"""
Interactive PayGuard Agent — chat-style transaction investigation in terminal.
Users type transaction details, agent responds with decision and explanation.
"""

import json
import sys
from pathlib import Path
from datetime import datetime

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from agent import FraudInvestigationAgent
from memory_store import MemoryStore
from tools import get_user_profile

def load_data():
    """Load user profiles and merchant risk data."""
    root = Path(__file__).parent.parent
    
    with open(root / "data" / "users.json") as f:
        users = json.load(f)
    
    with open(root / "data" / "merchant_risk.json") as f:
        merchant_risk = json.load(f)
    
    return users, merchant_risk

def parse_transaction_input(user_input: str) -> dict | None:
    """Parse user input into a transaction dict.
    
    Expected format: user_id: u_001, amount: 5000, merchant_id: m_202, country: US
    """
    try:
        parts = [p.strip() for p in user_input.split(",")]
        txn = {}
        
        for part in parts:
            if ":" not in part:
                continue
            key, val = part.split(":", 1)
            key = key.strip()
            val = val.strip()
            txn[key] = val
        
        # Validate required fields
        required = ["user_id", "amount", "merchant_id", "country"]
        if not all(k in txn for k in required):
            print(f"❌ Missing fields. Required: {', '.join(required)}")
            return None
        
        # Convert amount to int
        try:
            txn["amount"] = int(txn["amount"])
        except ValueError:
            print("❌ Amount must be a number.")
            return None
        
        # Generate txn_id and timestamp
        txn["txn_id"] = f"interactive_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')[:20]}"
        txn["timestamp"] = datetime.now().isoformat()
        txn["scenario"] = "interactive_query"
        
        return txn
    
    except Exception as e:
        print(f"❌ Error parsing input: {e}")
        return None

def print_header():
    """Print welcome header."""
    print("\n" + "=" * 70)
    print("  PayGuard Agent — Interactive Transaction Investigation")
    print("=" * 70)
    print("\n💡 Type a transaction like this:")
    print("   user_id: u_001, amount: 5000, merchant_id: m_202, country: US")
    print("\n📋 Tip: View available users in data/users.json")
    print("        View merchant risk in data/merchant_risk.json")
    print("\n✅ Commands: 'quit' to exit, 'help' for format reminder\n")

def main():
    print_header()
    
    root = Path(__file__).parent.parent
    users, merchant_risk = load_data()
    memory = MemoryStore(root / "memory" / "cases.json")
    agent = FraudInvestigationAgent(users, merchant_risk, memory)
    
    prior_cases = len(memory._read())
    print(f"📚 Loaded {len(users)} users, {len(merchant_risk)} merchants, {prior_cases} prior cases\n")
    
    while True:
        try:
            user_input = input("🔍 Enter transaction (or 'quit'/'help'): ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() == "quit":
                print("\n👋 Goodbye!\n")
                break
            
            if user_input.lower() == "help":
                print("   Format: user_id: <id>, amount: <num>, merchant_id: <id>, country: <code>")
                print("   Example: user_id: u_001, amount: 5000, merchant_id: m_202, country: US\n")
                continue
            
            # Parse and investigate
            txn = parse_transaction_input(user_input)
            if txn is None:
                continue
            
            print("\n⏳ Investigating...\n")
            result = agent.investigate(txn)
            
            # Pretty-print result
            print("─" * 70)
            print(f"📍 Transaction ID: {result['txn_id']}")
            print(f"👤 User: {result['user_id']} | 💰 Amount: ${txn['amount']} | 🌍 Country: {txn['country']}")
            print(f"🏪 Merchant: {txn['merchant_id']} (risk: {result['observations'].get('merchant_risk', 'N/A')})")
            print("─" * 70)
            
            print(f"\n🎯 **DECISION: {result['decision']}** (score: {result['risk_score']}/100, confidence: {result['confidence']})")
            
            if result['reasons']:
                print(f"   Reasons: {', '.join(result['reasons'][:2])}")
            
            # Show explainability
            if "explainability" in result:
                exp = result["explainability"]
                print(f"\n💡 Label: {exp['label']}")
                print(f"   Summary: {exp['summary']}")
            
            print(f"\n📋 Investigation Log:")
            for line in result['investigation_log'][:5]:  # Show first 5 lines
                print(f"   • {line}")
            if len(result['investigation_log']) > 5:
                print(f"   ... (+{len(result['investigation_log']) - 5} more)")
            
            print("─" * 70 + "\n")
        
        except KeyboardInterrupt:
            print("\n\n👋 Interrupted. Goodbye!\n")
            break
        except Exception as e:
            print(f"❌ Error: {e}\n")

if __name__ == "__main__":
    main()
