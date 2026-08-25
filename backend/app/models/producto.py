from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import DECIMAL, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.models.movimiento_stock import MovimientoStock
    from app.models.stand import Stand


class Producto(Base):
    """Producto que un stand ofrece, con control de inventario."""

    __tablename__ = "productos"

    id_producto: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    id_stand: Mapped[int] = mapped_column(ForeignKey("stands.id_stand", ondelete="CASCADE"), nullable=False)
    nombre: Mapped[str] = mapped_column(String(150), nullable=False)
    descripcion: Mapped[str | None] = mapped_column(Text, nullable=True)
    stock_inicial: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    stock_actual: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    precio: Mapped[Decimal | None] = mapped_column(DECIMAL(10, 2), nullable=True)

    stand: Mapped["Stand"] = relationship(back_populates="productos")
    movimientos: Mapped[list["MovimientoStock"]] = relationship(
        back_populates="producto",
        cascade="all, delete-orphan",
        order_by="MovimientoStock.fecha_hora, MovimientoStock.id_movimiento",
    )
