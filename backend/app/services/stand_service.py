from datetime import date

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.exceptions import NotFoundError
from app.models.stand import EstadoStandEnum, Stand
from app.schemas.common import PaginatedResponse
from app.schemas.stand import StandCreate, StandResponse, StandUpdate
from app.services.empresario_service import get_empresario_or_404
from app.services.evento_service import get_evento_or_404


def get_stand_or_404(db: Session, stand_id: int) -> Stand:
    stand = db.get(Stand, stand_id)
    if stand is None:
        raise NotFoundError(f"Stand {stand_id} no encontrado.")
    return stand


def list_stands(
    db: Session,
    page: int,
    page_size: int,
    id_evento: int | None = None,
    id_empresario: int | None = None,
    estado: EstadoStandEnum | None = None,
) -> PaginatedResponse[StandResponse]:
    stmt = select(Stand)
    if id_evento is not None:
        stmt = stmt.where(Stand.id_evento == id_evento)
    if id_empresario is not None:
        stmt = stmt.where(Stand.id_empresario == id_empresario)
    if estado is not None:
        stmt = stmt.where(Stand.estado == estado)

    total = db.scalar(select(func.count()).select_from(stmt.subquery())) or 0
    items = db.scalars(stmt.order_by(Stand.id_stand).offset((page - 1) * page_size).limit(page_size)).all()

    return PaginatedResponse[StandResponse](
        items=[StandResponse.model_validate(item) for item in items],
        total=total,
        page=page,
        page_size=page_size,
    )


def create_stand(db: Session, data: StandCreate) -> Stand:
    # Validación proactiva de existencia (evita depender solo del error de FK de MySQL).
    get_evento_or_404(db, data.id_evento)
    get_empresario_or_404(db, data.id_empresario)

    stand = Stand(**data.model_dump(), fecha_registro=date.today())
    db.add(stand)
    db.commit()
    db.refresh(stand)
    return stand


def update_stand(db: Session, stand: Stand, data: StandUpdate) -> Stand:
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(stand, field, value)
    db.commit()
    db.refresh(stand)
    return stand


def delete_stand(db: Session, stand: Stand) -> None:
    db.delete(stand)
    db.commit()
