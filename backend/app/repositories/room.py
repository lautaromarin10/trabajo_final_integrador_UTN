from sqlalchemy import ColumnElement, func
from sqlmodel import Session, col, select

from app.models.room import Room, RoomCleaningStatus, RoomStatus
from app.repositories.base import Repository


class RoomRepository(Repository[Room]):
    def __init__(self, session: Session) -> None:
        super().__init__(session, Room)

    def get_by_number(
        self,
        numero: str,
        exclude_room_id: int | None = None,
    ) -> Room | None:
        statement = select(Room).where(Room.numero == numero)
        if exclude_room_id is not None:
            statement = statement.where(Room.id != exclude_room_id)
        return self.session.exec(statement).first()

    def get_active(self, room_id: int) -> Room | None:
        statement = select(Room).where(Room.id == room_id, Room.deleted == False)
        return self.session.exec(statement).first()

    def get_page(
        self,
        skip: int,
        limit: int,
        hotel_id: int | None = None,
        tipo_habitacion_id: int | None = None,
        numero: str | None = None,
        descripcion: str | None = None,
        piso: int | None = None,
        estado_habitacion: RoomStatus | None = None,
        estado_limpieza: RoomCleaningStatus | None = None,
    ) -> tuple[int, list[Room]]:
        filters: list[ColumnElement[bool]] = [col(Room.deleted) == False]
        if hotel_id is not None:
            filters.append(Room.hotel_id == hotel_id)
        if tipo_habitacion_id is not None:
            filters.append(Room.tipo_habitacion_id == tipo_habitacion_id)
        if numero:
            filters.append(Room.numero == numero)
        if descripcion:
            filters.append(Room.descripcion == descripcion)
        if piso is not None:
            filters.append(Room.piso == piso)
        if estado_habitacion is not None:
            filters.append(Room.estado_habitacion == estado_habitacion)
        if estado_limpieza is not None:
            filters.append(Room.estado_limpieza == estado_limpieza)

        total = self.session.exec(
            select(func.count()).select_from(Room).where(*filters)
        ).one()

        items = self.session.exec(
            select(Room)
            .where(*filters)
            .order_by(col(Room.id))
            .offset(skip)
            .limit(limit)
        ).all()

        return total, list(items)