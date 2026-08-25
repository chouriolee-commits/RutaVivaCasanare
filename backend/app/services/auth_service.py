from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import (
    create_access_token,
    create_refresh_token,
    hash_password,
    verify_password,
)
from app.exceptions import ConflictError, ValidationDomainError
from app.models.usuario import Usuario
from app.schemas.auth import RegisterRequest, TokenResponse


def get_usuario_by_email(db: Session, email: str) -> Usuario | None:
    return db.scalar(select(Usuario).where(Usuario.email == email))


def register_usuario(db: Session, data: RegisterRequest) -> Usuario:
    if get_usuario_by_email(db, data.email) is not None:
        raise ConflictError("Ya existe una cuenta registrada con ese email.")

    try:
        contrasena_hash = hash_password(data.password)
    except ValueError as exc:
        raise ValidationDomainError(str(exc)) from exc

    usuario = Usuario(
        nombre=data.nombre,
        email=data.email,
        contrasena_hash=contrasena_hash,
        telefono=data.telefono,
    )
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario


def _build_tokens(usuario: Usuario) -> TokenResponse:
    return TokenResponse(
        access_token=create_access_token(usuario.id_usuario),
        refresh_token=create_refresh_token(usuario.id_usuario),
    )


def authenticate(db: Session, email: str, password: str) -> TokenResponse | None:
    usuario = get_usuario_by_email(db, email)
    if usuario is None or not verify_password(password, usuario.contrasena_hash):
        return None
    return _build_tokens(usuario)


def refresh_tokens(db: Session, usuario_id: int) -> TokenResponse | None:
    usuario = db.get(Usuario, usuario_id)
    if usuario is None:
        return None
    return _build_tokens(usuario)
