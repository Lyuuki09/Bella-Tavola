from __future__ import annotations

import pytest

@pytest.mark.ml
@pytest.mark.integration
def test_ml_health_disponivel(client):
    response = client.get("/ml/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["model_loaded"] is True


@pytest.mark.ml
@pytest.mark.integration
def test_ml_predict_payload_valido(client, payload_predict_valido):
    response = client.post("/ml/predict", json=payload_predict_valido)
    assert response.status_code == 200
    body = response.json()
    assert "prediction" in body
    assert "probability" in body
    assert "label" in body
    assert body["model_version"]


@pytest.mark.ml
@pytest.mark.parametrize(
    "payload",
    [
        {
            "valor_transacao": -10,
            "hora_transacao": 50,
            "distancia_ultima_compra": -1,
            "tentativas_senha": 0,
            "pais_diferente": 2,
        },
        {
            "valor_transacao": 100,
            "hora_transacao": 24,
            "distancia_ultima_compra": 5,
            "tentativas_senha": 1,
            "pais_diferente": 0,
        },
    ],
)
def test_ml_predict_payload_invalido_retorna_422(client, payload):
    response = client.post("/ml/predict", json=payload)
    assert response.status_code == 422
