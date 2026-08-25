from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies import get_current_user
from app.models.stand import EstadoStandEnum
from app.schemas.common import PaginatedResponse
from app.schemas.stand import StandCreate, StandResponse, StandUpdate
from app.services import stand_service

router = APIRouter(dependencies=[Depends(get_current_user)])


@router.get("", response_model=PaginatedResponse[StandResponse])
def list_stands(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    id_evento: int | None = Query(default=None),
    id_empresario: int | None = Query(default=None),
    estado: EstadoStandEnum | None = Query(default=None),
    db: Session = Depends(get_db),
) -> PaginatedResponse[StandResponse]:
    return stand_service.list_stands(db, page, page_size, id_evento, id_empresario, estado)


@router.get("/{stand_id}", response_model=StandResponse)
def get_stand(stand_id: int, db: Session = Depends(get_db)) -> StandResponse:
    stand = stand_service.get_stand_or_404(db, stand_id)
    return StandResponse.model_validate(stand)


@router.post("", response_model=StandResponse, status_code=status.HTTP_201_CREATED)
def create_stand(data: StandCreate, db: Session = Depends(get_db)) -> StandResponse:
    stand = stand_service.create_stand(db, data)
    return StandResponse.model_validate(stand)


@router.put("/{stand_id}", response_model=StandResponse)
def update_stand(stand_id: int, data: StandUpdate, db: Session = Depends(get_db)) -> StandResponse:
    stand = stand_service.get_stand_or_404(db, stand_id)
    stand = stand_service.update_stand(db, stand, data)
    return StandResponse.model_validate(stand)


@router.delete("/{stand_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_stand(stand_id: int, db: Session = Depends(get_db)) -> None:
    stand = stand_service.get_stand_or_404(db, stand_id)
    stand_service.delete_stand(db, stand)
