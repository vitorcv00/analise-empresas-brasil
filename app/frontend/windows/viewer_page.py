"""Tela de visualizacao de documentos em PDF."""

from __future__ import annotations

from typing import Callable

from PySide6.QtCore import QUrl
from PySide6.QtPdf import QPdfDocument
from PySide6.QtPdfWidgets import QPdfView
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from app.bridge.models import DocumentEntry
from app.frontend.widgets.documents_list import DocumentsListWidget
from app.frontend.widgets.macro_summary_panel import MacroSummaryPanel
from src.schemas.collection import MacroData


class ViewerPage(QWidget):
    """Tela que lista arquivos e exibe o PDF selecionado."""

    def __init__(
        self,
        on_back_clicked: Callable[[], None],
        on_save_favorite_clicked: Callable[[], None],
        on_update_clicked: Callable[[], None],
    ) -> None:
        """Inicializa a tela de visualizacao com callbacks."""

        super().__init__()
        self.title_label = QLabel("Visualizacao")
        self.title_label.setObjectName("viewerTitle")
        self.document_label = QLabel("Selecione um documento para visualizar.")
        self.document_label.setObjectName("viewerDocumentLabel")
        self.back_button = QPushButton("Voltar")
        self.update_button = QPushButton("Atualizar")
        self.favorite_button = QPushButton("Salvar como favorito")
        self.documents_list = DocumentsListWidget(self._open_document)
        self.macro_panel = MacroSummaryPanel()
        self.pdf_document = QPdfDocument(self)
        self.pdf_view = QPdfView(self)
        self.pdf_view.setDocument(self.pdf_document)
        self.pdf_view.setPageMode(QPdfView.PageMode.MultiPage)
        self.pdf_view.setZoomMode(QPdfView.ZoomMode.FitToWidth)

        self._build_ui(on_back_clicked, on_save_favorite_clicked, on_update_clicked)

    def set_ticker(self, ticker: str) -> None:
        """Atualiza o titulo da tela com o ticker selecionado."""

        self.title_label.setText(f"Visualizacao - {ticker}")

    def set_documents(self, documents: list[DocumentEntry]) -> None:
        """Atualiza a lista de documentos disponiveis."""

        self.documents_list.set_documents(documents)

    def set_macro_data(self, macro_data: MacroData | None) -> None:
        """Atualiza o painel de resumo macro do ticker atual."""

        self.macro_panel.set_data(macro_data)

    def open_first_document(self, documents: list[DocumentEntry]) -> None:
        """Abre automaticamente o primeiro documento disponivel."""

        if documents:
            self._open_document(documents[0])
        else:
            self.pdf_document.close()
            self.document_label.setText("Nenhum documento disponivel para este ticker.")

    def _build_ui(
        self,
        on_back_clicked: Callable[[], None],
        on_save_favorite_clicked: Callable[[], None],
        on_update_clicked: Callable[[], None],
    ) -> None:
        """Monta o layout visual da tela de visualizacao."""

        root = QVBoxLayout(self)
        root.setContentsMargins(24, 24, 24, 24)
        root.setSpacing(14)

        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.addWidget(self.title_label)
        header_layout.addStretch()
        header_layout.addWidget(self.update_button)
        header_layout.addWidget(self.favorite_button)
        header_layout.addWidget(self.back_button)

        info_bar = QFrame()
        info_bar.setObjectName("viewerInfoBar")
        info_layout = QHBoxLayout(info_bar)
        info_layout.setContentsMargins(12, 8, 12, 8)
        info_layout.addWidget(self.document_label)

        body_layout = QHBoxLayout()
        body_layout.setSpacing(14)
        body_layout.addWidget(self.documents_list, stretch=2)

        pdf_panel = QFrame()
        pdf_panel.setObjectName("pdfPanel")
        pdf_layout = QVBoxLayout(pdf_panel)
        pdf_layout.setContentsMargins(10, 10, 10, 10)
        pdf_layout.addWidget(self.pdf_view)
        body_layout.addWidget(pdf_panel, stretch=6)

        root.addLayout(header_layout)
        root.addWidget(info_bar)
        root.addWidget(self.macro_panel)
        root.addLayout(body_layout)

        self.back_button.clicked.connect(on_back_clicked)
        self.favorite_button.clicked.connect(on_save_favorite_clicked)
        self.update_button.clicked.connect(on_update_clicked)

    def _open_document(self, document: DocumentEntry) -> None:
        """Abre o documento selecionado no painel PDF."""

        status = self.pdf_document.load(QUrl.fromLocalFile(document.path).toLocalFile())
        if status != QPdfDocument.Error.None_:
            QMessageBox.warning(self, "Erro", f"Nao foi possivel abrir o PDF: {document.name}")
            self.document_label.setText(f"Erro ao abrir: {document.name}")
            return

        self.document_label.setText(document.name)
