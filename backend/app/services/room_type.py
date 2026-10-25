from fastapi import HTTPException

from app.core.unit_of_work import UnitOfWork
from app.models.room_type import RoomType
from app.schemas.room_type import (
    RoomTypeCreate,
    RoomTypePage,
    RoomTypeRead,
    RoomTypeUpdate,
)


def _ensure_name_available(
    unit_of_work: UnitOfWork,
    nombre: str,
    exclude_room_type_id: int | None = None,
) -> None:
    existing = unit_of_work.room_types.get_by_name(nombre, exclude_room_type_id)
    if existing:
        detail = (
            "El tipo de habitación ya está eliminado; debe reactivarse en lugar de crear otro"
            if existing.deleted
            else "Ya existe un tipo de habitación con ese nombre"
        )
        raise HTTPException(status_code=409, detail=detail)


def create_room_type(data: RoomTypeCreate, unit_of_work: UnitOfWork) -> RoomType:
    _ensure_name_available(unit_of_work, data.nombre)

    room_type = RoomType(**data.model_dump())
    return unit_of_work.room_types.add(room_type)


def get_room_types(
    unit_of_work: UnitOfWork,
    skip: int = 0,
    limit: int = 20,
    nombre: str | None = None,
    descripcion: str | None = None,
    capacidad_adultos: int | None = None,
    capacidad_ninos: int | None = None,
    cantidad_camas: int | None = None,
    tamanio_m2: float | None = None,
    precio: float | None = None,
) -> RoomTypePage:
    total, items = unit_of_work.room_types.get_page(
        skip,
        limit,
        nombre,
        descripcion,
        capacidad_adultos,
        capacidad_ninos,
        cantidad_camas,
        tamanio_m2,
        precio,
    )
    return RoomTypePage(
        total=total,
        items=[RoomTypeRead.model_validate(room_type) for room_type in items],
        hasNextPage=skip + len(items) < total,
        hasPrevPage=skip > 0 and total > 0,
    )


def get_room_type(unit_of_work: UnitOfWork, room_type_id: int) -> RoomType:
    room_type = unit_of_work.room_types.get_active(room_type_id)
    if not room_type:
        raise HTTPException(status_code=404, detail="Tipo de habitación no encontrado")

    return room_type


def update_room_type(
    unit_of_work: UnitOfWork,
    room_type_id: int,
    data: RoomTypeUpdate,
) -> RoomType:
    room_type = get_room_type(unit_of_work, room_type_id)
    update_data = data.model_dump(exclude_unset=True)

    nombre = update_data.get("nombre", room_type.nombre)
    if nombre != room_type.nombre:
        _ensure_name_available(unit_of_work, nombre, exclude_room_type_id=room_type_id)

    unit_of_work.room_types.update_fields(room_type, update_data)
    return unit_of_work.room_types.add(room_type)


def delete_room_type(unit_of_work: UnitOfWork, room_type_id: int) -> RoomType:
    room_type = get_room_type(unit_of_work, room_type_id)
    return unit_of_work.room_types.soft_delete(room_type)


def reactivate_room_type(unit_of_work: UnitOfWork, room_type_id: int) -> RoomType:
    room_type = unit_of_work.room_types.get(room_type_id)
    if room_type is None:
        raise HTTPException(status_code=404, detail="Tipo de habitación no encontrado")
    if not room_type.deleted:
        raise HTTPException(status_code=409, detail="El tipo de habitación ya está activo")

    _ensure_name_available(
        unit_of_work,
        room_type.nombre,
        exclude_room_type_id=room_type_id,
    )
    return unit_of_work.room_types.reactivate(room_type)
