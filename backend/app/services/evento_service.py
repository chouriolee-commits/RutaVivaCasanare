from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.exceptions import NotFoundError, ValidationDomainError
from app.models.evento import Evento, EstadoEventoEnum
from app.schemas.common import PaginatedResponse
from app.schemas.evento import EventoCreate, EventoResponse, EventoUpdate


def get_evento_or_404(db: Session, evento_id: int) -> Evento:
    evento = db.get(Evento, evento_id)
    if evento is None:
        raise NotFoundError(f"Evento {evento_id} no encontrado.")
    return evento


def list_eventos(
    db: Session, page: int, page_size: int, estado: EstadoEventoEnum | None = None
) -> PaginatedResponse[EventoResponse]:
    stmt = select(Evento)
    if estado:
        stmt = stmt.where(Evento.estado == estado)

    total = db.scalar(select(func.count()).select_from(stmt.subquery())) or 0
    items = db.scalars(
        stmt.order_by(Evento.fecha_inicio.desc()).offset((page - 1) * page_size).limit(page_size)
    ).all()

    return PaginatedResponse[EventoResponse](
        items=[EventoResponse.model_validate(item) for item in items],
        total=total,
        page=page,
        page_size=page_size,
    )


def create_evento(db: Session, data: EventoCreate) -> Evento:
    evento = Evento(**data.model_dump())
    db.add(evento)
    db.commit()
    db.refresh(evento)
    return evento


def update_evento(db: Session, evento: Evento, data: EventoUpdate) -> Evento:
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(evento, field, value)

    if evento.fecha_fin < evento.fecha_inicio:
        db.rollback()
        raise ValidationDomainError("fecha_fin no puede quedar antes de fecha_inicio tras la actualización.")

    db.commit()
    db.refresh(evento)
    return evento


def delete_evento(db: Session, evento: Evento) -> None:
    db.delete(evento)
    db.commit()
