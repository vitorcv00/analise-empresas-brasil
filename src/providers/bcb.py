"""Provider do Banco Central para series oficiais simples."""

from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any

import requests

from src.config.settings import settings
from src.providers.base import BaseProvider
from src.schemas.collection import CollectionItem
from src.schemas.company import CompanyProfile


class BCBProvider(BaseProvider):
    """Consulta series do SGS para valores oficiais correntes."""

    BASE_URL = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.{code}/dados"

    def supports(self, item_name: str) -> bool:
        """Indica se o item e suportado pelas series configuradas."""

        return item_name in settings.bcb_series

    def collect(self, company: CompanyProfile, item: CollectionItem) -> dict[str, Any]:
        """Coleta o ultimo valor disponivel da serie correspondente."""

        code = settings.bcb_series[item.item]
        end_date = datetime.today()
        lookback_days = 400 if item.item == "selic_atual" else 365 * 3
        response = requests.get(
            self.BASE_URL.format(code=code),
            params={
                "formato": "json",
                "dataInicial": (end_date - timedelta(days=lookback_days)).strftime("%d/%m/%Y"),
                "dataFinal": end_date.strftime("%d/%m/%Y"),
            },
            timeout=settings.request_timeout_seconds,
        )
        response.raise_for_status()
        data: Any = response.json()
        if not isinstance(data, list) or not data:
            raise ValueError(f"Nenhum dado encontrado para a serie {code}.")
        latest = data[-1]

        return {
            "fonte_utilizada": "bcb_sgs",
            "resumo": f"Ultimo valor oficial coletado para {item.item}.",
            "dados": {
                "valor": latest.get("valor"),
                "referencia": latest.get("data"),
                "serie_codigo": code,
                "ultimos_registros": data[-12:],
            },
        }
