"""Cadastro inicial de empresas conhecidas pelo projeto."""

from __future__ import annotations

from src.schemas.company import CompanyProfile


COMPANY_REGISTRY: dict[str, CompanyProfile] = {
    "BBAS3": CompanyProfile(
        ticker="BBAS3",
        empresa="Banco do Brasil",
        setor="financeiro",
        subsetor="bancos",
        tipo_empresa="banco_multiplo",
        descricao=(
            "Banco brasileiro com forte atuacao em credito, agronegocio, "
            "servicos financeiros e presenca relevante no sistema bancario."
        ),
        website="https://www.bb.com.br",
        ri_url="https://ri.bb.com.br",
        cvm_code="1023",
    ),
    "ITUB4": CompanyProfile(
        ticker="ITUB4",
        empresa="Itau Unibanco",
        setor="financeiro",
        subsetor="bancos",
        tipo_empresa="banco_multiplo",
        descricao=(
            "Banco privado brasileiro com forte atuacao em credito, "
            "servicos financeiros, varejo e corporate banking."
        ),
        website="https://www.itau.com.br",
        ri_url="https://www.itau.com.br/relacoes-com-investidores",
        cvm_code="19348",
    ),
}
