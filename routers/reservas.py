from typing import Optional

from fastapi import APIRouter, HTTPException

from models.reserva import ReservaInput, ReservaOutput

router = APIRouter()

reservas: list[dict] = []


@router.post("/", response_model=ReservaOutput, status_code=201)
async def criar_reserva(payload: ReservaInput) -> dict:
    conflito = any(
        r["mesa"] == payload.mesa
        and r["ativa"]
        and r["data_hora"].date() == payload.data_hora.date()
        for r in reservas
    )
    if conflito:
        raise HTTPException(
            status_code=400,
            detail=f"Mesa {payload.mesa} ja possui reserva ativa para essa data",
        )

    novo_id = max((r["id"] for r in reservas), default=0) + 1
    nova_reserva = {"id": novo_id, "ativa": True, **payload.model_dump()}
    reservas.append(nova_reserva)
    return nova_reserva


@router.get("/", response_model=list[ReservaOutput])
async def listar_reservas(apenas_ativas: Optional[bool] = None) -> list[dict]:
    if apenas_ativas is None:
        return reservas
    return [r for r in reservas if r["ativa"] is apenas_ativas]


@router.get("/{reserva_id}", response_model=ReservaOutput)
async def buscar_reserva(reserva_id: int) -> dict:
    reserva = next((r for r in reservas if r["id"] == reserva_id), None)
    if not reserva:
        raise HTTPException(status_code=404, detail=f"Reserva com id {reserva_id} nao encontrada")
    return reserva


@router.delete("/{reserva_id}")
async def cancelar_reserva(reserva_id: int) -> dict:
    reserva = next((r for r in reservas if r["id"] == reserva_id), None)
    if not reserva:
        raise HTTPException(status_code=404, detail=f"Reserva com id {reserva_id} nao encontrada")
    reserva["ativa"] = False
    return {"mensagem": "Reserva cancelada com sucesso", "reserva_id": reserva_id}
