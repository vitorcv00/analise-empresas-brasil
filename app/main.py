"""Ponto de entrada da aplicacao desktop em PySide6."""

from __future__ import annotations

import sys

from PySide6.QtWidgets import QApplication

from app.frontend.theme import apply_theme
from app.frontend.windows.main_window import MainWindow


def main() -> int:
    """Inicializa a aplicacao desktop."""

    app = QApplication(sys.argv)
    apply_theme(app)
    window = MainWindow()
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
