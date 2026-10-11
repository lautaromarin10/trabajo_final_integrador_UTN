from datetime import date

from app.models.generic_model import GenericModel


class Person(GenericModel, table=True):
    __tablename__ = "persona"

    nombre: str
    apellido: str
    tipo_documento: str
    numero_documento: str
    fecha_nacimiento: date
    nacionalidad: str
    observaciones: str | None = None
