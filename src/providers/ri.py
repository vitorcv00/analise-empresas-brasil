"""Provider de coleta corporativa via paginas de RI conhecidas."""

from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin

import requests

from src.config.settings import settings

from src.providers.base import BaseProvider
from src.schemas.collection import CollectionItem
from src.schemas.company import CompanyProfile
from src.storage.downloads import ensure_ticker_data_dir, remove_sibling_variants, save_binary_file


class _AnchorParser(HTMLParser):
    """Extrai links simples de uma pagina HTML."""

    def __init__(self) -> None:
        """Inicializa o parser com estado vazio."""

        super().__init__()
        self.links: list[dict[str, str]] = []
        self._current_href: str | None = None
        self._current_text: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        """Captura o inicio de uma tag de link."""

        if tag != "a":
            return
        attrs_dict = dict(attrs)
        self._current_href = attrs_dict.get("href")
        self._current_text = []

    def handle_data(self, data: str) -> None:
        """Acumula texto interno do link atual."""

        if self._current_href is not None:
            self._current_text.append(data.strip())

    def handle_endtag(self, tag: str) -> None:
        """Fecha o link atual e salva o resultado."""

        if tag != "a" or not self._current_href:
            return
        text = " ".join(part for part in self._current_text if part).strip()
        self.links.append({"href": self._current_href, "text": text})
        self._current_href = None
        self._current_text = []


class RIProvider(BaseProvider):
    """Busca links corporativos relevantes em paginas de RI conhecidas."""

    SUPPORTED_ITEMS = {
        "ri_recente",
    }
    KEYWORDS = {
        "ri_recente": ["ri", "investidor", "apresentacao", "resultado", "release"],
    }

    def supports(self, item_name: str) -> bool:
        """Indica se o provider atende ao item corporativo."""

        return item_name in self.SUPPORTED_ITEMS

    def collect(self, company: CompanyProfile, item: CollectionItem) -> dict:
        """Busca links corporativos candidatos na pagina de RI da empresa."""

        base_url = company.ri_url or company.website
        if not base_url:
            return {
                "fonte_utilizada": "ri",
                "resumo": f"Nao ha URL de RI configurada para {company.ticker}.",
                "dados": None,
            }

        response = requests.get(base_url, timeout=settings.request_timeout_seconds)
        response.raise_for_status()
        parser = _AnchorParser()
        parser.feed(response.text)
        filtered_links = self._filter_links(base_url, parser.links, item.item)
        if not filtered_links:
            return {
                "fonte_utilizada": "ri",
                "resumo": f"Nenhum link compativel encontrado para {item.item} em {base_url}.",
                "dados": None,
            }

        payload = filtered_links[0]
        local_path = self._download_page(company, item.item, payload["url"])
        payload["arquivo_local"] = str(local_path)
        return {
            "fonte_utilizada": "ri",
            "resumo": f"Foram encontrados {len(filtered_links)} links candidatos para {item.item}.",
            "dados": payload,
        }

    def _filter_links(
        self,
        base_url: str,
        links: list[dict[str, str]],
        item_name: str,
    ) -> list[dict[str, str]]:
        """Filtra links por palavras-chave simples para cada item corporativo."""

        keywords = self.KEYWORDS[item_name]
        filtered: list[dict[str, str]] = []
        seen: set[str] = set()
        for link in links:
            href = (link.get("href") or "").strip()
            text = (link.get("text") or "").strip()
            if not href:
                continue
            combined = f"{text} {href}".lower()
            if not any(keyword in combined for keyword in keywords):
                continue
            absolute_url = urljoin(base_url, href)
            if item_name == "ri_recente" and absolute_url.rstrip("/") == base_url.rstrip("/"):
                continue
            if absolute_url in seen:
                continue
            seen.add(absolute_url)
            filtered.append(
                {
                    "titulo": text or absolute_url,
                    "url": absolute_url,
                    "_score": self._score_link(item_name, combined),
                }
            )
        filtered.sort(key=lambda item: item["_score"], reverse=True)
        return [{"titulo": item["titulo"], "url": item["url"]} for item in filtered]

    def _score_link(self, item_name: str, combined: str) -> int:
        """Atribui prioridade simples para links mais relevantes."""

        priority_keywords = {
            "ri_recente": ["central de resultados", "resultado", "release", "apresentacao"],
        }
        score = 0
        for index, keyword in enumerate(priority_keywords[item_name], start=1):
            if keyword in combined:
                score += 10 - index
        return score

    def _download_page(self, company: CompanyProfile, item_name: str, url: str) -> Path:
        """Baixa a pagina candidata de RI para consulta local posterior."""

        response = requests.get(url, timeout=settings.request_timeout_seconds)
        response.raise_for_status()
        target_dir = ensure_ticker_data_dir(company.ticker)
        content = response.content
        filename = f"{item_name}_ri_fallback.pdf" if content.startswith(b"%PDF-") else f"{item_name}_ri_fallback.html"
        path = save_binary_file(target_dir, filename, response.content)
        if path.suffix == ".pdf":
            remove_sibling_variants(path, [".html"])
        else:
            remove_sibling_variants(path, [".pdf"])
        return path
