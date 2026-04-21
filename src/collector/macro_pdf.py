"""Geracao do PDF padrao com o panorama macroeconomico."""

from __future__ import annotations

from pathlib import Path

from src.schemas.collection import MacroData
from src.storage.downloads import ensure_ticker_data_dir
from src.storage.pdf_writer import write_simple_pdf


class MacroPDFBuilder:
    """Gera um PDF padrao com informacoes de Selic e IPCA."""

    def build(self, macro: MacroData) -> Path:
        """Gera e retorna o caminho do PDF macro consolidado."""

        shared_dir = Path("data") / "_shared"
        shared_dir.mkdir(parents=True, exist_ok=True)
        output_path = shared_dir / "macro_panorama_atual.pdf"
        lines = [
            "Selic",
            f"Atual: {macro.selic_atual.valor} | Ref: {macro.selic_atual.referencia}",
            f"Projecao de mercado: {macro.selic_projecao.valor} | Ref: {macro.selic_projecao.referencia}",
            "",
            "IPCA",
            f"Atual: {macro.ipca_atual.valor} | Ref: {macro.ipca_atual.referencia}",
            f"Meta: {macro.ipca_meta.valor} | Ref: {macro.ipca_meta.referencia}",
            f"Projecao de mercado: {macro.ipca_projecao.valor} | Ref: {macro.ipca_projecao.referencia}",
            "",
            "Observacao",
            "Este arquivo e padrao e independe do ticker consultado.",
        ]
        return write_simple_pdf(output_path, "Panorama Macro Atual", lines)
