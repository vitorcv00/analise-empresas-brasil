"""Executor deterministico do contrato base de coleta."""

from __future__ import annotations

from src.collector.macro_pdf import MacroPDFBuilder
from src.collector.report_builder import ReportBuilder
from src.collector.resolver import CompanyResolver
from src.providers.base import BaseProvider
from src.providers.bcb import BCBProvider
from src.providers.cvm import CVMProvider
from src.providers.focus import FocusProvider
from src.providers.policy import PolicyProvider
from src.providers.ri import RIProvider
from src.schemas.collection import CollectedArtifact, CollectionPlan, CollectorResult


class CollectorExecutor:
    """Executa o contrato fixo de coleta item por item."""

    def __init__(
        self,
        providers: list[BaseProvider] | None = None,
        resolver: CompanyResolver | None = None,
        report_builder: ReportBuilder | None = None,
        macro_pdf_builder: MacroPDFBuilder | None = None,
    ) -> None:
        """Inicializa o executor com providers e componentes auxiliares."""

        self.providers = providers or [
            CVMProvider(),
            BCBProvider(),
            FocusProvider(),
            PolicyProvider(),
            RIProvider(),
        ]
        self.resolver = resolver or CompanyResolver()
        self.report_builder = report_builder or ReportBuilder()
        self.macro_pdf_builder = macro_pdf_builder or MacroPDFBuilder()

    def execute(self, plan: CollectionPlan) -> CollectorResult:
        """Executa o plano e retorna os artefatos brutos e o report consolidado."""

        company = self.resolver.resolve(plan.ticker)
        artifacts: list[CollectedArtifact] = []

        for item in plan.collection_plan:
            provider = self._resolve_provider(item.item)
            if not provider:
                artifacts.append(
                    CollectedArtifact(
                        item=item.item,
                        status="nao_suportado",
                        resumo="Nenhum provider registrado para este item.",
                    )
                )
                continue

            try:
                payload = provider.collect(company, item)
                status = "coletado" if payload.get("dados") is not None else "pendente"
                artifacts.append(
                    CollectedArtifact(
                        item=item.item,
                        status=status,
                        fonte_utilizada=payload.get("fonte_utilizada"),
                        resumo=payload.get("resumo", ""),
                        dados=payload.get("dados"),
                    )
                )
            except Exception as exc:  # noqa: BLE001
                artifacts.append(
                    CollectedArtifact(
                        item=item.item,
                        status="erro",
                        fonte_utilizada=provider.__class__.__name__,
                        resumo=str(exc),
                    )
                )

        report = self.report_builder.build(company, artifacts)
        macro_pdf_path = self.macro_pdf_builder.build(report.macro)
        report = report.model_copy(update={"macro_pdf_path": str(macro_pdf_path)})
        return CollectorResult(plan=plan, resultados=artifacts, report=report)

    def _resolve_provider(self, item_name: str) -> BaseProvider | None:
        """Retorna o primeiro provider capaz de executar o item informado."""

        for provider in self.providers:
            if provider.supports(item_name):
                return provider
        return None
