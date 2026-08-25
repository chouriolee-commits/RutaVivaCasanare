from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies import get_current_user
from app.models.evento import EstadoEventoEnum
from app.schemas.common import PaginatedResponse
from app.schemas.evento import EventoCreate, EventoResponse, EventoUpdate
from app.services import evento_service

router = APIRouter()


@router.get("", response_model=PaginatedResponse[EventoResponse])
def list_eventos(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    estado: EstadoEventoEnum | None = Query(default=None),
    db: Session = Depends(get_db),
) -> PaginatedResponse[EventoResponse]:
    """Listado público de eventos (para mostrar la agenda de la feria)."""
    return evento_service.list_eventos(db, page, page_size, estado)


@router.get("/{evento_id}", response_model=EventoResponse)
def get_evento(evento_id: int, db: Session = Depends(get_db)) -> EventoResponse:
    """Detalle público de un evento."""
    evento = evento_service.get_evento_or_404(db, evento_id)
    return EventoResponse.model_validate(evento)


@router.post(
    "",
    response_model=EventoResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(get_current_user)],
)
def create_evento(data: EventoCreate, db: Session = Depends(get_db)) -> EventoResponse:
    evento = evento_service.create_evento(db, data)
    return EventoResponse.model_validate(evento)


@router.put("/{evento_id}", response_model=EventoResponse, dependencies=[Depends(get_current_user)])
def update_evento(evento_id: int, data: EventoUpdate, db: Session = Depends(get_db)) -> EventoResponse:
    evento = evento_service.get_evento_or_404(db, evento_id)
    evento = evento_service.update_evento(db, evento, data)
    return EventoResponse.model_validate(evento)


@router.delete("/{evento_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(get_current_user)])
def delete_evento(evento_id: int, db: Session = Depends(get_db)) -> None:
    evento = evento_service.get_evento_or_404(db, evento_id)
    evento_service.delete_evento(db, evento)
