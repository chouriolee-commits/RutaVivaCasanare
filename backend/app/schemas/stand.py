from datetime import date

from pydantic import BaseModel, ConfigDict, Field

from app.models.stand import EstadoStandEnum
from app.schemas.empresario import EmpresarioResponse


class StandBase(BaseModel):
    id_evento: int = Field(..., gt=0)
    id_empresario: int = Field(..., gt=0)
    ubicacion: str | None = Field(default=None, max_length=100)


class StandCreate(StandBase):
    estado: EstadoStandEnum = EstadoStandEnum.pendiente


class StandUpdate(BaseModel):
    ubicacion: str | None = Field(default=None, max_length=100)
    estado: EstadoStandEnum | None = None


class StandResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_stand: int
    id_evento: int
    id_empresario: int
    ubicacion: str | None
    fecha_registro: date | None
    estado: EstadoStandEnum


class StandConEmpresarioResponse(StandResponse):
    empresario: EmpresarioResponse
