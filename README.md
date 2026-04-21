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

## Execucao completa

### 1. Preparar ambiente

No WSL (ou Linux/macOS), com ambiente `mvp_agentes`:

```bash
pip install -r requirements.txt
```

### 2. Rodar coletor via terminal (CLI)

```bash
python -m src.main BBAS3
```

### 3. Rodar app desktop (PySide6)

A partir da raiz do projeto:

```bash
python3 -m app.main
```

Importante:
- Rode da raiz para manter imports como `app.*`.
- O app salva estado local em `data/_app/` (favoritos, cache de coleta, snapshots macro).

### 4. Gerar executavel Windows (.exe)

O `.exe` deve ser gerado com Python do Windows (nao via Python do WSL):

```cmd
cd /d "C:\Users\Vitor\Documents\seilalol\MVP - Analise Empresas" && py -m pip install -U pyinstaller && py -m PyInstaller --noconfirm --windowed --onedir --name AnaliseEmpresas --collect-all PySide6 app\main.py
```

Saida esperada:

```text
dist\AnaliseEmpresas\AnaliseEmpresas.exe
```

## Observacao

O bloco macro usa fontes oficiais do Banco Central quando disponiveis.
O bloco corporativo usa busca deterministica em links de RI conhecidos no cadastro inicial da empresa.
