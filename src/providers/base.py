"""Interface base para todos os providers do projeto."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from src.schemas.collection import CollectionItem
from src.schemas.company import CompanyProfile


class BaseProvider(ABC):
    """Define o contrato minimo de qualquer provider."""

    @abstractmethod
    def supports(self, item_name: str) -> bool:
        """Informa se o provider consegue coletar o item solicitado."""

        raise NotImplementedError

    @abstractmethod
    def collect(self, company: CompanyProfile, item: CollectionItem) -> dict[str, Any]:
        """Executa a coleta do item para a empresa informada."""

        raise NotImplementedError
