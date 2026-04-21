"""Tela inicial do aplicativo desktop."""

from __future__ import annotations

from typing import Callable

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from app.bridge.models import FavoriteTicker
from app.frontend.widgets.favorites_list import FavoritesListWidget


class HomePage(QWidget):
    """Tela inicial com ticker, favoritos e acao de download."""

    def __init__(
        self,
        on_download_clicked: Callable[[str], None],
        on_favorite_selected: Callable[[str], None],
        on_exit_clicked: Callable[[], None],
        on_theme_toggle_clicked: Callable[[], None],
        is_dark_mode: bool = False,
    ) -> None:
        """Inicializa a tela com callbacks de acao."""

        super().__init__()
        self.on_download_clicked = on_download_clicked
        self.ticker_input = QLineEdit()
        self.download_button = QPushButton("Baixar")
        self.exit_button = QPushButton("Sair")
        self.theme_toggle_button = QPushButton()
        self.theme_toggle_button.setObjectName("themeToggleButton")
        self.status_label = QLabel("Digite um ticker para iniciar.")
        self.status_label.setObjectName("statusLabel")
        self.favorites_list = FavoritesListWidget(on_favorite_selected)
        self.title_label = QLabel("Painel de Analise de Empresas")
        self.subtitle_label = QLabel("Use um ticker para coletar e abrir os documentos mais recentes.")

        self._build_ui(on_exit_clicked, on_theme_toggle_clicked)
        self.set_theme_mode(is_dark_mode)

    def set_favorites(self, favorites: list[FavoriteTicker]) -> None:
        """Atualiza a lista de favoritos exibida."""

        self.favorites_list.set_favorites(favorites)

    def set_status(self, message: str) -> None:
        """Atualiza a mensagem de status da tela."""

        self.status_label.setText(message)

    def set_loading(self, is_loading: bool) -> None:
        """Ajusta a UI da tela conforme o estado de carregamento."""

        self.download_button.setEnabled(not is_loading)
        self.ticker_input.setEnabled(not is_loading)
        self.exit_button.setEnabled(not is_loading)
        self.download_button.setText("Baixando..." if is_loading else "Baixar")
        self.status_label.setProperty("state", "loading" if is_loading else "idle")
        self.status_label.style().unpolish(self.status_label)
        self.status_label.style().polish(self.status_label)

    def set_ticker(self, ticker: str) -> None:
        """Preenche o ticker atual no campo de entrada."""

        self.ticker_input.setText(ticker)

    def set_theme_mode(self, is_dark_mode: bool) -> None:
        """Atualiza icone do botao de alternancia de tema."""

        if is_dark_mode:
            self.theme_toggle_button.setText("☀")
            self.theme_toggle_button.setToolTip("Alternar para tema claro")
        else:
            self.theme_toggle_button.setText("☾")
            self.theme_toggle_button.setToolTip("Alternar para tema escuro")

    def _build_ui(
        self,
        on_exit_clicked: Callable[[], None],
        on_theme_toggle_clicked: Callable[[], None],
    ) -> None:
        """Monta o layout visual da tela inicial."""

        root = QVBoxLayout(self)
        root.setContentsMargins(24, 24, 24, 24)
        root.setSpacing(18)

        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.addWidget(self.theme_toggle_button)
        header_layout.addStretch()
        header_layout.addWidget(self.exit_button)

        body_layout = QHBoxLayout()
        body_layout.setSpacing(18)

        left_panel_layout = QVBoxLayout()
        left_panel_layout.setContentsMargins(16, 16, 16, 16)
        left_panel_layout.setSpacing(10)
        favorites_label = QLabel("Favoritos")
        favorites_label.setObjectName("panelTitle")
        favorites_hint = QLabel("Clique para abrir o cache local do ticker.")
        favorites_hint.setObjectName("panelHint")
        favorites_hint.setWordWrap(True)
        left_panel_layout.addWidget(favorites_label)
        left_panel_layout.addWidget(favorites_hint)
        left_panel_layout.addWidget(self.favorites_list, stretch=1)
        left_panel = QFrame()
        left_panel.setObjectName("sidePanel")
        left_panel.setLayout(left_panel_layout)
        left_panel.setMinimumWidth(240)
        left_panel.setMaximumWidth(300)

        center_layout = QVBoxLayout()
        center_layout.setContentsMargins(24, 24, 24, 24)
        center_layout.setSpacing(10)
        center_layout.addStretch()

        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setObjectName("heroTitle")
        self.subtitle_label.setAlignment(Qt.AlignCenter)
        self.subtitle_label.setObjectName("heroSubtitle")
        self.subtitle_label.setWordWrap(True)

        input_layout = QHBoxLayout()
        input_layout.setSpacing(10)
        self.ticker_input.setPlaceholderText("Digite um ticker, ex: BBAS3")
        self.ticker_input.setMinimumWidth(380)
        self.ticker_input.setMaxLength(8)
        input_layout.addWidget(self.ticker_input)
        input_layout.addWidget(self.download_button)
        self.download_button.setObjectName("primaryButton")

        center_layout.addWidget(self.title_label)
        center_layout.addWidget(self.subtitle_label)
        center_layout.addSpacing(16)
        center_layout.addLayout(input_layout)
        center_layout.addSpacing(12)
        center_layout.addWidget(self.status_label, alignment=Qt.AlignCenter)
        center_layout.addStretch()

        center_panel = QFrame()
        center_panel.setObjectName("centerPanel")
        center_panel.setLayout(center_layout)

        body_layout.addWidget(left_panel)
        body_layout.addWidget(center_panel)
        body_layout.setStretch(0, 2)
        body_layout.setStretch(1, 7)

        root.addLayout(header_layout)
        root.addLayout(body_layout, stretch=1)

        self.download_button.clicked.connect(self._handle_download)
        self.ticker_input.returnPressed.connect(self._handle_download)
        self.exit_button.clicked.connect(on_exit_clicked)
        self.theme_toggle_button.clicked.connect(on_theme_toggle_clicked)

    def _handle_download(self) -> None:
        """Aciona o fluxo de coleta para o ticker digitado."""

        self.on_download_clicked(self.ticker_input.text().strip())
