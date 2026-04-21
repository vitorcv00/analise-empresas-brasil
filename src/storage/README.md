# Storage

Esta pasta concentra utilitarios para salvar arquivos baixados localmente.

O que o codigo faz:
- cria a estrutura `data/<ticker>/`
- salva documentos corporativos baixados
- padroniza nomes de arquivos para facilitar rastreio
- gera PDFs simples produzidos pelo proprio projeto

Arquivos:
- `downloads.py`: helpers para paths e escrita binaria
- `pdf_writer.py`: geracao simples de PDF textual

Exemplo de entrada:
```python
ticker = "BBAS3"
item = "balanco_recente"
```

Exemplo de saida:
```text
data/BBAS3/balanco_recente_2025-12-31_v1.pdf
```
