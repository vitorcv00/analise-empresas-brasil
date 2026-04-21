"""Schemas do coletor deterministico e do contrato de saida."""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field


Priority = Literal["alta", "media", "baixa"]
CollectionStatus = Literal["coletado", "pendente", "nao_suportado", "erro"]
CollectionCategory = Literal["corporativo", "macro"]


class CollectionItem(BaseModel):
    """Representa um item fixo do contrato de coleta."""

    item: str
    categoria: CollectionCategory
    prioridade: Priority
    janela: str
    fontes_preferenciais: list[str]
    formato_esperado: list[str]
    justificativa: str


class CollectionPlan(BaseModel):
    """Representa o plano deterministico montado para um ticker."""

    ticker: str
    empresa: str
    setor: str
    subsetor: str
    tipo_empresa: str
    descricao: str
    collection_plan: list[CollectionItem]


class CollectedArtifact(BaseModel):
    """Representa o resultado bruto de coleta de um item do contrato."""

    item: str
    status: CollectionStatus
    fonte_utilizada: str | None = None
    resumo: str
    dados: Any | None = None


class ValueSnapshot(BaseModel):
    """Representa um valor macro resumido com metadados basicos."""

    status: CollectionStatus
    valor: Any | None = None
    referencia: str | None = None
    fonte: str | None = None
    resumo: str = ""
    dados_brutos: Any | None = None


class DocumentSnapshot(BaseModel):
    """Representa um documento ou conjunto de links corporativos relevantes."""

    status: CollectionStatus
    fonte: str | None = None
    resumo: str = ""
    dados_brutos: Any | None = None


class CorporateData(BaseModel):
    """Agrupa os itens corporativos do contrato base."""

    balanco_recente: DocumentSnapshot
    ri_recente: DocumentSnapshot
    fatos_relevantes_3m: DocumentSnapshot
    calendario_corporativo: DocumentSnapshot


class MacroData(BaseModel):
    """Agrupa os itens macroeconomicos do contrato base."""

    selic_atual: ValueSnapshot
    selic_projecao: ValueSnapshot
    ipca_atual: ValueSnapshot
    ipca_meta: ValueSnapshot
    ipca_projecao: ValueSnapshot


class DeterministicTickerReport(BaseModel):
    """Representa a saida consolidada do coletor base."""

    ticker: str
    empresa: str
    setor: str
    subsetor: str
    tipo_empresa: str
    descricao: str
    corporativo: CorporateData
    macro: MacroData
    macro_pdf_path: str | None = None


class CollectorResult(BaseModel):
    """Representa a resposta completa do coletor, incluindo detalhes de execucao."""

    plan: CollectionPlan
    resultados: list[CollectedArtifact]
    report: DeterministicTickerReport
