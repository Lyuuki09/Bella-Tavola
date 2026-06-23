# Contributing

## Fluxo recomendado

1. Crie uma branch a partir de `main`.
2. Implemente mudancas pequenas e focadas.
3. Rode lint e testes localmente antes de abrir PR:

```bash
python -m ruff check main.py config.py model_utils.py models routers tests
python -m pytest -q
```

4. Abra Pull Request com contexto, impacto e plano de testes.

## Convencoes

- Manter modularizacao (`routers/`, `models/`, `config.py`).
- Evitar logs com segredos.
- Preferir tipagem explicita e validacoes no contrato de entrada.

## CI

O pipeline em `.github/workflows/ci.yml` valida lint, testes e integridade de modelo.
PRs com pipeline vermelho nao devem ser mergeadas.
