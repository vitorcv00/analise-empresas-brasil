# Frontend Context

## Objetivo da camada

Criar um app desktop em Python, executavel em Windows, Linux e Mac, para interagir com o backend atual sem usar terminal.

## Stack proposta

- Python
- PySide6 para interface desktop

## Motivos da escolha

- cross-platform real
- boa integracao com Python
- suporte a janelas, navegacao e estado local
- possibilidade de visualizacao PDF embutida ou via componentes nativos

## Telas aprovadas

### Tela inicial

Componentes:
- botao `Sair`
- campo de texto ou area de chat para inserir ticker
- botao `Baixar`
- loading durante a execucao
- lista de tickers favoritos clicaveis

Comportamento:
- aceitar ticker como `BBAS3`
- iniciar o backend ao clicar em `Baixar`
- apos finalizar, navegar para a tela de visualizacao
- ao clicar em favorito, recarregar as visualizacoes daquele ticker

### Tela de visualizacao

Componentes:
- lista de arquivos baixados na esquerda
- painel de visualizacao de PDF
- botao `Salvar como favorito`
- botao `Atualizar`
- botao `Voltar`

Comportamento:
- clicar em um arquivo abre no painel
- permitir navegar entre os documentos baixados do ticker
- abrir PDFs em modo multipagina

## Favoritos

Favoritos devem ser salvos localmente, em um arquivo simples, sem banco de dados na primeira versao.

## Cache local de coleta

Se os arquivos de um ticker ja foram atualizados no dia atual, o app pode abrir os arquivos existentes sem rodar nova coleta.

Persistencia usada:
- `data/_app/favorites.json`
- `data/_app/collection_state.json`

## Relacao com o backend

O frontend nao faz coleta direta.

Ele apenas:
- chama o backend
- mostra loading
- lista arquivos gerados
- abre os arquivos dentro do app
- salva favoritos locais
