from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, model_validator


class PratoInput(BaseModel):
    nome: str = Field(min_length=3, max_length=100)
    categoria: str = Field(pattern="^(pizza|massa|sobremesa|entrada|salada)$")
    preco: float = Field(gt=0)
    preco_promocional: Optional[float] = Field(default=None, gt=0)
    descricao: Optional[str] = Field(default=None, max_length=500)
    disponivel: bool = True

    @model_validator(mode="after")
    def validar_preco_promocional(self) -> "PratoInput":
        if self.preco_promocional is None:
            return self
        if self.preco_promocional >= self.preco:
            raise ValueError("preco_promocional deve ser menor que preco")
        if self.preco_promocional < self.preco * 0.5:
            raise ValueError("desconto maximo permitido e de 50%")
        return self


class DisponibilidadeInput(BaseModel):
    disponivel: bool


class PratoOutput(BaseModel):
    id: int
    nome: str
    categoria: str
    preco: float
    preco_promocional: Optional[float]
    descricao: Optional[str]
    disponivel: bool
    criado_em: datetime
