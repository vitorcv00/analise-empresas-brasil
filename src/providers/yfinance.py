"""Integracao auxiliar com yfinance usada para metadados basicos."""

from __future__ import annotations

from typing import Any

import yfinance as yf

from src.config.settings import settings
from src.providers.base import BaseProvider
from src.schemas.collection import CollectionItem
from src.schemas.company import CompanyProfile


class YFinanceProvider(BaseProvider):
    """Provider auxiliar para dados de mercado e perfil de empresa."""

    def supports(self, item_name: str) -> bool:
        """Informa se o item pode ser coletado via yfinance."""

        return item_name in {"company_profile", "cotacao_historica", "dividendos", "ibov"}

    @staticmethod
    def _symbol_for(company: CompanyProfile, item_name: str) -> str:
        """Monta o simbolo usado pelo Yahoo Finance."""

        if item_name == "ibov":
            return "^BVSP"
        return f"{company.ticker}.SA"

    def collect(self, company: CompanyProfile, item: CollectionItem) -> dict[str, Any]:
        """Coleta perfil basico, dividendos ou historico de precos."""

        symbol = self._symbol_for(company, item.item)
        ticker = yf.Ticker(symbol)

        if item.item == "company_profile":
            info: Any = ticker.info
            payload = {
                "symbol": symbol,
                "shortName": info.get("shortName"),
                "longName": info.get("longName"),
                "sector": info.get("sector"),
                "industry": info.get("industry"),
                "marketCap": info.get("marketCap"),
                "website": info.get("website"),
            }
            return {
                "fonte_utilizada": "yfinance",
                "resumo": "Perfil basico coletado via yfinance.",
                "dados": payload,
            }

        if item.item == "dividendos":
            dividends = ticker.dividends.tail(20)
            payload = dividends.reset_index().to_dict(orient="records")
            return {
                "fonte_utilizada": "yfinance",
                "resumo": f"Historico recente de dividendos com {len(payload)} registros.",
                "dados": payload,
            }

        history = ticker.history(period=settings.quote_history_period)
        if history.empty:
            raise ValueError(f"Sem dados para {symbol}")

        payload = history.reset_index().to_dict(orient="records")
        return {
            "fonte_utilizada": "yfinance",
            "resumo": f"{item.item} coletado com {len(payload)} registros historicos.",
            "dados": payload,
        }
