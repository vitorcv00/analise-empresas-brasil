"""Persistencia local dos precos de commodities."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class CommoditiesRepository:
    """Le e grava o snapshot de commodities em arquivo JSON."""

    def __init__(self, storage_path: Path | None = None) -> None:
        """Inicializa o repositorio com caminho de persistencia."""

        self.storage_path = storage_path or Path("data") / "_app" / "commodities_snapshot.json"
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)

    def save(self, payload: dict[str, Any]) -> None:
        """Persiste o payload completo no disco."""

        self.storage_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    def load(self) -> dict[str, Any]:
        """Retorna o payload salvo, quando valido."""

        if not self.storage_path.exists():
            return {}

        try:
            loaded = json.loads(self.storage_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return {}

        return loaded if isinstance(loaded, dict) else {}
