from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class ProductoBase(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=150)
    descripcion: str | None = None
    precio: Decimal | None = Field(default=None, ge=0, max_digits=10, decimal_places=2)


class ProductoCreate(ProductoBase):
    id_stand: int = Field(..., gt=0)
    stock_inicial: int = Field(default=0, ge=0)


class ProductoUpdate(BaseModel):
    """Actualiza datos descriptivos del producto. El inventario (stock_actual)
    solo cambia registrando movimientos — nunca por edición directa."""

    nombre: str | None = Field(default=None, min_length=1, max_length=150)
    descripcion: str | None = None
    precio: Decimal | None = Field(default=None, ge=0, max_digits=10, decimal_places=2)


class ProductoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_producto: int
    id_stand: int
    nombre: str
    descripcion: str | None
    stock_inicial: int
    stock_actual: int
    precio: Decimal | None
