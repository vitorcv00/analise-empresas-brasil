# Collector

Esta pasta implementa o fluxo deterministico do coletor base.

O que o codigo faz:
- resolve a empresa a partir do ticker
- monta um plano fixo com itens obrigatorios do contrato base
- executa providers para cada item
- consolida a resposta em um report final

Arquivos:
- `resolver.py`: resolve o perfil da empresa por cadastro local ou yfinance
- `planner.py`: monta o plano fixo de coleta
- `executor.py`: executa os providers do contrato
- `report_builder.py`: transforma artefatos brutos no report final
- `service.py`: servico principal do coletor

Exemplo de entrada:
```json
{
  "ticker": "BBAS3"
}
```

Exemplo de saida:
```json
{
  "report": {
    "corporativo": {
      "balanco_recente": {
        "status": "coletado"
      }
    },
    "macro": {
      "ipca_projecao": {
        "status": "coletado"
      }
    }
  }
}
```
