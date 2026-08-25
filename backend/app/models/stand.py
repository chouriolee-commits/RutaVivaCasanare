import enum
from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy import Date, Enum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.models.empresario import Empresario
    from app.models.evento import Evento
    from app.models.producto import Producto


class EstadoStandEnum(str, enum.Enum):
    pendiente = "pendiente"
    confirmado = "confirmado"
    cancelado = "cancelado"


class Stand(Base):
    """Espacio que un empresario ocupa dentro de un evento."""

    __tablename__ = "stands"

    id_stand: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    id_evento: Mapped[int] = mapped_column(ForeignKey("eventos.id_evento", ondelete="CASCADE"), nullable=False)
    id_empresario: Mapped[int] = mapped_column(
        ForeignKey("empresarios.id_empresario", ondelete="CASCADE"), nullable=False
    )
    ubicacion: Mapped[str | None] = mapped_column(String(100), nullable=True)
    fecha_registro: Mapped[date | None] = mapped_column(Date, nullable=True)
    estado: Mapped[EstadoStandEnum] = mapped_column(
        Enum(EstadoStandEnum, native_enum=True), default=EstadoStandEnum.pendiente
    )

    evento: Mapped["Evento"] = relationship(back_populates="stands")
    empresario: Mapped["Empresario"] = relationship(back_populates="stands")
    productos: Mapped[list["Producto"]] = relationship(back_populates="stand", cascade="all, delete-orphan")
