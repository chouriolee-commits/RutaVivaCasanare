from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies import get_current_user
from app.schemas.common import PaginatedResponse
from app.schemas.movimiento_stock import MovimientoStockCreate, MovimientoStockResponse
from app.services import stock_service

router = APIRouter(dependencies=[Depends(get_current_user)])


@router.post(
    "/productos/{producto_id}/movimientos",
    response_model=MovimientoStockResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Movimientos de Stock"],
)
def registrar_movimiento(
    producto_id: int, data: MovimientoStockCreate, db: Session = Depends(get_db)
) -> MovimientoStockResponse:
    """Registra venta/reposición/ajuste y actualiza el stock del producto de forma atómica."""
    movimiento = stock_service.registrar_movimiento(db, producto_id, data)
    return MovimientoStockResponse.model_validate(movimiento)


@router.get(
    "/productos/{producto_id}/movimientos",
    response_model=PaginatedResponse[MovimientoStockResponse],
    tags=["Movimientos de Stock"],
)
def list_movimientos_de_producto(
    producto_id: int,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
) -> PaginatedResponse[MovimientoStockResponse]:
    return stock_service.list_movimientos(db, page, page_size, producto_id=producto_id)


@router.get("/movimientos", response_model=PaginatedResponse[MovimientoStockResponse], tags=["Movimientos de Stock"])
def list_movimientos(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    id_producto: int | None = Query(default=None),
    db: Session = Depends(get_db),
) -> PaginatedResponse[MovimientoStockResponse]:
    return stock_service.list_movimientos(db, page, page_size, producto_id=id_producto)
