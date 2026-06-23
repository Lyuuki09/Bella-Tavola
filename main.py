from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from config import settings
from database import SessionLocal, init_db, seed_pratos_if_empty
from routers import bebidas, pedidos, pratos, predict, reservas


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    db = SessionLocal()
    try:
        seed_pratos_if_empty(db)
    finally:
        db.close()
    yield


app = FastAPI(
    title=settings.app_name,
    description=settings.app_description,
    version=settings.app_version,
    debug=settings.debug,
    lifespan=lifespan,
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    return JSONResponse(
        status_code=422,
        content={
            "erro": "Dados de entrada invalidos",
            "status": 422,
            "path": str(request.url.path),
            "detalhes": [
                {"campo": " -> ".join(str(loc) for loc in e["loc"]), "mensagem": e["msg"]}
                for e in exc.errors()
            ],
        },
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "erro": exc.detail,
            "status": exc.status_code,
            "path": str(request.url.path),
        },
    )


@app.get("/", tags=["Geral"])
async def raiz() -> dict:
    return {
        "restaurante": "Bella Tavola",
        "mensagem": "Bem-vindo a API do Bella Tavola",
        "chef": "Marco Rossi",
        "cidade": "Sao Paulo",
        "especialidade": "Massas artesanais",
    }


@app.get("/health", tags=["Geral"])
async def health() -> dict:
    return {"status": "ok", "app": settings.app_name, "version": settings.app_version}


app.include_router(pratos.router, prefix="/pratos", tags=["Pratos"])
app.include_router(bebidas.router, prefix="/bebidas", tags=["Bebidas"])
app.include_router(pedidos.router, prefix="/pedidos", tags=["Pedidos"])
app.include_router(reservas.router, prefix="/reservas", tags=["Reservas"])
app.include_router(predict.router, prefix="/ml", tags=["ML"])
