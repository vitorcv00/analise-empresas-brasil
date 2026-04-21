"""Provider do Banco Central para projecoes de mercado via Focus/OData."""

from __future__ import annotations

from typing import Any

import requests

from src.config.settings import settings
from src.providers.base import BaseProvider
from src.schemas.collection import CollectionItem
from src.schemas.company import CompanyProfile


class FocusProvider(BaseProvider):
    """Consulta projecoes anuais de mercado para Selic e IPCA."""

    INDICATOR_MAP = {
        "selic_projecao": "Selic",
        "ipca_projecao": "IPCA",
    }

    def supports(self, item_name: str) -> bool:
        """Indica se o provider consegue atender ao item solicitado."""

        return item_name in self.INDICATOR_MAP

    def collect(self, company: CompanyProfile, item: CollectionItem) -> dict[str, Any]:
        """Retorna a projecao de mercado anual mais recente para o indicador."""

        indicator = self.INDICATOR_MAP[item.item]
        year = str(settings.current_year)
        url = (
            f"{settings.focus_base_url}/ExpectativasMercadoAnuais"
            f"?$filter=Indicador%20eq%20'{indicator}'%20and%20DataReferencia%20eq%20'{year}'"
            "&$orderby=Data%20desc&$top=1&$format=json"
        )
        response = requests.get(url, timeout=settings.request_timeout_seconds)
        response.raise_for_status()
        payload = response.json().get("value", [])
        if not payload:
            raise ValueError(f"Sem projecao de mercado encontrada para {indicator} em {year}.")

        latest = payload[0]
        return {
            "fonte_utilizada": "bcb_focus",
            "resumo": f"Projecao de mercado mais recente para {indicator} no ano {year}.",
            "dados": {
                "valor": latest.get("Mediana"),
                "referencia": f"{latest.get('Data')} | ano {latest.get('DataReferencia')}",
                "media": latest.get("Media"),
                "respondentes": latest.get("numeroRespondentes"),
                "serie": latest,
            },
        }
