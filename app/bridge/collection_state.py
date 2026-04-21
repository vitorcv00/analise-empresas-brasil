"""Persistencia simples do estado de atualizacao por ticker."""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path


class CollectionStateRepository:
    """Guarda a ultima data de coleta bem-sucedida por ticker."""

    def __init__(self, storage_path: Path | None = None) -> None:
        """Inicializa o repositorio local do estado de coleta."""

        self.storage_path = storage_path or Path("data") / "_app" / "collection_state.json"
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)

    def is_fresh_today(self, ticker: str) -> bool:
        """Retorna se o ticker ja foi atualizado hoje."""

        payload = self._read()
        return payload.get(ticker.upper().strip()) == date.today().isoformat()

    def mark_updated_today(self, ticker: str) -> None:
        """Marca o ticker como atualizado hoje."""

        payload = self._read()
        payload[ticker.upper().strip()] = date.today().isoformat()
        self.storage_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    def _read(self) -> dict[str, str]:
        """Le o estado persistido do disco."""

        if not self.storage_path.exists():
            return {}
        return json.loads(self.storage_path.read_text(encoding="utf-8"))
