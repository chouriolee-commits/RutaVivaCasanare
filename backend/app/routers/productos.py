from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies import get_current_user
from app.schemas.common import PaginatedResponse
from app.schemas.producto import ProductoCreate, ProductoResponse, ProductoUpdate
from app.services import producto_service

router = APIRouter(dependencies=[Depends(get_current_user)])


@router.get("", response_model=PaginatedResponse[ProductoResponse])
def list_productos(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    id_stand: int | None = Query(default=None),
    db: Session = Depends(get_db),
) -> PaginatedResponse[ProductoResponse]:
    return producto_service.list_productos(db, page, page_size, id_stand)


@router.get("/{producto_id}", response_model=ProductoResponse)
def get_producto(producto_id: int, db: Session = Depends(get_db)) -> ProductoResponse:
    producto = producto_service.get_producto_or_404(db, producto_id)
    return ProductoResponse.model_validate(producto)


@router.post("", response_model=ProductoResponse, status_code=status.HTTP_201_CREATED)
def create_producto(data: ProductoCreate, db: Session = Depends(get_db)) -> ProductoResponse:
    producto = producto_service.create_producto(db, data)
    return ProductoResponse.model_validate(producto)


@router.put("/{producto_id}", response_model=ProductoResponse)
def update_producto(producto_id: int, data: ProductoUpdate, db: Session = Depends(get_db)) -> ProductoResponse:
    producto = producto_service.get_producto_or_404(db, producto_id)
    producto = producto_service.update_producto(db, producto, data)
    return ProductoResponse.model_validate(producto)


@router.delete("/{producto_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_producto(producto_id: int, db: Session = Depends(get_db)) -> None:
    producto = producto_service.get_producto_or_404(db, producto_id)
    producto_service.delete_producto(db, producto)
