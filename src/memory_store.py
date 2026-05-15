import json
from pathlib import Path
from typing import Any


class MemoryStore:
    def __init__(self, path: str) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self.path.write_text("[]\n", encoding="utf-8")

    def _read(self) -> list[dict[str, Any]]:
        raw = self.path.read_text(encoding="utf-8").strip()
        if not raw:
            return []
        return json.loads(raw)

    def _write(self, rows: list[dict[str, Any]]) -> None:
        self.path.write_text(json.dumps(rows, indent=2), encoding="utf-8")

    def get_cases_for_user(self, user_id: str) -> list[dict[str, Any]]:
        return [row for row in self._read() if row.get("user_id") == user_id]

    def save_case(self, row: dict[str, Any]) -> None:
        rows = self._read()
        rows.append(row)
        self._write(rows)

    def clear(self) -> None:
        self._write([])

    def count(self) -> int:
        return len(self._read())
