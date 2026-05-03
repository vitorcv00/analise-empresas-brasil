# Implementacao: Atualizacao automatica de commodities

## Objetivo

Adicionar no backend uma rotina de atualizacao diaria para commodities estrategicas:
- petroleo
- ouro
- prata

A rotina foi projetada para manter um snapshot local atualizado sem bloquear a abertura do app.

## Componentes adicionados

### 1. `app/bridge/commodities_repository.py`

Responsavel por persistir e carregar o snapshot local em JSON:
- caminho padrao: `data/_app/commodities_snapshot.json`
- garante criacao do diretorio de persistencia
- retorna dicionario vazio para arquivo ausente/invalido

### 2. `app/bridge/commodities_service.py`

Responsavel pela regra de atualizacao e coleta dos precos.

Regras principais:
- timezone de referencia: `America/Sao_Paulo`
- atualiza no maximo 1 vez por dia
- so tenta atualizar apos `08:00`
- simbolos consultados via `yfinance`:
  - `BZ=F` (petroleo)
  - `GC=F` (ouro)
  - `SI=F` (prata)

Formato salvo:
- `trading_date`
- `updated_at`
- `timezone`
- `prices` (valor, moeda, unidade e data de referencia por commodity)

### 3. Integracao em `app/bridge/backend_service.py`

A ponte de backend passou a:
- instanciar `CommoditiesService`
- executar `ensure_daily_update()` na inicializacao
- ignorar falhas de rede nessa etapa para nao impedir o app de abrir
- expor `get_commodities_snapshot()` para consumo na UI

## Comportamento de falha

- Se a consulta remota falhar na inicializacao, o app continua abrindo normalmente.
- Se nao houver historico para um simbolo, o snapshot registra o ativo com campos nulos.

## Impacto esperado

- Dados macro de commodities mais consistentes para exibicao na UI.
- Menor acoplamento entre coleta de ticker e atualizacao de commodities.
- Persistencia local simples, auditavel e de baixo custo operacional.
