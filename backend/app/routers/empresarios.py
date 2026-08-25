from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies import get_current_user
from app.schemas.common import PaginatedResponse
from app.schemas.empresario import EmpresarioCreate, EmpresarioResponse, EmpresarioUpdate
from app.services import empresario_service

router = APIRouter(dependencies=[Depends(get_current_user)])


@router.get("", response_model=PaginatedResponse[EmpresarioResponse])
def list_empresarios(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    tipo_producto: str | None = Query(default=None),
    db: Session = Depends(get_db),
) -> PaginatedResponse[EmpresarioResponse]:
    return empresario_service.list_empresarios(db, page, page_size, tipo_producto)


@router.get("/{empresario_id}", response_model=EmpresarioResponse)
def get_empresario(empresario_id: int, db: Session = Depends(get_db)) -> EmpresarioResponse:
    empresario = empresario_service.get_empresario_or_404(db, empresario_id)
    return EmpresarioResponse.model_validate(empresario)


@router.post("", response_model=EmpresarioResponse, status_code=status.HTTP_201_CREATED)
def create_empresario(data: EmpresarioCreate, db: Session = Depends(get_db)) -> EmpresarioResponse:
    empresario = empresario_service.create_empresario(db, data)
    return EmpresarioResponse.model_validate(empresario)


@router.put("/{empresario_id}", response_model=EmpresarioResponse)
def update_empresario(empresario_id: int, data: EmpresarioUpdate, db: Session = Depends(get_db)) -> EmpresarioResponse:
    empresario = empresario_service.get_empresario_or_404(db, empresario_id)
    empresario = empresario_service.update_empresario(db, empresario, data)
    return EmpresarioResponse.model_validate(empresario)


@router.delete("/{empresario_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_empresario(empresario_id: int, db: Session = Depends(get_db)) -> None:
    empresario = empresario_service.get_empresario_or_404(db, empresario_id)
    empresario_service.delete_empresario(db, empresario)
