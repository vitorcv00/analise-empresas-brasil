# Catalogs

Esta pasta guarda catalogos estaticos do coletor.

O que o codigo faz:
- define o cadastro inicial de empresas conhecidas
- define o contrato fixo de coleta do MVP

Arquivos:
- `company_registry.py`: cadastro inicial com metadados e URLs de RI conhecidas
- `base_contract.py`: lista fixa de itens do coletor base

Exemplo de entrada:
```python
ticker = "BBAS3"
```

Exemplo de saida do registry:
```json
{
  "ticker": "BBAS3",
  "empresa": "Banco do Brasil",
  "ri_url": "https://ri.bb.com.br"
}
```

Exemplo de item do contrato base:
```json
{
  "item": "ipca_projecao",
  "categoria": "macro",
  "fontes_preferenciais": ["bcb_focus"]
}
```
