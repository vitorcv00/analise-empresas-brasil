# Providers

Esta pasta concentra os conectores com fontes externas.

O que o codigo faz:
- identifica qual fonte atende a cada item do contrato
- consulta APIs ou paginas oficiais
- devolve um resultado padronizado para o executor

Arquivos:
- `base.py`: interface base comum
- `cvm.py`: documentos oficiais via CVM Dados Abertos
- `bcb.py`: valores oficiais correntes do SGS
- `focus.py`: projecoes de mercado via Focus/OData
- `policy.py`: metas oficiais simples do regime atual
- `ri.py`: fallback simples para material de RI recente
- `yfinance.py`: suporte auxiliar para resolver perfil de empresa

Observacao importante:
- RI nao possui um padrao unico de API para todas as empresas
- para documentos oficiais estruturados, a fonte mais promissora e a CVM Dados Abertos
- o fluxo atual prioriza CVM para documentos oficiais e usa RI apenas como fallback
- documentos baixados sao salvos em `data/<ticker>/`

Exemplo de entrada:
```json
{
  "ticker": "BBAS3",
  "item": "selic_projecao"
}
```

Exemplo de saida:
```json
{
  "fonte_utilizada": "bcb_focus",
  "resumo": "Projecao de mercado mais recente para Selic no ano corrente.",
  "dados": {
    "valor": 13.0
  }
}
```
