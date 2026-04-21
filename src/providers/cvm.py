"""Provider da CVM Dados Abertos para documentos corporativos oficiais."""

from __future__ import annotations

import csv
import io
import time
import zipfile
from datetime import datetime, timedelta
from functools import lru_cache
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

import requests

from src.config.settings import settings
from src.providers.base import BaseProvider
from src.schemas.collection import CollectionItem
from src.schemas.company import CompanyProfile
from src.storage.downloads import ensure_ticker_data_dir, remove_sibling_variants, save_binary_file


class CVMProvider(BaseProvider):
    """Consulta DFP, ITR e IPE na base aberta da CVM."""

    SUPPORTED_ITEMS = {
        "balanco_recente",
        "fatos_relevantes_3m",
        "calendario_corporativo",
    }
    DFP_BASE_URL = "https://dados.cvm.gov.br/dados/CIA_ABERTA/DOC/DFP/DADOS/dfp_cia_aberta_{year}.zip"
    ITR_BASE_URL = "https://dados.cvm.gov.br/dados/CIA_ABERTA/DOC/ITR/DADOS/itr_cia_aberta_{year}.zip"
    IPE_BASE_URL = "https://dados.cvm.gov.br/dados/CIA_ABERTA/DOC/IPE/DADOS/ipe_cia_aberta_{year}.zip"

    def supports(self, item_name: str) -> bool:
        """Indica se o provider atende ao item corporativo informado."""

        return item_name in self.SUPPORTED_ITEMS

    def collect(self, company: CompanyProfile, item: CollectionItem) -> dict[str, Any]:
        """Executa a coleta oficial do item usando CVM Dados Abertos."""

        if not company.cvm_code:
            return {
                "fonte_utilizada": "cvm",
                "resumo": f"Ticker {company.ticker} nao possui codigo CVM configurado.",
                "dados": None,
            }

        if item.item == "balanco_recente":
            return self._collect_latest_financial_document(company)
        if item.item == "fatos_relevantes_3m":
            return self._collect_recent_ipe_documents(
                company=company,
                target_category="Fato Relevante",
                item_name=item.item,
                recent_days=settings.default_recent_days,
            )
        if item.item == "calendario_corporativo":
            return self._collect_recent_ipe_documents(
                company=company,
                target_category="Calendario de Eventos Corporativos",
                item_name=item.item,
                recent_days=365,
            )
        return {
            "fonte_utilizada": "cvm",
            "resumo": f"Item {item.item} ainda nao foi implementado na CVM.",
            "dados": None,
        }

    def _collect_latest_financial_document(self, company: CompanyProfile) -> dict[str, Any]:
        """Retorna o documento financeiro oficial mais recente entre DFP e ITR."""

        candidates: list[dict[str, Any]] = []
        for year in self._candidate_years():
            candidates.extend(self._load_financial_rows("DFP", year, company.cvm_code))
            candidates.extend(self._load_financial_rows("ITR", year, company.cvm_code))

        if not candidates:
            return {
                "fonte_utilizada": "cvm",
                "resumo": f"Nenhum DFP ou ITR encontrado para {company.ticker}.",
                "dados": None,
            }

        candidates.sort(
            key=lambda row: (row["dt_refer"], row["dt_receb"], row["versao"]),
            reverse=True,
        )
        selected = candidates[0]
        local_path = self._download_document(
            company=company,
            item_name="balanco_recente",
            url=selected["link_doc"],
            reference_date=selected["dt_refer"].strftime("%Y-%m-%d"),
            version=selected["versao"],
        )
        return {
            "fonte_utilizada": "cvm",
            "resumo": f"Documento oficial mais recente encontrado: {selected['categoria']} {selected['dt_refer']}.",
            "dados": {
                "categoria": selected["categoria"],
                "data_referencia": selected["dt_refer"].strftime("%Y-%m-%d"),
                "data_entrega": selected["dt_receb"].strftime("%Y-%m-%d"),
                "versao": selected["versao"],
                "url": selected["link_doc"],
                "id_documento": selected["id_doc"],
                "arquivo_local": str(local_path),
            },
        }

    def _collect_recent_ipe_documents(
        self,
        company: CompanyProfile,
        target_category: str,
        item_name: str,
        recent_days: int,
    ) -> dict[str, Any]:
        """Retorna documentos IPE recentes de uma categoria especifica."""

        min_date = datetime.today().date() - timedelta(days=recent_days)
        candidates: list[dict[str, Any]] = []
        for year in self._candidate_years():
            candidates.extend(
                self._load_ipe_rows(
                    year=year,
                    cvm_code=company.cvm_code,
                    target_category=target_category,
                    min_date=min_date,
                )
            )

        if not candidates:
            return {
                "fonte_utilizada": "cvm",
                "resumo": f"Nenhum documento CVM encontrado para {item_name}.",
                "dados": None,
            }

        candidates.sort(key=lambda row: (row["data_entrega"], row["versao"]), reverse=True)
        payload = []
        for row in candidates[:5]:
            local_path = self._download_document(
                company=company,
                item_name=item_name,
                url=row["link_download"],
                reference_date=row["data_entrega"].strftime("%Y-%m-%d"),
                version=row["versao"],
            )
            payload.append(
                {
                    "categoria": row["categoria"],
                    "tipo": row["tipo"],
                    "especie": row["especie"],
                    "assunto": row["assunto"],
                    "data_entrega": row["data_entrega"].strftime("%Y-%m-%d"),
                    "url": row["link_download"],
                    "arquivo_local": str(local_path),
                }
            )
        return {
            "fonte_utilizada": "cvm",
            "resumo": f"Foram encontrados {len(candidates)} documentos oficiais para {item_name}.",
            "dados": payload,
        }

    def _candidate_years(self) -> list[int]:
        """Retorna os anos prioritarios para busca dos datasets atuais."""

        return [settings.current_year, settings.current_year - 1]

    @lru_cache(maxsize=16)
    def _load_zip_rows(self, url: str, csv_filename: str) -> list[dict[str, str]]:
        """Baixa um ZIP da CVM e retorna suas linhas como dicionarios."""

        response = requests.get(url, timeout=120)
        response.raise_for_status()
        with zipfile.ZipFile(io.BytesIO(response.content)) as zipped:
            with zipped.open(csv_filename) as csv_file:
                decoded = io.TextIOWrapper(csv_file, encoding="latin1")
                return list(csv.DictReader(decoded, delimiter=";"))

    def _load_financial_rows(self, category: str, year: int, cvm_code: str) -> list[dict[str, Any]]:
        """Filtra linhas financeiras de DFP ou ITR para a companhia."""

        url = self.DFP_BASE_URL.format(year=year) if category == "DFP" else self.ITR_BASE_URL.format(year=year)
        filename = f"{category.lower()}_cia_aberta_{year}.csv"
        try:
            rows = self._load_zip_rows(url, filename)
        except requests.HTTPError:
            return []

        filtered: list[dict[str, Any]] = []
        for row in rows:
            if self._normalize_cvm_code(row.get("CD_CVM")) != self._normalize_cvm_code(cvm_code):
                continue
            filtered.append(
                {
                    "categoria": row.get("CATEG_DOC"),
                    "dt_refer": datetime.strptime(row["DT_REFER"], "%Y-%m-%d").date(),
                    "dt_receb": datetime.strptime(row["DT_RECEB"], "%Y-%m-%d").date(),
                    "versao": int(row.get("VERSAO") or 0),
                    "link_doc": row.get("LINK_DOC"),
                    "id_doc": row.get("ID_DOC"),
                }
            )
        return filtered

    def _load_ipe_rows(
        self,
        year: int,
        cvm_code: str,
        target_category: str,
        min_date: datetime.date,
    ) -> list[dict[str, Any]]:
        """Filtra linhas de IPE por companhia, categoria e data minima."""

        url = self.IPE_BASE_URL.format(year=year)
        filename = f"ipe_cia_aberta_{year}.csv"
        try:
            rows = self._load_zip_rows(url, filename)
        except requests.HTTPError:
            return []

        filtered: list[dict[str, Any]] = []
        for row in rows:
            if self._normalize_cvm_code(row.get("Codigo_CVM")) != self._normalize_cvm_code(cvm_code):
                continue
            if self._normalize_text(row.get("Categoria")) != self._normalize_text(target_category):
                continue
            data_entrega = datetime.strptime(row["Data_Entrega"], "%Y-%m-%d").date()
            if data_entrega < min_date:
                continue
            filtered.append(
                {
                    "categoria": row.get("Categoria"),
                    "tipo": row.get("Tipo"),
                    "especie": row.get("Especie"),
                    "assunto": row.get("Assunto"),
                    "data_entrega": data_entrega,
                    "versao": int(row.get("Versao") or 0),
                    "link_download": row.get("Link_Download"),
                }
            )
        return filtered

    def _normalize_cvm_code(self, value: Any) -> str:
        """Normaliza o codigo CVM para comparacao segura."""

        text = str(value or "").strip()
        return text.lstrip("0") or "0"

    def _normalize_text(self, value: Any) -> str:
        """Normaliza texto simples para comparacao sem ruido basico."""

        text = str(value or "").strip().lower()
        return (
            text.replace("á", "a")
            .replace("à", "a")
            .replace("ã", "a")
            .replace("â", "a")
            .replace("é", "e")
            .replace("ê", "e")
            .replace("í", "i")
            .replace("ó", "o")
            .replace("ô", "o")
            .replace("õ", "o")
            .replace("ú", "u")
            .replace("ç", "c")
        )

    def _download_document(
        self,
        company: CompanyProfile,
        item_name: str,
        url: str,
        reference_date: str,
        version: int,
    ) -> Path:
        """Baixa o documento oficial e salva em data/<ticker>/."""

        last_error: Exception | None = None
        response = None
        for attempt in range(1, 4):
            try:
                response = requests.get(url.replace("http://", "https://"), timeout=120, headers={"User-Agent": "Mozilla/5.0"})
                response.raise_for_status()
                break
            except requests.RequestException as exc:
                last_error = exc
                if attempt == 3:
                    raise
                time.sleep(attempt)

        if response is None:
            raise RuntimeError("Falha inesperada ao baixar documento da CVM.") from last_error

        target_dir = ensure_ticker_data_dir(company.ticker)
        content = response.content
        if content.startswith(b"%PDF-"):
            filename = f"{item_name}_{reference_date}_v{version}.pdf"
            path = save_binary_file(target_dir, filename, content)
            remove_sibling_variants(path, [".html"])
            return path
        if content.startswith(b"PK\x03\x04"):
            zip_path = save_binary_file(target_dir, f"{item_name}_{reference_date}_v{version}.zip", content)
            extracted_pdf = self._extract_pdf_from_zip(target_dir, item_name, reference_date, version, content)
            if extracted_pdf:
                remove_sibling_variants(extracted_pdf, [".html"])
            return extracted_pdf or zip_path
        filename = f"{item_name}_{reference_date}_v{version}.html"
        path = save_binary_file(target_dir, filename, content)
        remove_sibling_variants(path, [".pdf"])
        return path

    def _extract_pdf_from_zip(
        self,
        target_dir: Path,
        item_name: str,
        reference_date: str,
        version: int,
        zip_content: bytes,
    ) -> Path | None:
        """Extrai o primeiro PDF encontrado dentro de um ZIP baixado da CVM."""

        with zipfile.ZipFile(io.BytesIO(zip_content)) as zipped:
            pdf_names = [name for name in zipped.namelist() if name.lower().endswith(".pdf")]
            if not pdf_names:
                return None
            preferred_name = sorted(pdf_names)[0]
            with zipped.open(preferred_name) as pdf_file:
                pdf_bytes = pdf_file.read()
        return save_binary_file(target_dir, f"{item_name}_{reference_date}_v{version}.pdf", pdf_bytes)
