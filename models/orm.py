from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, DateTime, Float, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class PratoORM(Base):
    __tablename__ = "pratos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nome: Mapped[str] = mapped_column(String(100), nullable=False)
    categoria: Mapped[str] = mapped_column(String(50), nullable=False)
    preco: Mapped[float] = mapped_column(Float, nullable=False)
    preco_promocional: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    descricao: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    disponivel: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    criado_em: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "nome": self.nome,
            "categoria": self.categoria,
            "preco": self.preco,
            "preco_promocional": self.preco_promocional,
            "descricao": self.descricao,
            "disponivel": self.disponivel,
            "criado_em": self.criado_em,
        }
