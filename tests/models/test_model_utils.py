from __future__ import annotations

import pytest

from model_utils import LocalFallbackModel, load_model


@pytest.mark.ml
def test_load_model_sem_repo_retorna_fallback():
    model = load_model(repo_id="")
    assert model is not None
    assert hasattr(model, "predict")
    assert hasattr(model, "predict_proba")


@pytest.mark.ml
@pytest.mark.parametrize(
    "features",
    [
        [[250.0, 2, 12.5, 3, 1]],
        [[20.0, 15, 1.0, 1, 0]],
    ],
)
def test_fallback_predict_proba_fica_no_intervalo(features):
    model = LocalFallbackModel()
    proba = model.predict_proba(features)[0][1]
    assert 0.0 <= proba <= 1.0


@pytest.mark.ml
@pytest.mark.integration
def test_fallback_predict_retorna_binario():
    model = LocalFallbackModel()
    features = [[250.0, 2, 12.5, 3, 1]]
    pred = model.predict(features)[0]
    assert pred in {0, 1}
