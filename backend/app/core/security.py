from datetime import datetime, timedelta, timezone
from typing import Any, Literal

import bcrypt
from jose import JWTError, jwt

from app.core.config import settings

_BCRYPT_ROUNDS = 12
# bcrypt trunca el input a 72 bytes; lo validamos explícito para no fallar en silencio.
_MAX_PASSWORD_BYTES = 72


def hash_password(password: str) -> str:
    password_bytes = password.encode("utf-8")
    if len(password_bytes) > _MAX_PASSWORD_BYTES:
        raise ValueError(f"La contraseña no puede superar {_MAX_PASSWORD_BYTES} bytes.")
    salt = bcrypt.gensalt(rounds=_BCRYPT_ROUNDS)
    return bcrypt.hashpw(password_bytes, salt).decode("utf-8")


def verify_password(plain_password: str, password_hash: str) -> bool:
    try:
        return bcrypt.checkpw(plain_password.encode("utf-8"), password_hash.encode("utf-8"))
    except ValueError:
        # hash corrupto o con formato inválido — nunca autenticar en ese caso
        return False


def _create_token(subject: str, expires_delta: timedelta, token_type: Literal["access", "refresh"]) -> str:
    now = datetime.now(timezone.utc)
    payload: dict[str, Any] = {
        "sub": subject,
        "type": token_type,
        "iat": now,
        "exp": now + expires_delta,
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def create_access_token(user_id: int) -> str:
    return _create_token(str(user_id), timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES), "access")


def create_refresh_token(user_id: int) -> str:
    return _create_token(str(user_id), timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS), "refresh")


class InvalidTokenError(Exception):
    pass


def decode_token(token: str, expected_type: Literal["access", "refresh"] = "access") -> dict[str, Any]:
    """Decodifica y valida un JWT. Lanza InvalidTokenError si es inválido,
    expiró o no es del tipo esperado (evita usar un refresh_token como si
    fuera un access_token y viceversa)."""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    except JWTError as exc:
        raise InvalidTokenError("Token inválido o expirado.") from exc

    if payload.get("type") != expected_type:
        raise InvalidTokenError(f"Se esperaba un token de tipo '{expected_type}'.")

    return payload
