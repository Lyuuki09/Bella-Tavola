from datetime import datetime

from pydantic import BaseModel, Field, field_validator

from config import settings


class ReservaInput(BaseModel):
    mesa: int = Field(ge=1, le=settings.max_mesas)
    nome: str = Field(min_length=2, max_length=100)
    pessoas: int = Field(ge=1, le=settings.max_pessoas_por_mesa)
    data_hora: datetime

    @field_validator("data_hora")
    @classmethod
    def data_deve_ser_futura(cls, value: datetime) -> datetime:
        now = datetime.now(tz=value.tzinfo)
        if value <= now:
            raise ValueError("data_hora deve ser futura")
        return value


class ReservaOutput(BaseModel):
    id: int
    mesa: int
    nome: str
    pessoas: int
    data_hora: datetime
    ativa: bool
