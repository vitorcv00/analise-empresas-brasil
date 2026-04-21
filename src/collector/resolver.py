"""Resolver deterministico do perfil da empresa a partir do ticker."""

from __future__ import annotations

from typing import Any

import yfinance as yf

from src.catalogs.company_registry import COMPANY_REGISTRY
from src.collector.cvm_company_lookup import CVMCompanyLookup
from src.schemas.company import CompanyProfile


class CompanyResolver:
    """Resolve metadados basicos da empresa via cadastro local ou yfinance."""

    def __init__(self, cvm_lookup: CVMCompanyLookup | None = None) -> None:
        """Inicializa o resolver com lookup opcional da CVM."""

        self.cvm_lookup = cvm_lookup or CVMCompanyLookup()

    def resolve(self, ticker: str) -> CompanyProfile:
        """Retorna o perfil da empresa a partir do ticker informado."""

        normalized = ticker.upper().strip()
        if normalized in COMPANY_REGISTRY:
            return COMPANY_REGISTRY[normalized]
        return self._resolve_with_yfinance(normalized)

    def _resolve_with_yfinance(self, ticker: str) -> CompanyProfile:
        """Busca um perfil minimo no yfinance quando o ticker nao esta no registry."""

        info: Any = yf.Ticker(f"{ticker}.SA").info
        long_name = info.get("longName") or info.get("shortName")
        if not long_name:
            raise KeyError(f"Nao foi possivel resolver a empresa para o ticker {ticker}.")

        cvm_company = self.cvm_lookup.find_company(long_name, info.get("website"))

        return CompanyProfile(
            ticker=ticker,
            empresa=long_name,
            setor=info.get("sector") or "desconhecido",
            subsetor=info.get("industry") or "desconhecido",
            tipo_empresa="companhia_aberta",
            descricao=info.get("longBusinessSummary") or "Descricao nao encontrada.",
            website=info.get("website"),
            cvm_code=cvm_company.get("CD_CVM") if cvm_company else None,
        )
