from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.exceptions import NotFoundError
from app.models.producto import Producto
from app.schemas.common import PaginatedResponse
from app.schemas.producto import ProductoCreate, ProductoResponse, ProductoUpdate
from app.services.stand_service import get_stand_or_404


def get_producto_or_404(db: Session, producto_id: int) -> Producto:
    producto = db.get(Producto, producto_id)
    if producto is None:
        raise NotFoundError(f"Producto {producto_id} no encontrado.")
    return producto


def list_productos(
    db: Session, page: int, page_size: int, id_stand: int | None = None
) -> PaginatedResponse[ProductoResponse]:
    stmt = select(Producto)
    if id_stand is not None:
        stmt = stmt.where(Producto.id_stand == id_stand)

    total = db.scalar(select(func.count()).select_from(stmt.subquery())) or 0
    items = db.scalars(stmt.order_by(Producto.id_producto).offset((page - 1) * page_size).limit(page_size)).all()

    return PaginatedResponse[ProductoResponse](
        items=[ProductoResponse.model_validate(item) for item in items],
        total=total,
        page=page,
        page_size=page_size,
    )


def create_producto(db: Session, data: ProductoCreate) -> Producto:
    get_stand_or_404(db, data.id_stand)  # valida existencia antes de insertar

    producto = Producto(**data.model_dump(), stock_actual=data.stock_inicial)
    db.add(producto)
    db.commit()
    db.refresh(producto)
    return producto


def update_producto(db: Session, producto: Producto, data: ProductoUpdate) -> Producto:
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(producto, field, value)
    db.commit()
    db.refresh(producto)
    return producto


def delete_producto(db: Session, producto: Producto) -> None:
    db.delete(producto)
    db.commit()
