from models.generic_model import GenericModel
from sqlmodel import Field


class Roomtype(GenericModel, table=True):
    __tablename__ = "room_type"

    nombre: str
    descripcion: str | None = None
    capacidad_adultos: int = Field(nullable=False, default=1)
    capacidad_ninos: int = Field(nullable=False, default=0)
    cantidad_camas: int = Field(nullable=False, default=0)
    tamanio_m2: float
    precio: float = Field(nullable=False, default=0.0)