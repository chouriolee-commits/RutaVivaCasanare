import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.exceptions import register_exception_handlers
from app.routers import auth, empresarios, eventos, movimientos_stock, productos, stands, usuarios

logging.basicConfig(
    level=logging.WARNING if settings.is_production else logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

app = FastAPI(
    title="Casanare en Movimiento — API",
    description="API de gestión de eventos culturales, empresarios, stands, productos e inventario.",
    version="1.0.0",
    docs_url=None if settings.is_production else "/docs",
    redoc_url=None if settings.is_production else "/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

register_exception_handlers(app)

app.include_router(auth.router, prefix="/api/v1/auth", tags=["Autenticación"])
app.include_router(usuarios.router, prefix="/api/v1/usuarios", tags=["Usuarios"])
app.include_router(empresarios.router, prefix="/api/v1/empresarios", tags=["Empresarios"])
app.include_router(eventos.router, prefix="/api/v1/eventos", tags=["Eventos"])
app.include_router(stands.router, prefix="/api/v1/stands", tags=["Stands"])
app.include_router(productos.router, prefix="/api/v1/productos", tags=["Productos"])
app.include_router(movimientos_stock.router, prefix="/api/v1", tags=["Movimientos de Stock"])


@app.get("/health", tags=["Sistema"])
def health() -> dict[str, str]:
    return {"status": "ok", "version": "1.0.0"}
