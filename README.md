# MVP Analise Empresas

Este projeto agora esta organizado em duas camadas conceituais:

1. Coletor base por ticker
2. Agentes posteriores de interpretacao e apresentacao

## Estado atual

O foco atual e o coletor base deterministico.

Dado um ticker como `BBAS3`, o sistema tenta reunir:
- balanco recente
- RI recente
- fatos relevantes dos ultimos 3 meses
- calendario corporativo
- Selic atual
- meta Selic
- projecao de mercado para Selic
- IPCA atual
- meta de inflacao
- projecao de mercado para IPCA

Arquivos gerados:
- documentos corporativos em `data/<ticker>/`
- panorama macro padrao em `data/_shared/macro_panorama_atual.pdf`

## Execucao

No WSL com o ambiente `mvp_agentes`:

```bash
python -m src.main BBAS3
```

## Observacao

O bloco macro usa fontes oficiais do Banco Central quando disponiveis.
O bloco corporativo usa busca deterministica em links de RI conhecidos no cadastro inicial da empresa.
