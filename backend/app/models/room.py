from enum import Enum

from sqlalchemy import Column
from sqlalchemy import Enum as SAEnum
from sqlmodel import Field

from app.models.generic_model import GenericModel


class RoomStatus(str, Enum):
    DISPONIBLE = "disponible"
    OCUPADA = "ocupada"
    FUERA_DE_SERVICIO = "fuera_de_servicio"
    MANTENIMIENTO = "mantenimiento"


class RoomCleaningStatus(str, Enum):
    SUCIA = "sucia"
    EN_PROGRESO = "en_progreso"
    LIMPIA = "limpia"


class Room(GenericModel, table=True):
    __tablename__ = "habitacion"

    hotel_id: int = Field(foreign_key="hotel.id", index=True)
    tipo_habitacion_id: int = Field(foreign_key="tipo_habitacion.id", index=True)
    numero: str = Field(index=True)
    descripcion: str | None = None
    piso: int
    estado_habitacion: RoomStatus = Field(
        default=RoomStatus.DISPONIBLE,
        sa_column=Column(
            SAEnum(RoomStatus, values_callable=lambda enum: [item.value for item in enum]),
            nullable=False,
        ),
    )
    estado_limpieza: RoomCleaningStatus = Field(
        default=RoomCleaningStatus.LIMPIA,
        sa_column=Column(
            SAEnum(
                RoomCleaningStatus,
                values_callable=lambda enum: [item.value for item in enum],
            ),
            nullable=False,
        ),
    )