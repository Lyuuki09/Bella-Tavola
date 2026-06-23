from __future__ import annotations

from typing import Any

from fastapi import APIRouter
from pydantic import BaseModel, Field

from config import settings
from model_utils import load_model

router = APIRouter()
_model: Any = None


def get_model(force_download: bool = False) -> Any:
    global _model
    if _model is None or force_download:
        _model = load_model(
            repo_id=settings.model_repo_id,
            filename=settings.model_filename,
            force_download=force_download,
        )
    return _model


class PredictInput(BaseModel):
    valor_transacao: float = Field(gt=0, description="Valor em reais")
    hora_transacao: int = Field(ge=0, le=23, description="Hora do dia")
    distancia_ultima_compra: float = Field(ge=0, description="Distancia em km")
    tentativas_senha: int = Field(ge=1, description="Tentativas de senha")
    pais_diferente: int = Field(ge=0, le=1, description="1 se pais diferente")


class PredictOutput(BaseModel):
    prediction: int
    probability: float
    label: str
    model_version: str


@router.get("/health")
async def ml_health() -> dict:
    model = get_model()
    ready = model is not None
    return {
        "status": "ok" if ready else "unavailable",
        "model_loaded": ready,
        "model_version": settings.model_version,
        "repo_id": settings.model_repo_id or "local",
    }


@router.post("/predict", response_model=PredictOutput)
async def predict(payload: PredictInput) -> PredictOutput:
    model = get_model()
    features = [[
        payload.valor_transacao,
        payload.hora_transacao,
        payload.distancia_ultima_compra,
        payload.tentativas_senha,
        payload.pais_diferente,
    ]]

    prediction = int(model.predict(features)[0])
    probability = float(model.predict_proba(features)[0][1])
    label = "fraude" if prediction == 1 else "legitimo"

    return PredictOutput(
        prediction=prediction,
        probability=round(probability, 6),
        label=label,
        model_version=settings.model_version,
    )
