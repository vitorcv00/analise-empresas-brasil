"""Provider para metas oficiais e valores normativos simples."""

from __future__ import annotations

from typing import Any

from src.config.settings import settings
from src.providers.base import BaseProvider
from src.schemas.collection import CollectionItem
from src.schemas.company import CompanyProfile


class PolicyProvider(BaseProvider):
    """Fornece metas oficiais que nao dependem de consulta dinamica complexa."""

    def supports(self, item_name: str) -> bool:
        """Indica se o provider atende ao item informado."""

        return item_name == "ipca_meta"

    def collect(self, company: CompanyProfile, item: CollectionItem) -> dict[str, Any]:
        """Retorna a meta oficial de inflacao vigente no projeto."""

        return {
            "fonte_utilizada": "cmn",
            "resumo": "Meta oficial de inflacao vigente no regime atual.",
            "dados": {
                "valor": settings.inflation_target,
                "referencia": settings.inflation_target_reference,
            },
        }
