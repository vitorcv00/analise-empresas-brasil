"""Schema do perfil basico da empresa usada no coletor."""

from __future__ import annotations

from pydantic import BaseModel, Field


class CompanyProfile(BaseModel):
    """Representa os metadados minimos da empresa coletada."""

    ticker: str = Field(..., min_length=4)
    empresa: str
    setor: str
    subsetor: str
    tipo_empresa: str
    descricao: str
    website: str | None = None
    ri_url: str | None = None
    cvm_code: str | None = None
