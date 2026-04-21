# Src

Esta pasta concentra o coletor base por ticker.

O que existe aqui:
- `catalogs/`: contrato fixo de coleta e cadastro inicial de empresas
- `schemas/`: contratos Pydantic do plano, dos artefatos e do report final
- `providers/`: integracoes com fontes macro e corporativas
- `collector/`: planner deterministico, executor e consolidacao do report
- `config/`: configuracoes centrais do projeto
- `main.py`: ponto de entrada do coletor

Fluxo geral:
1. Receber um ticker
2. Resolver o perfil basico da empresa
3. Montar um plano fixo de coleta
4. Executar os providers do contrato base
5. Retornar um report estruturado com bloco corporativo e bloco macro

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
    "ticker": "BBAS3",
    "empresa": "Banco do Brasil",
    "macro": {
      "selic_atual": {
        "status": "coletado"
      }
    }
  }
}
```
