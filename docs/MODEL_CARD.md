# Model Card - Bella Tavola Fraud Classifier

## Visao geral

Este modelo classifica risco de fraude em transacoes com base em cinco features:

- `valor_transacao`
- `hora_transacao`
- `distancia_ultima_compra`
- `tentativas_senha`
- `pais_diferente`

## Uso na API

- Endpoint: `POST /ml/predict`
- Healthcheck: `GET /ml/health`
- Loader: `model_utils.load_model(force_download=False)`

## Versao e rastreabilidade

- Artefato esperado: `model.pkl`
- Versao em runtime: variavel `MODEL_VERSION`
- Repositorio do modelo: variavel `MODEL_REPO_ID`

## Limitacoes

- O fallback local e heuristico e serve apenas para garantir disponibilidade da API em ambiente de desenvolvimento.
- Para validacao de negocio, prefira sempre o artefato versionado no Hugging Face Hub.

## Consideracoes de seguranca

- Nunca commitar tokens de acesso.
- Em CI, usar `HF_TOKEN` via secrets do GitHub Actions.
