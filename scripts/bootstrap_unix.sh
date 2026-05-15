#!/usr/bin/env bash
set -euo pipefail

REPO_URL="https://github.com/Ranojitdas/Finance-app-jac.git"
TARGET_DIR="Finance-app-jac"

if ! command -v git >/dev/null 2>&1; then
  echo "git is required but not found. Install git and retry."
  exit 1
fi

if [ ! -d "$TARGET_DIR" ]; then
  git clone "$REPO_URL" "$TARGET_DIR"
fi

cd "$TARGET_DIR"
bash scripts/install_unix.sh

echo ""
echo "Next:"
echo "cd $TARGET_DIR"
echo ".venv/bin/python src/app.py --reset-memory"
