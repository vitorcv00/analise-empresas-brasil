# Schemas

Esta pasta define os contratos de dados usando Pydantic.

O que o codigo faz:
- valida o perfil da empresa
- valida o plano fixo de coleta
- valida os artefatos brutos de cada provider
- valida o report final com bloco corporativo e macro

Arquivos:
- `company.py`: schema do perfil da empresa
- `collection.py`: schemas do plano, artefatos e report consolidado

Exemplo de entrada:
```json
{
  "ticker": "BBAS3",
  "empresa": "Banco do Brasil",
  "setor": "financeiro"
}
```

Exemplo de saida validada:
```json
{
  "ticker": "BBAS3",
  "corporativo": {
    "balanco_recente": {
      "status": "coletado"
    }
  },
  "macro": {
    "selic_atual": {
      "valor": "14.75"
    }
  }
}
```
