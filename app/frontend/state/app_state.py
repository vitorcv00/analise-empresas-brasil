"""Estado simples da aplicacao desktop."""

from __future__ import annotations

from dataclasses import dataclass, field

from app.bridge.models import DocumentEntry, FavoriteTicker


@dataclass
class AppState:
    """Representa o estado principal usado entre as telas."""

    current_ticker: str = ""
    favorites: list[FavoriteTicker] = field(default_factory=list)
    documents: list[DocumentEntry] = field(default_factory=list)
    selected_document: DocumentEntry | None = None
