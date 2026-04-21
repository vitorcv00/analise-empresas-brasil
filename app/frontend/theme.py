"""Tema visual compartilhado da interface desktop."""

from __future__ import annotations

from typing import Literal

from PySide6.QtGui import QFont
from PySide6.QtWidgets import QApplication


ThemeMode = Literal["light", "dark"]


LIGHT_STYLESHEET = """
QMainWindow {
    background-color: #f4f6f8;
}

QLabel {
    color: #203242;
}

QLabel#heroTitle {
    font-size: 30px;
    font-weight: 700;
    color: #0f4c5c;
}

QLabel#heroSubtitle {
    font-size: 14px;
    color: #4f6472;
}

QLabel#panelTitle {
    font-size: 16px;
    font-weight: 650;
}

QLabel#panelHint {
    font-size: 12px;
    color: #617381;
}

QLabel#statusLabel {
    font-size: 13px;
    color: #3b5568;
}

QLabel#statusLabel[state="loading"] {
    color: #0f4c5c;
    font-weight: 600;
}

QLabel#viewerTitle {
    font-size: 22px;
    font-weight: 700;
    color: #0f4c5c;
}

QLabel#viewerDocumentLabel {
    font-size: 13px;
    color: #3f5668;
}

QPushButton {
    border: 1px solid #c3cdd5;
    border-radius: 8px;
    padding: 8px 14px;
    background-color: #ffffff;
    color: #203242;
}

QPushButton:hover {
    background-color: #eef3f7;
}

QPushButton:disabled {
    background-color: #eff2f5;
    color: #96a4b0;
}

QPushButton#primaryButton {
    border: none;
    background-color: #0f4c5c;
    color: #ffffff;
    font-weight: 700;
}

QPushButton#primaryButton:hover {
    background-color: #0c3f4d;
}

QPushButton#themeToggleButton {
    min-width: 38px;
    max-width: 38px;
    min-height: 34px;
    max-height: 34px;
    padding: 0px;
    font-size: 21px;
}

QLineEdit {
    background-color: #ffffff;
    border: 1px solid #c2cdd6;
    border-radius: 8px;
    padding: 8px 10px;
    selection-background-color: #0f4c5c;
}

QFrame#sidePanel, QFrame#centerPanel, QFrame#pdfPanel, QFrame#viewerInfoBar {
    background-color: #ffffff;
    border: 1px solid #d7dee4;
    border-radius: 12px;
}

QFrame#macroCard {
    background-color: #ffffff;
    border: 1px solid #d7dee4;
    border-radius: 12px;
}

QLabel#macroCardTitle {
    font-size: 14px;
    font-weight: 700;
    color: #0f4c5c;
}

QLabel#macroCompactLine {
    font-size: 13px;
    color: #2c4354;
}

QListWidget#favoritesList, QListWidget#documentsList {
    border: 1px solid #cfd7df;
    border-radius: 10px;
    padding: 4px;
    background-color: #fefefe;
    alternate-background-color: #f4f7fa;
    outline: 0;
}

QListWidget#favoritesList::item, QListWidget#documentsList::item {
    border-radius: 6px;
    padding: 8px;
    background-color: transparent;
    color: #203242;
}

QListWidget#favoritesList::item:selected, QListWidget#documentsList::item:selected {
    background-color: #d9edf2;
    color: #0b3440;
    font-weight: 600;
}

QListWidget#favoritesList::item:selected:!active, QListWidget#documentsList::item:selected:!active {
    background-color: #d9edf2;
    color: #0b3440;
    font-weight: 600;
}
"""


DARK_STYLESHEET = """
QMainWindow {
    background-color: #141a22;
}

QLabel {
    color: #d8e3ee;
}

QLabel#heroTitle {
    font-size: 30px;
    font-weight: 700;
    color: #8ecfe0;
}

QLabel#heroSubtitle {
    font-size: 14px;
    color: #b0c1cf;
}

QLabel#panelTitle {
    font-size: 16px;
    font-weight: 650;
}

QLabel#panelHint {
    font-size: 12px;
    color: #9cb0be;
}

QLabel#statusLabel {
    font-size: 13px;
    color: #b7c8d7;
}

QLabel#statusLabel[state="loading"] {
    color: #8ecfe0;
    font-weight: 600;
}

QLabel#viewerTitle {
    font-size: 22px;
    font-weight: 700;
    color: #8ecfe0;
}

QLabel#viewerDocumentLabel {
    font-size: 13px;
    color: #b2c4d4;
}

QPushButton {
    border: 1px solid #3f4d5c;
    border-radius: 8px;
    padding: 8px 14px;
    background-color: #202a36;
    color: #dbe6f1;
}

QPushButton:hover {
    background-color: #283544;
}

QPushButton:disabled {
    background-color: #1b232e;
    color: #7f90a0;
}

QPushButton#primaryButton {
    border: none;
    background-color: #2f8aa3;
    color: #0e1a23;
    font-weight: 700;
}

QPushButton#primaryButton:hover {
    background-color: #3c9ab4;
}

QPushButton#themeToggleButton {
    min-width: 38px;
    max-width: 38px;
    min-height: 34px;
    max-height: 34px;
    padding: 0px;
    font-size: 21px;
}

QLineEdit {
    background-color: #1c2531;
    border: 1px solid #3f4f5f;
    border-radius: 8px;
    padding: 8px 10px;
    color: #dce7f2;
    selection-background-color: #2f8aa3;
}

QFrame#sidePanel, QFrame#centerPanel, QFrame#pdfPanel, QFrame#viewerInfoBar {
    background-color: #1b2430;
    border: 1px solid #324252;
    border-radius: 12px;
}

QFrame#macroCard {
    background-color: #1b2430;
    border: 1px solid #324252;
    border-radius: 12px;
}

QLabel#macroCardTitle {
    font-size: 14px;
    font-weight: 700;
    color: #8ecfe0;
}

QLabel#macroCompactLine {
    font-size: 13px;
    color: #cad8e6;
}

QListWidget#favoritesList, QListWidget#documentsList {
    border: 1px solid #3a4b5c;
    border-radius: 10px;
    padding: 4px;
    background-color: #18202b;
    alternate-background-color: #1f2a36;
    outline: 0;
    color: #dbe6f1;
}

QListWidget#favoritesList::item, QListWidget#documentsList::item {
    border-radius: 6px;
    padding: 8px;
    background-color: transparent;
    color: #dbe6f1;
}

QListWidget#favoritesList::item:selected, QListWidget#documentsList::item:selected {
    background-color: #2d4a5a;
    color: #dff4ff;
    font-weight: 600;
}

QListWidget#favoritesList::item:selected:!active, QListWidget#documentsList::item:selected:!active {
    background-color: #2d4a5a;
    color: #dff4ff;
    font-weight: 600;
}
"""


def apply_theme(app: QApplication, mode: ThemeMode = "light") -> None:
    """Aplica tema visual padrao ao app."""

    app.setStyleSheet(DARK_STYLESHEET if mode == "dark" else LIGHT_STYLESHEET)
    app.setFont(QFont("IBM Plex Sans", 10))
