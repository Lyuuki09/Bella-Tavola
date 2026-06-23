# Bella Tavola API + ML

API FastAPI modular para o restaurante Bella Tavola com camada de ML para predição de fraude, testes automatizados e pipeline de CI.

## Visao geral

O sistema combina dois blocos principais:

- **API de restaurante**: dominios de pratos, bebidas, pedidos e reservas.
- **API de ML**: endpoint de inferencia (`/ml/predict`) com healthcheck (`/ml/health`) e carregamento de modelo via `model_utils.py`.

## Estrutura do projeto

Arquitetura organizada por responsabilidade:

- `main.py`: bootstrap da aplicacao, handlers globais e composicao de routers.
- `routers/`: endpoints por dominio (`pratos`, `bebidas`, `pedidos`, `reservas`, `predict`).
- `models/`: contratos Pydantic de entrada e saida.
- `config.py`: configuracao por variaveis de ambiente.
- `tests/`: testes organizados em `tests/api` e `tests/models`.
- `.github/workflows/ci.yml`: pipeline de lint, testes e validacao de modelo.
- `Dockerfile` + `docker-compose.yml`: empacotamento e execucao local com containers.

## Pre-requisitos

- Docker Desktop (ou Docker Engine + Compose plugin)
- Python 3.11+ (para execucao local sem Docker)

## Configuracao de ambiente

1. Copie o arquivo de exemplo:

```bash
cp .env.example .env
```

No Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

2. Ajuste os valores no `.env` conforme seu ambiente (especialmente `MODEL_REPO_ID` e `HF_TOKEN`, se usar Hugging Face Hub).

## Como rodar com Docker Compose

Subir o ambiente:

```bash
docker compose up --build
```

Parar o ambiente:

```bash
docker compose down
```

API disponivel em:

- [http://localhost:8000](http://localhost:8000)
- [http://localhost:8000/docs](http://localhost:8000/docs)

## Build manual da imagem

```bash
docker build -t bella-tavola-api:latest .
```

## Como testar

### Local (Python)

```bash
python -m pytest -q
```

Testes seletivos por marker:

```bash
python -m pytest -q -m "api and not ml"
python -m pytest -q -m "ml"
python -m pytest -q -m "integration"
```

### Durante o build Docker

O stage `builder` do `Dockerfile` executa:

```bash
pytest -q -m "not integration"
```

Ou seja, a imagem de runtime so e gerada se os testes nao-integracao passarem.

## Pipeline CI

O CI em `.github/workflows/ci.yml` roda automaticamente a cada `push` e `pull_request`, com:

- lint com Ruff
- testes API e ML por markers
- validacao de integridade do modelo
- cache de artefatos Hugging Face
- verificacao de `HF_TOKEN` via secrets

## Observacoes de configuracao

- O `docker-compose.yml` usa `env_file: .env`; portanto, garanta que esse arquivo exista antes de subir.
- Os defaults definidos em `docker-compose.yml` e `config.py` sao compativeis com `.env.example`.
