from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class PedidoInput(BaseModel):
    prato_id: int = Field(ge=1)
    quantidade: int = Field(ge=1, le=20)


class PedidoOutput(BaseModel):
    id: int
    prato_id: int
    quantidade: int
    valor_unitario: float
    valor_total: float
    status: Literal["recebido", "em_preparo", "enviado", "entregue"] = "recebido"
    criado_em: datetime
