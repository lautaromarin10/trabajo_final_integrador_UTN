from fastapi import HTTPException

from app.core.unit_of_work import UnitOfWork
from app.models.room import Room, RoomCleaningStatus, RoomStatus
from app.schemas.room import RoomCreate, RoomPage, RoomRead, RoomUpdate


def _ensure_number_available(
    unit_of_work: UnitOfWork,
    numero: str,
    exclude_room_id: int | None = None,
) -> None:
    existing = unit_of_work.rooms.get_by_number(numero, exclude_room_id)
    if existing:
        detail = (
            "La habitación ya está eliminada; debe reactivarse en lugar de crear otra"
            if existing.deleted
            else "Ya existe una habitación con ese número"
        )
        raise HTTPException(status_code=409, detail=detail)


def _ensure_room_type_exists(unit_of_work: UnitOfWork, tipo_habitacion_id: int) -> None:
    if not unit_of_work.room_types.get_active(tipo_habitacion_id):
        raise HTTPException(status_code=404, detail="Tipo de habitación no encontrado")


def _ensure_hotel_exists(unit_of_work: UnitOfWork, hotel_id: int) -> None:
    if not unit_of_work.hotels.get_active(hotel_id):
        raise HTTPException(status_code=404, detail="Hotel no encontrado")


def create_room(data: RoomCreate, unit_of_work: UnitOfWork) -> Room:
    _ensure_number_available(unit_of_work, data.numero)
    _ensure_hotel_exists(unit_of_work, data.hotel_id)
    _ensure_room_type_exists(unit_of_work, data.tipo_habitacion_id)

    room = Room(**data.model_dump())
    return unit_of_work.rooms.add(room)


def get_rooms(
    unit_of_work: UnitOfWork,
    skip: int = 0,
    limit: int = 20,
    hotel_id: int | None = None,
    tipo_habitacion_id: int | None = None,
    numero: str | None = None,
    descripcion: str | None = None,
    piso: int | None = None,
    estado_habitacion: RoomStatus | None = None,
    estado_limpieza: RoomCleaningStatus | None = None,
) -> RoomPage:
    total, items = unit_of_work.rooms.get_page(
        skip,
        limit,
        hotel_id,
        tipo_habitacion_id,
        numero,
        descripcion,
        piso,
        estado_habitacion,
        estado_limpieza,
    )
    return RoomPage(
        total=total,
        items=[RoomRead.model_validate(room) for room in items],
        hasNextPage=skip + len(items) < total,
        hasPrevPage=skip > 0 and total > 0,
    )


def get_room(unit_of_work: UnitOfWork, room_id: int) -> Room:
    room = unit_of_work.rooms.get_active(room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Habitación no encontrada")

    return room


def update_room(unit_of_work: UnitOfWork, room_id: int, data: RoomUpdate) -> Room:
    room = get_room(unit_of_work, room_id)
    update_data = data.model_dump(exclude_unset=True)

    numero = update_data.get("numero", room.numero)
    if numero != room.numero:
        _ensure_number_available(unit_of_work, numero, exclude_room_id=room_id)

    tipo_habitacion_id = update_data.get("tipo_habitacion_id", room.tipo_habitacion_id)
    if tipo_habitacion_id != room.tipo_habitacion_id:
        _ensure_room_type_exists(unit_of_work, tipo_habitacion_id)

    unit_of_work.rooms.update_fields(room, update_data)
    return unit_of_work.rooms.add(room)


def delete_room(unit_of_work: UnitOfWork, room_id: int) -> Room:
    room = get_room(unit_of_work, room_id)
    return unit_of_work.rooms.soft_delete(room)


def reactivate_room(unit_of_work: UnitOfWork, room_id: int) -> Room:
    room = unit_of_work.rooms.get(room_id)
    if room is None:
        raise HTTPException(status_code=404, detail="Habitación no encontrada")
    if not room.deleted:
        raise HTTPException(status_code=409, detail="La habitación ya está activa")

    _ensure_number_available(unit_of_work, room.numero, exclude_room_id=room_id)
    _ensure_hotel_exists(unit_of_work, room.hotel_id)
    _ensure_room_type_exists(unit_of_work, room.tipo_habitacion_id)
    return unit_of_work.rooms.reactivate(room)
