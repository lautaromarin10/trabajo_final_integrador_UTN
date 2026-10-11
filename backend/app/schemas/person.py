from datetime import date

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.schemas.generic_schema import GenericSchema
from app.utils.validators import reject_null_value


class PersonBase(BaseModel):
    nombre: str = Field(..., examples=["Ana"])
    apellido: str = Field(..., examples=["Pérez"])
    tipo_documento: str = Field(..., examples=["DNI"])
    numero_documento: str = Field(..., examples=["12345678"])
    fecha_nacimiento: date = Field(..., examples=["1990-01-15"])
    nacionalidad: str = Field(..., examples=["Argentina"])
    observaciones: str | None = Field(None, examples=[""])


class PersonCreate(PersonBase):
    pass


class PersonUpdate(BaseModel):
    nombre: str | None = Field(None, examples=["Ana"])
    apellido: str | None = Field(None, examples=["Pérez"])
    tipo_documento: str | None = Field(None, examples=["DNI"])
    numero_documento: str | None = Field(None, examples=["12345678"])
    fecha_nacimiento: date | None = Field(None, examples=["1990-01-15"])
    nacionalidad: str | None = Field(None, examples=["Argentina"])
    observaciones: str | None = Field(None, examples=[""])

    @field_validator(
        "nombre",
        "apellido",
        "tipo_documento",
        "numero_documento",
        "fecha_nacimiento",
        "nacionalidad",
        mode="before",
    )
    @classmethod
    def reject_null_values(cls, value):
        return reject_null_value(value)


class PersonRead(GenericSchema):
    model_config = ConfigDict(from_attributes=True)

    nombre: str
    apellido: str
    tipo_documento: str
    numero_documento: str
    fecha_nacimiento: date
    nacionalidad: str
    observaciones: str | None = None


class PersonPage(BaseModel):
    items: list[PersonRead]
    total: int
    hasNextPage: bool
    hasPrevPage: bool
