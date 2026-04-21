"""Widget de exibicao dos documentos disponiveis para visualizacao."""

from __future__ import annotations

from typing import Callable

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QListWidget, QListWidgetItem

from app.bridge.models import DocumentEntry


class DocumentsListWidget(QListWidget):
    """Lista clicavel de documentos gerados pelo backend."""

    def __init__(self, on_selected: Callable[[DocumentEntry], None]) -> None:
        """Inicializa o widget com callback de selecao."""

        super().__init__()
        self.on_selected = on_selected
        self._documents: list[DocumentEntry] = []
        self.setObjectName("documentsList")
        self.setAlternatingRowColors(True)
        self.itemClicked.connect(self._handle_click)

    def set_documents(self, documents: list[DocumentEntry]) -> None:
        """Atualiza os documentos exibidos no painel lateral."""

        self.clear()
        self._documents = documents
        if not documents:
            empty_item = QListWidgetItem("Nenhum documento encontrado")
            empty_item.setFlags(Qt.ItemFlag.NoItemFlags)
            self.addItem(empty_item)
            return

        for document in documents:
            self.addItem(QListWidgetItem(document.name))

        self.setCurrentRow(0)

    def _handle_click(self, item: QListWidgetItem) -> None:
        """Propaga o documento selecionado para a tela de visualizacao."""

        index = self.row(item)
        if 0 <= index < len(self._documents):
            self.on_selected(self._documents[index])
