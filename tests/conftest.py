from __future__ import annotations

import os
from copy import deepcopy
from datetime import datetime

import pytest
from fastapi.testclient import TestClient

# SQLite em memoria para testes — nao depende de PostgreSQL no CI.
os.environ["DATABASE_URL"] = "sqlite:///:memory:"

from database import Base, SessionLocal, engine, init_db, reset_pratos  # noqa: E402
from main import app  # noqa: E402
from routers import pedidos, reservas  # noqa: E402
from routers.predict import get_model  # noqa: E402


@pytest.fixture()
def client() -> TestClient:
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture(autouse=True)
def reset_state() -> None:
    init_db()
    db = SessionLocal()
    try:
        reset_pratos(db)
    finally:
        db.close()

    pedidos_original = deepcopy(pedidos.pedidos)
    reservas_original = deepcopy(reservas.reservas)

    yield

    db = SessionLocal()
    try:
        reset_pratos(db)
    finally:
        db.close()

    pedidos.pedidos.clear()
    pedidos.pedidos.extend(pedidos_original)
    reservas.reservas.clear()
    reservas.reservas.extend(reservas_original)


@pytest.fixture(scope="session", autouse=True)
def teardown_database() -> None:
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def payload_predict_valido() -> dict:
    return {
        "valor_transacao": 250.0,
        "hora_transacao": 2,
        "distancia_ultima_compra": 12.5,
        "tentativas_senha": 3,
        "pais_diferente": 1,
    }


@pytest.fixture()
def reserva_data_futura_iso() -> str:
    return datetime(2099, 1, 1, 19, 0, 0).isoformat()


@pytest.fixture()
def model_instance():
    return get_model()
