from __future__ import annotations

import pytest

@pytest.mark.api
def test_root_deve_retornar_metadados_basicos(client):
    response = client.get("/")
    assert response.status_code == 200
    body = response.json()
    assert body["restaurante"] == "Bella Tavola"
    assert "chef" in body


@pytest.mark.api
def test_listar_pratos_eh_lista(client):
    response = client.get("/pratos")
    assert response.status_code == 200
    body = response.json()
    assert isinstance(body, list)
    assert len(body) >= 2


@pytest.mark.api
@pytest.mark.integration
def test_criar_pedido_valido(client):
    response = client.post("/pedidos", json={"prato_id": 1, "quantidade": 2})
    assert response.status_code == 201
    body = response.json()
    assert body["valor_total"] == 90.0
    assert body["status"] == "recebido"


@pytest.mark.api
def test_criar_pedido_com_prato_inexistente_retorna_404(client):
    response = client.post("/pedidos", json={"prato_id": 999, "quantidade": 1})
    assert response.status_code == 404
    assert "nao encontrado" in response.json()["erro"]


@pytest.mark.api
@pytest.mark.integration
def test_fluxo_reserva_criar_e_cancelar(client, reserva_data_futura_iso):
    payload = {
        "mesa": 4,
        "nome": "Cliente Teste",
        "pessoas": 2,
        "data_hora": reserva_data_futura_iso,
    }
    criar = client.post("/reservas", json=payload)
    assert criar.status_code == 201
    reserva_id = criar.json()["id"]

    cancelar = client.delete(f"/reservas/{reserva_id}")
    assert cancelar.status_code == 200
    assert cancelar.json()["mensagem"] == "Reserva cancelada com sucesso"


@pytest.mark.api
@pytest.mark.parametrize(
    ("payload", "status_esperado"),
    [
        ({"disponivel": False}, 200),
        ({"disponivel": True}, 200),
        ({"disponivel": "sim"}, 422),
    ],
)
def test_atualizar_disponibilidade_validacoes(client, payload, status_esperado):
    response = client.put("/pratos/1/disponibilidade", json=payload)
    assert response.status_code == status_esperado


@pytest.mark.api
@pytest.mark.parametrize(
    "payload",
    [
        {"nome": "Ravioli", "categoria": "massa", "preco": 70, "preco_promocional": 70},
        {"nome": "Ravioli", "categoria": "massa", "preco": 70, "preco_promocional": 30},
    ],
)
def test_criar_prato_rejeita_preco_promocional_invalido(client, payload):
    response = client.post("/pratos", json=payload)
    assert response.status_code == 422
