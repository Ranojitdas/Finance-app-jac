# PayGuard Agent MVP (JacHacks)

A practical, hackathon-friendly fraud investigation agent inspired by PayGuard.

Repository: https://github.com/Ranojitdas/Finance-app-jac

This MVP is intentionally simple and fully local:
- No external APIs required
- Deterministic behavior for stable demos
- Persistent memory across runs using a local JSON file

## What it demonstrates
- Planning: chooses checks per transaction
- Tool use: calls local risk tools
- Memory: reuses prior user investigation outcomes
- Multi-step reasoning: combines signals into a decision
- Investigation logs: shows `plan -> tool calls -> decision`

## Decisions
- `ALLOW`
- `ESCALATE`
- `BLOCK`

## Project structure
- `src/app.py` - scenario runner
- `src/agent.py` - planning, scoring, decision logic
- `src/tools.py` - risk tools
- `src/memory_store.py` - persistent memory
- `data/scenarios.json` - demo transactions
- `memory/cases.json` - stored investigation results
- `jac/payguard_agent.jac` - Jac core logic port (planning, tools, scoring, decision)

## Run locally
From project root:

**Ask the agent — interactive chat mode:**
```bash
python src/interactive.py
```

Type a transaction:
```
user_id: u_001, amount: 8000, merchant_id: m_202, country: US
```

Agent will investigate and respond instantly with decision + explainability.

**Optional: Batch demo mode (for video):**
```bash
python src/app.py --reset-memory
```

If `python` does not work on the system, try:

```bash
py src/interactive.py
```

## Install on any system
One-command setup from anywhere (clones repo + installs):

Windows (PowerShell):

```powershell
powershell -ExecutionPolicy Bypass -Command "iwr https://raw.githubusercontent.com/Ranojitdas/Finance-app-jac/main/scripts/bootstrap_windows.ps1 -UseBasicParsing | iex"
```

Linux / macOS:

```bash
curl -fsSL https://raw.githubusercontent.com/Ranojitdas/Finance-app-jac/main/scripts/bootstrap_unix.sh | bash
```

If you already cloned the repo, run one install script from project root.

Windows (PowerShell):

```powershell
powershell -ExecutionPolicy Bypass -File scripts/install_windows.ps1
```

Linux / macOS:

```bash
bash scripts/install_unix.sh
```

After install, run with project virtual environment:

Windows:

```powershell
.\.venv\Scripts\python.exe src/app.py --reset-memory
```

Linux / macOS:

```bash
.venv/bin/python src/app.py --reset-memory
```

## Judge quick start (portable)
From project root:

**Ask the agent your own questions:**
```bash
python src/interactive.py
```

Type transactions. Agent investigates and responds instantly.

**Or run the automated demo (no interaction):**
```bash
python src/app.py --reset-memory
```

Expected behavior:
- Prints 7 investigation scenarios
- Shows trace logs in the format: PLAN -> TOOL -> MEMORY -> DECISION
- Outputs ALLOW, ESCALATE, or BLOCK with reasons
- No paid API keys required

## Open the project webpage
From project root, run a quick static server:

```bash
python -m http.server 5500
```

Then open:

```text
http://localhost:5500/web/
```

## Included realistic scenarios
- Baseline legit purchase
- Account takeover style high-value cross-border attempt
- New account ambiguous case (escalate)
- False-positive style travel-like pattern
- Small mule pattern with rapid repeated transactions

## How to demo in 3 minutes
1. Run `python src/app.py`
2. Show one low-risk allow case
3. Show one high-risk block case
4. Show one ambiguous escalate case
5. Show investigation trace logs in terminal output
6. Open `memory/cases.json` to show memory persistence

## Hackathon note
Python currently acts as a local runner for deterministic demos.
Jac core logic is ported in `jac/payguard_agent.jac`; wire this into your Jaseci runtime entrypoint during hackathon coding so Jac is the primary execution path for final submission.
