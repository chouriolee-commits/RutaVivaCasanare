from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies import get_current_user
from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioResponse, UsuarioUpdate
from app.services import usuario_service

router = APIRouter()


@router.get("/me", response_model=UsuarioResponse)
def get_me(current_user: Usuario = Depends(get_current_user)) -> UsuarioResponse:
    return UsuarioResponse.model_validate(current_user)


@router.put("/me", response_model=UsuarioResponse)
def update_me(
    data: UsuarioUpdate,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> UsuarioResponse:
    usuario = usuario_service.update_usuario(db, current_user, data)
    return UsuarioResponse.model_validate(usuario)
