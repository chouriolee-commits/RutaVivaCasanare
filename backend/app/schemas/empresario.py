from pydantic import BaseModel, ConfigDict, EmailStr, Field


class EmpresarioBase(BaseModel):
    nombre_negocio: str = Field(..., min_length=2, max_length=150)
    propietario: str = Field(..., min_length=2, max_length=150)
    telefono: str | None = Field(default=None, max_length=20)
    email: EmailStr | None = None
    tipo_producto: str | None = Field(default=None, max_length=100)


class EmpresarioCreate(EmpresarioBase):
    pass


class EmpresarioUpdate(BaseModel):
    nombre_negocio: str | None = Field(default=None, min_length=2, max_length=150)
    propietario: str | None = Field(default=None, min_length=2, max_length=150)
    telefono: str | None = Field(default=None, max_length=20)
    email: EmailStr | None = None
    tipo_producto: str | None = Field(default=None, max_length=100)


class EmpresarioResponse(EmpresarioBase):
    model_config = ConfigDict(from_attributes=True)

    id_empresario: int
