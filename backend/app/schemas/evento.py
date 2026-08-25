from datetime import date

from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.models.evento import EstadoEventoEnum


class EventoBase(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=150)
    descripcion: str | None = None
    fecha_inicio: date
    fecha_fin: date
    ubicacion: str | None = Field(default=None, max_length=200)

    @model_validator(mode="after")
    def validar_fechas(self) -> "EventoBase":
        if self.fecha_fin < self.fecha_inicio:
            raise ValueError("fecha_fin no puede ser anterior a fecha_inicio.")
        return self


class EventoCreate(EventoBase):
    estado: EstadoEventoEnum = EstadoEventoEnum.planeado


class EventoUpdate(BaseModel):
    nombre: str | None = Field(default=None, min_length=2, max_length=150)
    descripcion: str | None = None
    fecha_inicio: date | None = None
    fecha_fin: date | None = None
    ubicacion: str | None = Field(default=None, max_length=200)
    estado: EstadoEventoEnum | None = None

    @model_validator(mode="after")
    def validar_fechas(self) -> "EventoUpdate":
        if self.fecha_inicio and self.fecha_fin and self.fecha_fin < self.fecha_inicio:
            raise ValueError("fecha_fin no puede ser anterior a fecha_inicio.")
        return self


class EventoResponse(EventoBase):
    model_config = ConfigDict(from_attributes=True)

    id_evento: int
    estado: EstadoEventoEnum
