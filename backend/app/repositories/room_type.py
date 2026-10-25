from sqlalchemy import func
from sqlalchemy.sql.elements import ColumnElement
from sqlmodel import Session, col, select

from app.models.room_type import RoomType
from app.repositories.base import Repository


class RoomTypeRepository(Repository[RoomType]):
    def __init__(self, session: Session) -> None:
        super().__init__(session, RoomType)

    def get_by_name(
        self,
        nombre: str,
        exclude_room_type_id: int | None = None,
    ) -> RoomType | None:
        statement = select(RoomType).where(RoomType.nombre == nombre)
        if exclude_room_type_id is not None:
            statement = statement.where(RoomType.id != exclude_room_type_id)
        return self.session.exec(statement).first()

    def get_active(self, room_type_id: int) -> RoomType | None:
        return self.session.exec(
            select(RoomType).where(
                RoomType.id == room_type_id,
                RoomType.deleted == False,
            )
        ).first()

    def get_page(
        self,
        skip: int,
        limit: int,
        nombre: str | None,
        descripcion: str | None,
        capacidad_adultos: int | None,
        capacidad_ninos: int | None,
        cantidad_camas: int | None,
        tamanio_m2: float | None,
        precio: float | None,
    ) -> tuple[int, list[RoomType]]:
        filters: list[ColumnElement[bool]] = [col(RoomType.deleted) == False]
        if nombre:
            filters.append(func.lower(col(RoomType.nombre)).like(f"%{nombre.lower()}%"))
        if descripcion:
            filters.append(
                func.lower(col(RoomType.descripcion)).like(f"%{descripcion.lower()}%")
            )
        if capacidad_adultos is not None:
            filters.append(col(RoomType.capacidad_adultos) == capacidad_adultos)
        if capacidad_ninos is not None:
            filters.append(col(RoomType.capacidad_ninos) == capacidad_ninos)
        if cantidad_camas is not None:
            filters.append(col(RoomType.cantidad_camas) == cantidad_camas)
        if tamanio_m2 is not None:
            filters.append(col(RoomType.tamanio_m2) == tamanio_m2)
        if precio is not None:
            filters.append(col(RoomType.precio) == precio)

        total = self.session.exec(
            select(func.count()).select_from(RoomType).where(*filters)
        ).one()
        items = self.session.exec(
            select(RoomType)
            .where(*filters)
            .order_by(col(RoomType.id))
            .offset(skip)
            .limit(limit)
        ).all()
        return total, list(items)
