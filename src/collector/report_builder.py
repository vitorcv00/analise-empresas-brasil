"""Monta a saida consolidada do coletor a partir dos artefatos brutos."""

from __future__ import annotations

from src.schemas.collection import (
    CollectedArtifact,
    CorporateData,
    DeterministicTickerReport,
    DocumentSnapshot,
    MacroData,
    ValueSnapshot,
)
from src.schemas.company import CompanyProfile


def _artifact_by_name(artifacts: list[CollectedArtifact], item_name: str) -> CollectedArtifact:
    """Retorna o artefato correspondente ao nome do item."""

    for artifact in artifacts:
        if artifact.item == item_name:
            return artifact
    return CollectedArtifact(item=item_name, status="nao_suportado", resumo="Item nao executado.")


class ReportBuilder:
    """Transforma resultados brutos em um report mais facil de consumir."""

    def build(
        self,
        company: CompanyProfile,
        artifacts: list[CollectedArtifact],
    ) -> DeterministicTickerReport:
        """Retorna o report final do coletor base."""

        return DeterministicTickerReport(
            ticker=company.ticker,
            empresa=company.empresa,
            setor=company.setor,
            subsetor=company.subsetor,
            tipo_empresa=company.tipo_empresa,
            descricao=company.descricao,
            corporativo=CorporateData(
                balanco_recente=self._build_document_snapshot(artifacts, "balanco_recente"),
                ri_recente=self._build_document_snapshot(artifacts, "ri_recente"),
                fatos_relevantes_3m=self._build_document_snapshot(artifacts, "fatos_relevantes_3m"),
                calendario_corporativo=self._build_document_snapshot(artifacts, "calendario_corporativo"),
            ),
            macro=MacroData(
                selic_atual=self._build_value_snapshot(artifacts, "selic_atual"),
                selic_projecao=self._build_value_snapshot(artifacts, "selic_projecao"),
                ipca_atual=self._build_value_snapshot(artifacts, "ipca_atual"),
                ipca_meta=self._build_value_snapshot(artifacts, "ipca_meta"),
                ipca_projecao=self._build_value_snapshot(artifacts, "ipca_projecao"),
            ),
        )

    def _build_document_snapshot(
        self,
        artifacts: list[CollectedArtifact],
        item_name: str,
    ) -> DocumentSnapshot:
        """Converte um artefato de documento em snapshot consolidado."""

        artifact = _artifact_by_name(artifacts, item_name)
        return DocumentSnapshot(
            status=artifact.status,
            fonte=artifact.fonte_utilizada,
            resumo=artifact.resumo,
            dados_brutos=artifact.dados,
        )

    def _build_value_snapshot(
        self,
        artifacts: list[CollectedArtifact],
        item_name: str,
    ) -> ValueSnapshot:
        """Converte um artefato macro em snapshot resumido."""

        artifact = _artifact_by_name(artifacts, item_name)
        value = artifact.dados.get("valor") if isinstance(artifact.dados, dict) else None
        reference = artifact.dados.get("referencia") if isinstance(artifact.dados, dict) else None
        return ValueSnapshot(
            status=artifact.status,
            valor=value,
            referencia=reference,
            fonte=artifact.fonte_utilizada,
            resumo=artifact.resumo,
            dados_brutos=artifact.dados,
        )
