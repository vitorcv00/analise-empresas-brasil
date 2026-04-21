"""Planner deterministico do contrato base por ticker."""

from __future__ import annotations

from src.catalogs.base_contract import BASE_COLLECTION_CONTRACT
from src.collector.resolver import CompanyResolver
from src.schemas.collection import CollectionItem, CollectionPlan


class DeterministicPlanner:
    """Monta um plano fixo de coleta sem uso de LLM."""

    def __init__(self, resolver: CompanyResolver | None = None) -> None:
        """Inicializa o planner com o resolvedor de empresa."""

        self.resolver = resolver or CompanyResolver()

    def build_plan(self, ticker: str) -> CollectionPlan:
        """Retorna o plano fixo de coleta para o ticker informado."""

        company = self.resolver.resolve(ticker)
        items = [CollectionItem(**item) for item in BASE_COLLECTION_CONTRACT]
        return CollectionPlan(
            ticker=company.ticker,
            empresa=company.empresa,
            setor=company.setor,
            subsetor=company.subsetor,
            tipo_empresa=company.tipo_empresa,
            descricao=company.descricao,
            collection_plan=items,
        )
