# Config

Esta pasta centraliza configuracoes tecnicas do coletor base.

O que o codigo faz:
- define timeouts de requisicao
- define codigos de series do Banco Central
- define a meta oficial de inflacao usada no projeto
- define a base URL da API Focus/OData

Arquivo:
- `settings.py`: configuracoes centrais do coletor

Exemplo de entrada:
```python
from src.config.settings import settings
```

Exemplo de uso:
```python
settings.bcb_series["selic_atual"]
settings.inflation_target
```

Exemplo de saida:
```python
432
3.0
```
