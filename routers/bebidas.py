# bebidas

from datetime import datetime

from fastapi import APIRouter, HTTPException

from models.bebida import BebidaInput, BebidaOutput

router = APIRouter()

bebidas: list[dict] = [
    {
        "id": 1,
        "nome": "Agua Mineral",
        "tipo": "agua",
        "preco": 8.0,
        "alcoolica": False,
        "volume_ml": 500,
        "criado_em": datetime(2024, 1, 1, 0, 0, 0),
    }
]


@router.get("/", response_model=list[BebidaOutput])
async def listar_bebidas() -> list[dict]:
    return bebidas


@router.get("/{bebida_id}", response_model=BebidaOutput)
async def buscar_bebida(bebida_id: int) -> dict:
    bebida = next((b for b in bebidas if b["id"] == bebida_id), None)
    if not bebida:
        raise HTTPException(status_code=404, detail=f"Bebida com id {bebida_id} nao encontrada")
    return bebida


@router.post("/", response_model=BebidaOutput, status_code=201)
async def criar_bebida(payload: BebidaInput) -> dict:
    novo_id = max((b["id"] for b in bebidas), default=0) + 1
    nova_bebida = {"id": novo_id, "criado_em": datetime.utcnow(), **payload.model_dump()}
    bebidas.append(nova_bebida)
    return nova_bebida
