from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models.orm import PratoORM
from models.prato import DisponibilidadeInput, PratoInput, PratoOutput

router = APIRouter()


@router.get("/", response_model=list[PratoOutput])
async def listar_pratos(
    categoria: Optional[str] = None,
    preco_maximo: Optional[float] = None,
    apenas_disponiveis: bool = False,
    db: Session = Depends(get_db),
) -> list[dict]:
    query = db.query(PratoORM)

    if categoria:
        query = query.filter(PratoORM.categoria == categoria)
    if preco_maximo is not None:
        query = query.filter(PratoORM.preco <= preco_maximo)
    if apenas_disponiveis:
        query = query.filter(PratoORM.disponivel.is_(True))

    return [prato.to_dict() for prato in query.all()]


@router.get("/{prato_id}", response_model=PratoOutput)
async def buscar_prato(prato_id: int, db: Session = Depends(get_db)) -> dict:
    prato = db.query(PratoORM).filter(PratoORM.id == prato_id).first()
    if not prato:
        raise HTTPException(status_code=404, detail=f"Prato com id {prato_id} nao encontrado")
    return prato.to_dict()


@router.post("/", response_model=PratoOutput, status_code=201)
async def criar_prato(payload: PratoInput, db: Session = Depends(get_db)) -> dict:
    novo_prato = PratoORM(criado_em=datetime.utcnow(), **payload.model_dump())
    db.add(novo_prato)
    db.commit()
    db.refresh(novo_prato)
    return novo_prato.to_dict()


@router.put("/{prato_id}/disponibilidade", response_model=PratoOutput)
async def atualizar_disponibilidade(
    prato_id: int,
    payload: DisponibilidadeInput,
    db: Session = Depends(get_db),
) -> dict:
    prato = db.query(PratoORM).filter(PratoORM.id == prato_id).first()
    if not prato:
        raise HTTPException(status_code=404, detail=f"Prato com id {prato_id} nao encontrado")
    prato.disponivel = payload.disponivel
    db.commit()
    db.refresh(prato)
    return prato.to_dict()
