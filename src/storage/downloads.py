"""Utilitarios para persistir downloads corporativos no disco."""

from __future__ import annotations

from pathlib import Path
import re


def ensure_ticker_data_dir(ticker: str) -> Path:
    """Cria e retorna a pasta local de dados do ticker."""

    path = Path("data") / ticker.upper().strip()
    path.mkdir(parents=True, exist_ok=True)
    return path


def sanitize_filename(value: str) -> str:
    """Normaliza um nome para uso seguro em arquivo local."""

    cleaned = re.sub(r"[^a-zA-Z0-9._-]+", "_", value.strip())
    return cleaned.strip("._") or "documento"


def save_binary_file(target_dir: Path, filename: str, content: bytes) -> Path:
    """Escreve um arquivo binario no diretorio indicado."""

    target_path = target_dir / sanitize_filename(filename)
    target_path.write_bytes(content)
    return target_path


def remove_sibling_variants(target_path: Path, suffixes: list[str]) -> None:
    """Remove variantes de extensao para evitar arquivos duplicados incorretos."""

    for suffix in suffixes:
        candidate = target_path.with_suffix(suffix)
        if candidate == target_path:
            continue
        if candidate.exists():
            candidate.unlink()
