from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.models.stand import Stand


class Empresario(Base):
    """Negocio/vendedor que puede tomar stands en eventos."""

    __tablename__ = "empresarios"

    id_empresario: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nombre_negocio: Mapped[str] = mapped_column(String(150), nullable=False)
    propietario: Mapped[str] = mapped_column(String(150), nullable=False)
    telefono: Mapped[str | None] = mapped_column(String(20), nullable=True)
    email: Mapped[str | None] = mapped_column(String(150), nullable=True)
    tipo_producto: Mapped[str | None] = mapped_column(String(100), nullable=True)

    stands: Mapped[list["Stand"]] = relationship(back_populates="empresario")
