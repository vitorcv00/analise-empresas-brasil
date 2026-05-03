"""Servico de atualizacao diaria dos precos de commodities."""

from __future__ import annotations

from datetime import datetime, time
from zoneinfo import ZoneInfo

import yfinance as yf

from app.bridge.commodities_repository import CommoditiesRepository


class CommoditiesService:
    """Atualiza e fornece precos de petroleo, ouro e prata com cache local."""

    UPDATE_TZ = ZoneInfo("America/Sao_Paulo")
    UPDATE_TIME = time(hour=8, minute=0)
    SYMBOLS = {
        "petroleo": "BZ=F",
        "ouro": "GC=F",
        "prata": "SI=F",
    }

    def __init__(self, repository: CommoditiesRepository | None = None) -> None:
        """Inicializa com repositorio de snapshot local."""

        self.repository = repository or CommoditiesRepository()

    def ensure_daily_update(self) -> dict:
        """Atualiza no maximo uma vez ao dia apos 08:00 (UTC-3)."""

        snapshot = self.repository.load()
        now = datetime.now(self.UPDATE_TZ)
        trading_date = now.date().isoformat()

        if not self._should_update(snapshot, now, trading_date):
            return snapshot

        prices = self._fetch_prices()
        updated_payload = {
            "trading_date": trading_date,
            "updated_at": now.isoformat(),
            "timezone": "America/Sao_Paulo",
            "prices": prices,
        }
        self.repository.save(updated_payload)
        return updated_payload

    def get_cached_snapshot(self) -> dict:
        """Retorna o snapshot atual sem forcar atualizacao remota."""

        return self.repository.load()

    def _should_update(self, snapshot: dict, now: datetime, trading_date: str) -> bool:
        """Aplica regra de atualizacao diaria apos 08:00."""

        if now.time() < self.UPDATE_TIME:
            return False
        return snapshot.get("trading_date") != trading_date

    def _fetch_prices(self) -> dict[str, dict[str, str | float | None]]:
        """Busca o preco atual dos simbolos configurados via yfinance."""

        prices: dict[str, dict[str, str | float | None]] = {}
        for name, symbol in self.SYMBOLS.items():
            ticker = yf.Ticker(symbol)
            history = ticker.history(period="2d", interval="1d")
            if history.empty:
                prices[name] = {
                    "symbol": symbol,
                    "value": None,
                    "currency": None,
                    "unit": None,
                    "reference": None,
                }
                continue

            latest_row = history.iloc[-1]
            latest_reference = history.index[-1]
            prices[name] = {
                "symbol": symbol,
                "value": float(latest_row["Close"]) if latest_row.get("Close") is not None else None,
                "currency": "USD",
                "unit": self._unit_for(name),
                "reference": latest_reference.strftime("%Y-%m-%d"),
            }
        return prices

    @staticmethod
    def _unit_for(name: str) -> str:
        """Retorna unidade de exibicao por commodity."""

        if name == "petroleo":
            return "USD/barril"
        if name == "ouro":
            return "USD/onca"
        return "USD/onca"
