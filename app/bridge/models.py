"""Modelos simples usados pela ponte entre UI e backend."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class FavoriteTicker:
    """Representa um ticker salvo como favorito."""

    ticker: str


@dataclass(slots=True)
class DocumentEntry:
    """Representa um arquivo exibivel dentro do app."""

    name: str
    path: str
    category: str
