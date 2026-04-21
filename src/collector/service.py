"""Servico principal do coletor base deterministico."""

from __future__ import annotations

from src.collector.executor import CollectorExecutor
from src.collector.planner import DeterministicPlanner
from src.schemas.collection import CollectorResult


class BaseTickerCollectorService:
    """Coordena montagem do plano fixo e execucao da coleta."""

    def __init__(
        self,
        planner: DeterministicPlanner | None = None,
        executor: CollectorExecutor | None = None,
    ) -> None:
        """Inicializa o servico com planner e executor."""

        self.planner = planner or DeterministicPlanner()
        self.executor = executor or CollectorExecutor()

    def run(self, ticker: str) -> CollectorResult:
        """Executa o fluxo completo do coletor base para um ticker."""

        plan = self.planner.build_plan(ticker)
        return self.executor.execute(plan)
