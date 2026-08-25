import enum
from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy import Date, Enum, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.models.stand import Stand


class EstadoEventoEnum(str, enum.Enum):
    planeado = "planeado"
    en_curso = "en_curso"
    finalizado = "finalizado"


class Evento(Base):
    """Evento cultural (feria) que agrupa stands."""

    __tablename__ = "eventos"

    id_evento: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(150), nullable=False)
    descripcion: Mapped[str | None] = mapped_column(Text, nullable=True)
    fecha_inicio: Mapped[date] = mapped_column(Date, nullable=False)
    fecha_fin: Mapped[date] = mapped_column(Date, nullable=False)
    ubicacion: Mapped[str | None] = mapped_column(String(200), nullable=True)
    estado: Mapped[EstadoEventoEnum] = mapped_column(
        Enum(EstadoEventoEnum, native_enum=True), default=EstadoEventoEnum.planeado
    )

    stands: Mapped[list["Stand"]] = relationship(back_populates="evento", cascade="all, delete-orphan")
