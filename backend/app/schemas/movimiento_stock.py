from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.models.movimiento_stock import TipoMovimientoEnum


class MovimientoStockCreate(BaseModel):
    """
    Registra un cambio de inventario. Semántica de `cantidad_cambio`:
      - venta / reposicion: magnitud positiva de unidades (la dirección la
        determina `tipo_movimiento`: venta resta, reposicion suma).
      - ajuste: delta con signo aplicado directo al stock (positivo o
        negativo, pero nunca cero).
    """

    cantidad_cambio: int
    tipo_movimiento: TipoMovimientoEnum

    @model_validator(mode="after")
    def validar_cantidad(self) -> "MovimientoStockCreate":
        if self.tipo_movimiento in (TipoMovimientoEnum.venta, TipoMovimientoEnum.reposicion):
            if self.cantidad_cambio <= 0:
                raise ValueError(f"Para '{self.tipo_movimiento.value}', cantidad_cambio debe ser un entero positivo.")
        elif self.cantidad_cambio == 0:
            raise ValueError("Para 'ajuste', cantidad_cambio no puede ser cero.")
        return self


class MovimientoStockResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_movimiento: int
    id_producto: int
    cantidad_cambio: int
    tipo_movimiento: TipoMovimientoEnum
    fecha_hora: datetime
    stock_resultante: int | None = Field(
        default=None,
        description="stock_actual del producto justo después de este movimiento. "
        "Solo se calcula al registrar el movimiento; en listados históricos es null.",
    )
