import enum
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.models.producto import Producto


class TipoMovimientoEnum(str, enum.Enum):
    venta = "venta"
    reposicion = "reposicion"
    ajuste = "ajuste"


class MovimientoStock(Base):
    """Registro histórico e inmutable de cada cambio de inventario."""

    __tablename__ = "movimientos_stock"

    id_movimiento: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    id_producto: Mapped[int] = mapped_column(ForeignKey("productos.id_producto", ondelete="CASCADE"), nullable=False)
    cantidad_cambio: Mapped[int] = mapped_column(Integer, nullable=False)
    tipo_movimiento: Mapped[TipoMovimientoEnum] = mapped_column(Enum(TipoMovimientoEnum, native_enum=True), nullable=False)
    fecha_hora: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    producto: Mapped["Producto"] = relationship(back_populates="movimientos")
