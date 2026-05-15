import shutil
from pathlib import Path

root = Path(__file__).resolve().parents[1]
src = root / "memory" / "cases.json"
dst = root / "demo_results.json"

if not src.exists():
    print(f"Source not found: {src}")
else:
    shutil.copy2(src, dst)
    print(f"Copied {src} -> {dst}")
