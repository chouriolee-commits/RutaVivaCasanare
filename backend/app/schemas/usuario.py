from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UsuarioResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_usuario: int
    nombre: str
    email: EmailStr
    telefono: str | None
    fecha_registro: datetime


class UsuarioUpdate(BaseModel):
    nombre: str | None = Field(default=None, min_length=2, max_length=150)
    telefono: str | None = Field(default=None, max_length=20)


class CambiarPasswordRequest(BaseModel):
    password_actual: str
    password_nueva: str = Field(..., min_length=8, max_length=128)
