"""Janela principal da aplicacao desktop."""

from __future__ import annotations

from PySide6.QtCore import QObject, QThread, Signal
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox, QStackedWidget

from app.bridge.backend_service import BackendBridgeService
from app.bridge.collection_state import CollectionStateRepository
from app.bridge.document_service import DocumentService
from app.bridge.favorites import FavoritesRepository
from app.bridge.macro_snapshot_repository import MacroSnapshotRepository
from app.frontend.state.app_state import AppState
from app.frontend.theme import apply_theme
from app.frontend.windows.home_page import HomePage
from app.frontend.windows.viewer_page import ViewerPage
from src.schemas.collection import CollectorResult


class _CollectionWorker(QObject):
    """Worker que executa a coleta fora da thread principal."""

    finished = Signal(object)
    failed = Signal(str)

    def __init__(self, service: BackendBridgeService, ticker: str) -> None:
        """Inicializa o worker com ticker e service bridge."""

        super().__init__()
        self.service = service
        self.ticker = ticker

    def run(self) -> None:
        """Executa a coleta e emite o resultado para a UI."""

        try:
            result = self.service.run_collection(self.ticker)
        except Exception as exc:  # noqa: BLE001
            self.failed.emit(str(exc))
            return
        self.finished.emit(result)


class MainWindow(QMainWindow):
    """Janela principal com navegacao entre tela inicial e visualizacao."""

    def __init__(self) -> None:
        """Inicializa estado, servicos e interface principal."""

        super().__init__()
        self.setWindowTitle("Analise de Empresas")
        self.resize(1200, 800)
        self.is_dark_mode = False

        self.state = AppState()
        self.backend_service = BackendBridgeService()
        self.document_service = DocumentService()
        self.favorites_repository = FavoritesRepository()
        self.collection_state_repository = CollectionStateRepository()
        self.macro_snapshot_repository = MacroSnapshotRepository()

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.home_page = HomePage(
            on_download_clicked=self._start_collection,
            on_favorite_selected=self._load_ticker_from_favorite,
            on_exit_clicked=self.close,
            on_theme_toggle_clicked=self._toggle_theme_mode,
            is_dark_mode=self.is_dark_mode,
        )
        self.viewer_page = ViewerPage(
            on_back_clicked=self._go_home,
            on_save_favorite_clicked=self._save_current_ticker_as_favorite,
            on_update_clicked=self._force_refresh_current_ticker,
        )

        self.stack.addWidget(self.home_page)
        self.stack.addWidget(self.viewer_page)

        self._load_favorites()

    def _toggle_theme_mode(self) -> None:
        """Alterna entre tema claro e escuro no app inteiro."""

        self.is_dark_mode = not self.is_dark_mode
        app = QApplication.instance()
        if app is not None:
            apply_theme(app, mode="dark" if self.is_dark_mode else "light")
        self.home_page.set_theme_mode(self.is_dark_mode)

    def _load_favorites(self) -> None:
        """Carrega favoritos do armazenamento local para a tela inicial."""

        self.state.favorites = self.favorites_repository.list_favorites()
        self.home_page.set_favorites(self.state.favorites)

    def _start_collection(self, ticker: str, force_refresh: bool = False) -> None:
        """Inicia o fluxo de coleta assincrona do ticker informado."""

        normalized = ticker.upper().strip()
        if not normalized:
            QMessageBox.warning(self, "Ticker invalido", "Digite um ticker antes de continuar.")
            return

        self.state.current_ticker = normalized

        if not force_refresh and self.collection_state_repository.is_fresh_today(normalized):
            if self._open_existing_documents(normalized, f"Arquivos de {normalized} ja estao atualizados hoje."):
                return

        self.home_page.set_loading(True)
        self.home_page.set_status(f"Baixando arquivos de {normalized}...")

        self.worker_thread = QThread(self)
        self.worker = _CollectionWorker(self.backend_service, normalized)
        self.worker.moveToThread(self.worker_thread)
        self.worker_thread.started.connect(self.worker.run)
        self.worker.finished.connect(self._handle_collection_success)
        self.worker.failed.connect(self._handle_collection_error)
        self.worker.finished.connect(self.worker_thread.quit)
        self.worker.failed.connect(self.worker_thread.quit)
        self.worker_thread.finished.connect(self.worker.deleteLater)
        self.worker_thread.finished.connect(self.worker_thread.deleteLater)
        self.worker_thread.start()

    def _handle_collection_success(self, result: CollectorResult) -> None:
        """Atualiza a UI quando a coleta termina com sucesso."""

        ticker = result.report.ticker
        self.macro_snapshot_repository.save_snapshot(ticker, result.report.macro)
        self.collection_state_repository.mark_updated_today(ticker)
        self.home_page.set_loading(False)
        self.home_page.set_status(f"Coleta concluida para {ticker}.")
        self._open_existing_documents(ticker, f"Coleta concluida para {ticker}.")

    def _handle_collection_error(self, message: str) -> None:
        """Exibe erro de coleta e restaura a tela inicial."""

        self.home_page.set_loading(False)
        self.home_page.set_status("Falha na coleta.")
        QMessageBox.critical(self, "Erro na coleta", message)

    def _load_ticker_from_favorite(self, ticker: str) -> None:
        """Abre os arquivos existentes do ticker favorito ou coleta se necessario."""

        self.home_page.set_ticker(ticker)
        self.state.current_ticker = ticker.upper().strip()
        if not self._open_existing_documents(ticker, f"Visualizando arquivos salvos de {ticker}."):
            self._start_collection(ticker)

    def _save_current_ticker_as_favorite(self) -> None:
        """Salva o ticker atual como favorito."""

        if not self.state.current_ticker:
            return
        self.favorites_repository.save_favorite(self.state.current_ticker)
        self._load_favorites()
        QMessageBox.information(self, "Favorito salvo", f"{self.state.current_ticker} foi salvo.")

    def _force_refresh_current_ticker(self) -> None:
        """Executa atualizacao manual do ticker atual."""

        if not self.state.current_ticker:
            return
        self.stack.setCurrentWidget(self.home_page)
        self._start_collection(self.state.current_ticker, force_refresh=True)

    def _go_home(self) -> None:
        """Volta para a tela inicial."""

        self.stack.setCurrentWidget(self.home_page)

    def _open_existing_documents(self, ticker: str, status_message: str) -> bool:
        """Abre documentos ja existentes sem rodar nova coleta."""

        documents = self.document_service.list_documents_for_ticker(ticker)
        macro_document = self.document_service.get_shared_macro_document()
        if macro_document and all(doc.path != macro_document.path for doc in documents):
            documents.insert(0, macro_document)
        if not documents:
            return False

        self.state.documents = documents
        self.state.selected_document = documents[0]
        self.home_page.set_loading(False)
        self.home_page.set_status(status_message)
        self.viewer_page.set_ticker(ticker)
        self.viewer_page.set_macro_data(self.macro_snapshot_repository.get_snapshot(ticker))
        self.viewer_page.set_documents(documents)
        self.viewer_page.open_first_document(documents)
        self.stack.setCurrentWidget(self.viewer_page)
        return True
