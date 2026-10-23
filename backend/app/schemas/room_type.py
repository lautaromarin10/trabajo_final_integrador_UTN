from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.schemas.generic_schema import GenericSchema
from app.utils.validators import reject_null_value


class RoomTypeBase(BaseModel):
    nombre: str = Field(..., examples=["Doble"])
    descripcion: str | None = Field(None, examples=["Habitación doble con balcón"])
    capacidad_adultos: int = Field(..., ge=1, examples=[2])
    capacidad_ninos: int = Field(..., ge=0, examples=[1])
    cantidad_camas: int = Field(..., ge=1, examples=[1])
    tamanio_m2: float = Field(..., gt=0, examples=[25.0])
    precio: float = Field(..., gt=0, examples=[15000.0])


class RoomTypeCreate(RoomTypeBase):
    pass


class RoomTypeUpdate(BaseModel):
    nombre: str | None = Field(None, examples=["Doble"])
    descripcion: str | None = Field(None, examples=["Habitación doble con balcón"])
    capacidad_adultos: int | None = Field(None, ge=1, examples=[2])
    capacidad_ninos: int | None = Field(None, ge=0, examples=[1])
    cantidad_camas: int | None = Field(None, ge=1, examples=[1])
    tamanio_m2: float | None = Field(None, gt=0, examples=[25.0])
    precio: float | None = Field(None, gt=0, examples=[15000.0])

    @field_validator(
        "nombre",
        "capacidad_adultos",
        "capacidad_ninos",
        "cantidad_camas",
        "tamanio_m2",
        "precio",
        mode="before",
    )
    @classmethod
    def reject_null_values(cls, value):
        return reject_null_value(value)


class RoomTypeRead(GenericSchema):
    model_config = ConfigDict(from_attributes=True)

    nombre: str
    descripcion: str | None = None
    capacidad_adultos: int
    capacidad_ninos: int
    cantidad_camas: int
    tamanio_m2: float
    precio: float


class RoomTypePage(BaseModel):
    items: list[RoomTypeRead]
    total: int
    hasNextPage: bool
    hasPrevPage: bool
