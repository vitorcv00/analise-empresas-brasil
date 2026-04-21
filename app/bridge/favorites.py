"""Persistencia local de favoritos da aplicacao."""

from __future__ import annotations

import json
from pathlib import Path

from app.bridge.models import FavoriteTicker


class FavoritesRepository:
    """Gerencia favoritos persistidos em JSON local."""

    def __init__(self, storage_path: Path | None = None) -> None:
        """Inicializa o repositorio com o caminho de persistencia."""

        self.storage_path = storage_path or Path("data") / "_app" / "favorites.json"
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)

    def list_favorites(self) -> list[FavoriteTicker]:
        """Retorna a lista atual de favoritos."""

        if not self.storage_path.exists():
            return []
        payload = json.loads(self.storage_path.read_text(encoding="utf-8"))
        return [FavoriteTicker(ticker=item["ticker"]) for item in payload]

    def save_favorite(self, ticker: str) -> None:
        """Salva um ticker como favorito, evitando duplicidade."""

        normalized = ticker.upper().strip()
        favorites = self.list_favorites()
        if any(item.ticker == normalized for item in favorites):
            return
        favorites.append(FavoriteTicker(ticker=normalized))
        self._write(favorites)

    def remove_favorite(self, ticker: str) -> None:
        """Remove um ticker da lista de favoritos."""

        normalized = ticker.upper().strip()
        favorites = [item for item in self.list_favorites() if item.ticker != normalized]
        self._write(favorites)

    def _write(self, favorites: list[FavoriteTicker]) -> None:
        """Persiste a lista completa de favoritos."""

        payload = [{"ticker": item.ticker} for item in favorites]
        self.storage_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
