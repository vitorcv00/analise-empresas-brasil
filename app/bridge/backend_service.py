"""Ponte entre a UI desktop e o backend atual do coletor."""

from __future__ import annotations

from app.bridge.commodities_service import CommoditiesService
from src.collector.service import BaseTickerCollectorService
from src.schemas.collection import CollectorResult


class BackendBridgeService:
    """Executa o coletor backend e devolve o resultado bruto para a UI."""

    def __init__(self, collector: BaseTickerCollectorService | None = None) -> None:
        """Inicializa a ponte com o coletor principal."""

        self.collector = collector or BaseTickerCollectorService()
        self.commodities_service = CommoditiesService()
        try:
            self.commodities_service.ensure_daily_update()
        except Exception:  # noqa: BLE001
            # Falha de rede nao deve impedir o app de abrir.
            pass

    def run_collection(self, ticker: str) -> CollectorResult:
        """Executa a coleta completa para o ticker informado."""

        return self.collector.run(ticker.upper().strip())

    def get_commodities_snapshot(self) -> dict:
        """Retorna o snapshot de commodities em cache local."""

        return self.commodities_service.get_cached_snapshot()
