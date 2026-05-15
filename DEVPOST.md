# PayGuard Agent — Project Summary

## Inspiration

Fraud detection systems often return opaque risk scores without revealing the reasoning or tool usage behind decisions. For judges and operators, reproducible, explainable autonomy that shows PLAN → TOOL CALLS → MEMORY → DECISION is far more compelling than a black‑box score. PayGuard Agent was built to demonstrate clear, agentic behavior for transaction investigations that is easy to verify during a live demo.

## What it does

**Ask the agent directly — type transactions, get instant decisions.**

**Interactive Chat Mode** — Users type transaction details in the terminal, agent investigates and responds in real-time with full explainability.
- Type: `user_id: u_001, amount: 8000, merchant_id: m_202, country: US`
- Agent responds with: decision (ALLOW / ESCALATE / BLOCK), top reasons, explainability label (Likely Legit / Ambiguous / Fraud), and one-line summary.
- For each transaction it builds a simple investigation plan, calls local tools (user profile, velocity, merchant risk, amount anomaly, location mismatch), reads prior cases from local memory, scores the outcome.
- Loop for unlimited queries — ask as many questions as you want.

**Bonus: Batch Demo Mode** (optional for video) — Runs a deterministic demo suite of 7 realistic scenarios with full traces.

- Persists all investigations to `memory/cases.json` so repeated runs can show persistence effects.

## How we built it

- Language: Python 3.14 for the demo runner and tooling.
- Agent logic: `src/agent.py` implements deterministic planning, tool orchestration, scoring, and the explainability helper.
- Tools: small local functions in `src/tools.py` providing merchant risk, velocity counting, amount outlier checks, and simple location mismatch logic.
- Memory: `src/memory_store.py` persists case records to `memory/cases.json`.
- Web demo: a static single‑page site (`index.html`, `styles.css`, `script.js`) reads `demo_results.json` (synced from memory) to showcase explainability badges and summaries.
- Jac scaffold: `jac/payguard_agent.jac` contains the Jac design for porting the logic to Jaseci/Jac for a Jac‑first submission.

## Challenges we ran into

- Keeping the demo fully local and reproducible for judges while still demonstrating multi-step, agentic behavior (no paid APIs).
- Designing investigation logs that are informative but compact for display in a terminal and on a webpage.
- Balancing deterministic outputs (for video) with realistic variability and memory effects.

## Accomplishments that we're proud of

- A compact, judge-friendly demo that is runnable in minutes and produces transparent traces for every decision.
- Clear explainability layer (label + one-line summary) added to each investigation result to aid human review.
- A modern static demo site and one-line bootstrap installers so judges can reproduce the demo quickly.
- Jac scaffold included so the project can be migrated to a Jac‑primary runtime for the hackathon requirement.

## What we learned

- Small deterministic agents can be very effective for demo clarity: planable, testable, and easy to explain to judges.
- Memory and persistence are powerful storytelling tools for demonstrations — they let you show how the agent's posture adapts over time.
- Prioritizing reproducibility (reset mode, sync script, one-liners) drastically reduces demo fragility.

## What's next for PayGuard Agent

- Wire `jac/payguard_agent.jac` into a Jaseci runtime so the repo can run Jac as the primary execution path.
- Add a small local API to let the web UI run single synthetic transactions and show live agent traces.
- Improve the scoring model and add a merchant whitelist override and confidence-driven step‑up checks.
- Prepare a short Devpost writeup and a 3‑minute demo video script based on the deterministic scenario run.

---

### Quick run notes

**Primary: Interactive chat (ask the agent live)**
```powershell
python src/interactive.py
```
Then type: `user_id: u_001, amount: 8000, merchant_id: m_202, country: US`

**Optional: Batch demo mode (for recording videos)**
```powershell
python src/app.py --reset-memory
```

**Optional: View results on website**
```powershell
python scripts/sync_demo_results.py
python -m http.server 5500
# open http://localhost:5500/
```
