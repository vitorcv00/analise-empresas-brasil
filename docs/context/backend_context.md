# Backend Context

## Objetivo atual

O backend atual e um coletor deterministico por ticker.

Entrada principal:
- ticker, exemplo `BBAS3`

Saida principal:
- documentos corporativos baixados
- dados macro estruturados
- PDF padrao com panorama macro

## Responsabilidades

O backend atual faz:
- resolver empresa por ticker
- consultar CVM para documentos oficiais
- consultar RI como fallback para material recente
- consultar BCB e Focus para Selic, IPCA e projecoes
- salvar arquivos em `data/<ticker>/`
- gerar PDF macro em `data/_shared/`

## Fontes oficiais principais

- CVM Dados Abertos
- Banco Central do Brasil
- Focus/OData do BCB
- RI da empresa como fonte complementar

## Estrutura atual

- `src/collector/`: fluxo principal do coletor
- `src/providers/`: integracoes com fontes externas
- `src/storage/`: persistencia local de downloads e PDFs
- `src/schemas/`: contratos de dados

## Estado atual

O backend ja consegue:
- baixar balanco recente
- baixar fatos relevantes recentes
- baixar calendario corporativo
- localizar RI recente
- gerar panorama macro padrao em PDF

## Fora de escopo atual

- interpretacao inteligente dos documentos
- resumo analitico da empresa
- dashboards
- autenticacao
- multiusuario
