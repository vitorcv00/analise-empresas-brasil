"""Widget de exibicao dos tickers favoritos."""

from __future__ import annotations

from typing import Callable

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QListWidget, QListWidgetItem

from app.bridge.models import FavoriteTicker


class FavoritesListWidget(QListWidget):
    """Lista clicavel de tickers favoritos."""

    def __init__(self, on_selected: Callable[[str], None]) -> None:
        """Inicializa o widget com callback de selecao."""

        super().__init__()
        self.on_selected = on_selected
        self.setObjectName("favoritesList")
        self.setAlternatingRowColors(True)
        self.itemClicked.connect(self._handle_click)

    def set_favorites(self, favorites: list[FavoriteTicker]) -> None:
        """Atualiza a lista exibida de favoritos."""

        self.clear()
        if not favorites:
            empty_item = QListWidgetItem("Sem favoritos salvos")
            empty_item.setFlags(Qt.ItemFlag.NoItemFlags)
            self.addItem(empty_item)
            return

        for favorite in favorites:
            self.addItem(QListWidgetItem(favorite.ticker))

    def _handle_click(self, item: QListWidgetItem) -> None:
        """Propaga o ticker selecionado para a tela principal."""

        self.on_selected(item.text())
