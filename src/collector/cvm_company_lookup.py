"""Lookup de companhias abertas usando o cadastro oficial da CVM."""

from __future__ import annotations

import csv
import io
from functools import lru_cache
from typing import Any
from urllib.parse import urlparse
import difflib

import requests

from src.config.settings import settings


class CVMCompanyLookup:
    """Resolve metadados oficiais da CVM a partir do nome comercial da empresa."""

    CAD_URL = "https://dados.cvm.gov.br/dados/CIA_ABERTA/CAD/DADOS/cad_cia_aberta.csv"

    def find_company(self, company_name: str, website: str | None = None) -> dict[str, str] | None:
        """Busca a melhor correspondencia no cadastro da CVM."""

        normalized_name = self._normalize_company_name(company_name)
        candidates = self._active_rows()

        exact = [
            row
            for row in candidates
            if normalized_name in {
                self._normalize_company_name(row.get("DENOM_SOCIAL", "")),
                self._normalize_company_name(row.get("DENOM_COMERC", "")),
            }
        ]
        if exact:
            return exact[0]

        best_row = None
        best_score = 0.0
        website_domain = self._extract_domain(website)
        for row in candidates:
            options = [
                self._normalize_company_name(row.get("DENOM_SOCIAL", "")),
                self._normalize_company_name(row.get("DENOM_COMERC", "")),
            ]
            score = max(difflib.SequenceMatcher(a=normalized_name, b=option).ratio() for option in options if option)
            if website_domain:
                email_domain = self._extract_domain(row.get("EMAIL"))
                if email_domain and website_domain == email_domain:
                    score += 0.15
            if score > best_score:
                best_score = score
                best_row = row

        if best_row and best_score >= 0.74:
            return best_row
        return None

    @lru_cache(maxsize=1)
    def _active_rows(self) -> list[dict[str, str]]:
        """Carrega o cadastro da CVM e retorna apenas companhias ativas."""

        response = requests.get(self.CAD_URL, timeout=settings.request_timeout_seconds * 4)
        response.raise_for_status()
        decoded = response.content.decode("latin1")
        rows = list(csv.DictReader(io.StringIO(decoded), delimiter=";"))
        return [row for row in rows if row.get("SIT") == "ATIVO"]

    def _normalize_company_name(self, value: str) -> str:
        """Normaliza nome empresarial para comparacao robusta."""

        text = (value or "").upper().strip()
        replacements = {
            "S.A.": "",
            " S/A": "",
            " SA": "",
            " - EM RECUPERACAO JUDICIAL": "",
            " - EM LIQUIDACAO EXTRAJUDICIAL": "",
            "BANCO": "BCO",
            "PETROLEO": "PETR",
        }
        for old, new in replacements.items():
            text = text.replace(old, new)
        text = (
            text.replace("Á", "A")
            .replace("À", "A")
            .replace("Ã", "A")
            .replace("Â", "A")
            .replace("É", "E")
            .replace("Ê", "E")
            .replace("Í", "I")
            .replace("Ó", "O")
            .replace("Ô", "O")
            .replace("Õ", "O")
            .replace("Ú", "U")
            .replace("Ç", "C")
        )
        return " ".join(text.split())

    def _extract_domain(self, value: str | None) -> str | None:
        """Extrai dominio simples de uma URL ou email."""

        if not value:
            return None
        text = value.strip().lower()
        if "@" in text:
            return text.split("@")[-1]
        parsed = urlparse(text if "://" in text else f"https://{text}")
        return parsed.netloc.replace("www.", "") or None
