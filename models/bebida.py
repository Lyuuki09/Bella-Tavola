# bebidas

from datetime import datetime

from pydantic import BaseModel, Field


class BebidaInput(BaseModel):
    nome: str = Field(min_length=2, max_length=100)
    tipo: str = Field(pattern="^(agua|refrigerante|suco|vinho|cerveja|drinque)$")
    preco: float = Field(gt=0)
    alcoolica: bool
    volume_ml: int = Field(gt=0, le=2000)


class BebidaOutput(BaseModel):
    id: int
    nome: str
    tipo: str
    preco: float
    alcoolica: bool
    volume_ml: int
    criado_em: datetime
