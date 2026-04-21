"""Persistencia local do snapshot macro por ticker."""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path

from src.schemas.collection import MacroData


class MacroSnapshotRepository:
    """Gerencia snapshots macro persistidos em JSON local."""

    def __init__(self, storage_path: Path | None = None) -> None:
        """Inicializa o repositorio com caminho de persistencia."""

        self.storage_path = storage_path or Path("data") / "_app" / "macro_snapshots.json"
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)

    def save_snapshot(self, ticker: str, macro_data: MacroData) -> None:
        """Persiste o snapshot macro do ticker informado."""

        payload = self._read()
        payload[ticker.upper().strip()] = {
            "updated_at": date.today().isoformat(),
            "macro": macro_data.model_dump(mode="json"),
        }
        self.storage_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    def get_snapshot(self, ticker: str) -> MacroData | None:
        """Retorna o snapshot macro atual do ticker, quando existir."""

        payload = self._read()
        snapshot = payload.get(ticker.upper().strip(), {})
        macro_payload = snapshot.get("macro")
        if not isinstance(macro_payload, dict):
            return None

        try:
            return MacroData.model_validate(macro_payload)
        except Exception:  # noqa: BLE001
            return None

    def _read(self) -> dict[str, dict]:
        """Le o estado persistido do disco."""

        if not self.storage_path.exists():
            return {}

        try:
            loaded = json.loads(self.storage_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return {}

        return loaded if isinstance(loaded, dict) else {}
