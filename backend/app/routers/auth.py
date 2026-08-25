from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import InvalidTokenError, decode_token
from app.schemas.auth import LoginRequest, RefreshRequest, RegisterRequest, TokenResponse
from app.schemas.usuario import UsuarioResponse
from app.services import auth_service

router = APIRouter()


@router.post("/register", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
def register(data: RegisterRequest, db: Session = Depends(get_db)) -> UsuarioResponse:
    """Registra una nueva cuenta de usuario. 409 si el email ya existe."""
    usuario = auth_service.register_usuario(db, data)
    return UsuarioResponse.model_validate(usuario)


@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)) -> TokenResponse:
    """Autentica por email/contraseña y retorna access_token + refresh_token."""
    tokens = auth_service.authenticate(db, data.email, data.password)
    if tokens is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Email o contraseña incorrectos.")
    return tokens


@router.post("/refresh", response_model=TokenResponse)
def refresh(data: RefreshRequest, db: Session = Depends(get_db)) -> TokenResponse:
    """Renueva el access_token (y rota el refresh_token) a partir de un refresh_token válido."""
    try:
        payload = decode_token(data.refresh_token, expected_type="refresh")
    except InvalidTokenError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc)) from exc

    tokens = auth_service.refresh_tokens(db, int(payload["sub"]))
    if tokens is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuario no encontrado.")
    return tokens
