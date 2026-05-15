#!/usr/bin/env bash
set -euo pipefail

if command -v python3 >/dev/null 2>&1; then
  PYTHON_CMD="python3"
elif command -v python >/dev/null 2>&1; then
  PYTHON_CMD="python"
else
  echo "Python is not installed or not in PATH. Install Python 3.10+ and retry."
  exit 1
fi

if [ ! -d ".venv" ]; then
  "$PYTHON_CMD" -m venv .venv
fi

. .venv/bin/activate
python -m pip install --upgrade pip

if [ -s requirements.txt ]; then
  python -m pip install -r requirements.txt
fi

echo "Install complete."
echo "Run demo: .venv/bin/python src/app.py --reset-memory"
echo "Run website: .venv/bin/python -m http.server 5500"
