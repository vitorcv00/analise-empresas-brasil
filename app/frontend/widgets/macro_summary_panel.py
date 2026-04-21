"""Painel macro compacto exibido na tela de visualizacao."""

from __future__ import annotations

from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QWidget

from src.schemas.collection import MacroData, ValueSnapshot


def _format_value(snapshot: ValueSnapshot) -> str:
    """Formata o valor principal de um snapshot macro."""

    if snapshot.valor is None:
        return "-"
    return str(snapshot.valor)


class MacroSummaryPanel(QWidget):
    """Renderiza dados macro em formato compacto horizontal."""

    def __init__(self) -> None:
        """Inicializa a estrutura visual do painel."""

        super().__init__()
        self._inflation_line = QLabel("")
        self._rates_line = QLabel("")
        self._build_ui()
        self.clear_data()

    def clear_data(self) -> None:
        """Limpa os valores exibidos no painel."""

        self._inflation_line.setText("Mês: - | Meta: - | Projeção: -")
        self._rates_line.setText("Atual: - | Projeção: -")

    def set_data(self, macro_data: MacroData | None) -> None:
        """Preenche o painel com dados macro."""

        if macro_data is None:
            self.clear_data()
            return

        self._inflation_line.setText(
            "Mês: "
            f"{_format_value(macro_data.ipca_atual)}"
            " | Meta: "
            f"{_format_value(macro_data.ipca_meta)}"
            " | Projeção: "
            f"{_format_value(macro_data.ipca_projecao)}"
        )
        self._rates_line.setText(
            "Atual: "
            f"{_format_value(macro_data.selic_atual)}"
            " | Projeção: "
            f"{_format_value(macro_data.selic_projecao)}"
        )

    def _build_ui(self) -> None:
        """Monta o layout horizontal compacto do painel macro."""

        root = QHBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(14)

        inflation_card = self._create_card("Inflação", self._inflation_line)
        rates_card = self._create_card("Juros", self._rates_line)
        root.addWidget(inflation_card, stretch=1)
        root.addWidget(rates_card, stretch=1)

    def _create_card(self, title: str, line_label: QLabel) -> QFrame:
        """Cria um card visual com titulo e linha unica de metricas."""

        card = QFrame()
        card.setObjectName("macroCard")
        layout = QHBoxLayout(card)
        layout.setContentsMargins(12, 8, 12, 8)
        layout.setSpacing(10)

        title_label = QLabel(title)
        title_label.setObjectName("macroCardTitle")
        line_label.setObjectName("macroCompactLine")
        layout.addWidget(title_label)
        layout.addWidget(line_label, stretch=1)

        return card
