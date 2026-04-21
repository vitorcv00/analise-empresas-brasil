"""Ponte entre a UI desktop e o backend atual do coletor."""

from __future__ import annotations

from src.collector.service import BaseTickerCollectorService
from src.schemas.collection import CollectorResult


class BackendBridgeService:
    """Executa o coletor backend e devolve o resultado bruto para a UI."""

    def __init__(self, collector: BaseTickerCollectorService | None = None) -> None:
        """Inicializa a ponte com o coletor principal."""

        self.collector = collector or BaseTickerCollectorService()

    def run_collection(self, ticker: str) -> CollectorResult:
        """Executa a coleta completa para o ticker informado."""

        return self.collector.run(ticker.upper().strip())
