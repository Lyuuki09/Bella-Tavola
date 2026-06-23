from __future__ import annotations

from collections.abc import Generator
from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker
from sqlalchemy.pool import StaticPool

from config import settings


def _engine_connect_args() -> dict:
    if settings.database_url.startswith("sqlite"):
        return {"check_same_thread": False}
    return {}


def _engine_kwargs() -> dict:
    kwargs: dict = {
        "connect_args": _engine_connect_args(),
        "pool_pre_ping": not settings.database_url.startswith("sqlite"),
    }
    if settings.database_url in {"sqlite:///:memory:", "sqlite://"}:
        kwargs["poolclass"] = StaticPool
    return kwargs


engine = create_engine(settings.database_url, **_engine_kwargs())
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    from models.orm import PratoORM  # noqa: F401 — registra o modelo no metadata

    Base.metadata.create_all(bind=engine)


SEED_PRATOS: list[dict] = [
    {
        "id": 1,
        "nome": "Margherita",
        "categoria": "pizza",
        "preco": 45.0,
        "preco_promocional": None,
        "descricao": "Molho de tomate, muzzarella e manjericao.",
        "disponivel": True,
        "criado_em": datetime(2024, 1, 1, 0, 0, 0),
    },
    {
        "id": 2,
        "nome": "Carbonara",
        "categoria": "massa",
        "preco": 52.0,
        "preco_promocional": None,
        "descricao": "Massa fresca com molho carbonara.",
        "disponivel": True,
        "criado_em": datetime(2024, 1, 1, 0, 0, 0),
    },
]


def seed_pratos_if_empty(db: Session) -> None:
    from models.orm import PratoORM

    if db.query(PratoORM).count() > 0:
        return

    for dados in SEED_PRATOS:
        db.add(PratoORM(**dados))
    db.commit()


def reset_pratos(db: Session) -> None:
    from models.orm import PratoORM

    db.query(PratoORM).delete()
    db.commit()
    for dados in SEED_PRATOS:
        db.add(PratoORM(**dados))
    db.commit()
