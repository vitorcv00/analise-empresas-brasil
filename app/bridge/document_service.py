"""Servico de listagem de documentos gerados para um ticker."""

from __future__ import annotations

from pathlib import Path

from app.bridge.models import DocumentEntry


class DocumentService:
    """Lista arquivos gerados pelo backend e filtra o que a UI deve mostrar."""

    EXCLUDED_PATTERNS = [
        "ri_recente",
        ".zip",
    ]

    def list_documents_for_ticker(self, ticker: str) -> list[DocumentEntry]:
        """Retorna os documentos exibiveis para um ticker."""

        base_dir = Path("data") / ticker.upper().strip()
        if not base_dir.exists():
            return []

        documents: list[DocumentEntry] = []
        for file_path in sorted(base_dir.glob("*")):
            if not file_path.is_file():
                continue
            if any(pattern in file_path.name for pattern in self.EXCLUDED_PATTERNS):
                continue
            if file_path.suffix.lower() not in {".pdf"}:
                continue
            category = "macro" if "macro" in file_path.name else "corporativo"
            documents.append(
                DocumentEntry(
                    name=file_path.name,
                    path=str(file_path.resolve()),
                    category=category,
                )
            )
        return documents

    def get_shared_macro_document(self) -> DocumentEntry | None:
        """Retorna o PDF macro compartilhado quando ele existir."""

        macro_path = Path("data") / "_shared" / "macro_panorama_atual.pdf"
        if not macro_path.exists():
            return None
        return DocumentEntry(
            name=macro_path.name,
            path=str(macro_path.resolve()),
            category="macro",
        )
