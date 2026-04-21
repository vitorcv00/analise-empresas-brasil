"""Configuracoes centrais usadas pelo coletor deterministico."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict


@dataclass(frozen=True)
class Settings:
    """Agrupa constantes e configuracoes tecnicas do projeto."""

    quote_history_period: str = "5y"
    default_recent_days: int = 90
    request_timeout_seconds: int = 30
    inflation_target: float = 3.0
    inflation_target_reference: str = "Resolucao CMN 5.141/2024"
    focus_base_url: str = "https://olinda.bcb.gov.br/olinda/servico/Expectativas/versao/v1/odata"
    bcb_series: Dict[str, int] = field(
        default_factory=lambda: {
            "selic_atual": 432,
            "ipca_atual": 433,
        }
    )

    @property
    def current_year(self) -> int:
        """Retorna o ano corrente no momento da execucao."""

        return datetime.today().year


settings = Settings()
