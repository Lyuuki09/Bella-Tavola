from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models.orm import PratoORM
from models.pedido import PedidoInput, PedidoOutput

router = APIRouter()

pedidos: list[dict] = []


@router.get("/", response_model=list[PedidoOutput])
async def listar_pedidos() -> list[dict]:
    return pedidos


@router.post("/", response_model=PedidoOutput, status_code=201)
async def criar_pedido(payload: PedidoInput, db: Session = Depends(get_db)) -> dict:
    prato = db.query(PratoORM).filter(PratoORM.id == payload.prato_id).first()
    if not prato:
        raise HTTPException(status_code=404, detail=f"Prato com id {payload.prato_id} nao encontrado")
    if not prato.disponivel:
        raise HTTPException(status_code=400, detail="Prato indisponivel para pedido")

    valor_unitario = float(prato.preco_promocional or prato.preco)
    novo_id = max((p["id"] for p in pedidos), default=0) + 1
    novo_pedido = {
        "id": novo_id,
        "prato_id": payload.prato_id,
        "quantidade": payload.quantidade,
        "valor_unitario": valor_unitario,
        "valor_total": round(valor_unitario * payload.quantidade, 2),
        "status": "recebido",
        "criado_em": datetime.utcnow(),
    }
    pedidos.append(novo_pedido)
    return novo_pedido
