# App Scope

## Escopo aprovado da primeira versao

### Objetivo

Transformar o coletor atual em um app desktop com interface simples e foco em consulta por ticker.

### Fluxo principal

1. Usuario abre o app
2. Digita um ticker
3. Clica em `Baixar`
4. App roda a coleta
5. App mostra os documentos e o PDF macro
6. Usuario pode salvar o ticker como favorito

## Funcionalidades obrigatorias

- rodar em Windows, Linux e Mac
- aceitar ticker por texto
- mostrar loading durante a coleta
- navegar para tela de visualizacao ao concluir
- listar arquivos baixados na lateral esquerda
- abrir PDF no painel principal
- salvar favorito
- permitir atualizacao manual do ticker na tela de visualizacao
- voltar ao menu inicial
- sair pelo botao do sistema ou pelo botao `Sair`

## Decisoes de UX aprovadas

- layout com duas telas principais
- favoritos acessiveis na lateral esquerda da tela inicial
- barra de ticker centralizada na tela inicial
- foco inicial em PDF como formato principal de visualizacao

## Decisoes tecnicas aprovadas

- app em Python
- frontend desktop com PySide6
- backend atual reaproveitado
- separacao formal entre contexto de backend e frontend

## Fora de escopo da primeira versao

- chat inteligente
- analise automatica da empresa
- dashboards interativos
- login
- sincronizacao em nuvem
- multiworkspace
