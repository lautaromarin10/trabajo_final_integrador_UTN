

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.models.room import RoomCleaningStatus, RoomStatus
from app.schemas.generic_schema import GenericSchema
from app.utils.validators import reject_null_value


class RoomBase(BaseModel):
    hotel_id: int = Field(..., gt=0, examples=[1])
    tipo_habitacion_id: int = Field(..., gt=0, examples=[1])
    numero: str = Field(..., pattern=r"^[1-9]\d*$", examples=["101"])
    descripcion: str | None = Field(None, examples=["Suite con vista a la playa"])
    piso: int = Field(..., ge=0, examples=[1])
    estado_habitacion: RoomStatus = Field(..., examples=[RoomStatus.DISPONIBLE])
    estado_limpieza: RoomCleaningStatus = Field(..., examples=[RoomCleaningStatus.LIMPIA])

class RoomCreate(RoomBase):
    pass

class RoomUpdate(BaseModel):
    tipo_habitacion_id: int | None = Field(None, gt=0, examples=[1])
    numero: str | None = Field(None, pattern=r"^[1-9]\d*$", examples=["101"])
    descripcion: str | None = Field(None, examples=["Suite con vista a la playa"])
    piso: int | None = Field(None, ge=0, examples=[1])
    estado_habitacion: RoomStatus | None = Field(None, examples=[RoomStatus.DISPONIBLE])
    estado_limpieza: RoomCleaningStatus | None = Field(None, examples=[RoomCleaningStatus.LIMPIA])

    @field_validator(
        "tipo_habitacion_id",
        "numero",
        "piso",
        "estado_habitacion",
        "estado_limpieza",
        mode="before",
    )
    @classmethod
    def reject_null_values(cls, value):
        return reject_null_value(value)


class RoomRead(GenericSchema):
    model_config = ConfigDict(from_attributes=True)

    hotel_id: int
    tipo_habitacion_id: int
    numero: str
    descripcion: str | None = None
    piso: int
    estado_habitacion: RoomStatus
    estado_limpieza: RoomCleaningStatus

class RoomPage(BaseModel):
    items: list[RoomRead]
    total: int
    hasNextPage: bool
    hasPrevPage: bool