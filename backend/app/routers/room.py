from typing import Annotated

from fastapi import APIRouter, Path, Query, Response, status

from app.core.auth import AdminUserDep, CurrentUserDep
from app.core.database import UnitOfWorkDep
from app.models.room import Room, RoomCleaningStatus, RoomStatus
from app.schemas.room import RoomCreate, RoomPage, RoomRead, RoomUpdate
from app.services.room import (
    create_room as create_room_service,
)
from app.services.room import (
    delete_room as delete_room_service,
)
from app.services.room import (
    get_room as get_room_service,
)
from app.services.room import (
    get_rooms as get_rooms_service,
)
from app.services.room import (
    reactivate_room as reactivate_room_service,
)
from app.services.room import (
    update_room as update_room_service,
)

router = APIRouter(
    prefix="/room",
    tags=["Habitación"],
)


@router.post("/", response_model=RoomRead, status_code=status.HTTP_201_CREATED)
def create_room(
    room: RoomCreate,
    unit_of_work: UnitOfWorkDep,
    _: AdminUserDep,
) -> Room:
    return create_room_service(room, unit_of_work)


@router.get("/", response_model=RoomPage)
def get_rooms(
    unit_of_work: UnitOfWorkDep,
    _: CurrentUserDep,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    hotel_id: int | None = Query(None, gt=0),
    tipo_habitacion_id: int | None = Query(None, gt=0),
    numero: str | None = Query(None, pattern=r"^[1-9]\d*$"),
    descripcion: str | None = Query(None, min_length=1),
    piso: int | None = Query(None, ge=0),
    estado_habitacion: RoomStatus | None = None,
    estado_limpieza: RoomCleaningStatus | None = None,
) -> RoomPage:
    return get_rooms_service(
        unit_of_work,
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


@router.get("/{room_id}", response_model=RoomRead)
def get_room(
    room_id: Annotated[int, Path(gt=0)],
    unit_of_work: UnitOfWorkDep,
    _: CurrentUserDep,
) -> Room:
    return get_room_service(unit_of_work, room_id)


@router.patch("/{room_id}", response_model=RoomRead)
def update_room(
    room: RoomUpdate,
    room_id: Annotated[int, Path(gt=0)],
    unit_of_work: UnitOfWorkDep,
    _: AdminUserDep,
) -> Room:
    return update_room_service(unit_of_work, room_id, room)


@router.delete("/{room_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_room(
    room_id: Annotated[int, Path(gt=0)],
    unit_of_work: UnitOfWorkDep,
    _: AdminUserDep,
) -> Response:
    delete_room_service(unit_of_work, room_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/{room_id}/reactivate", response_model=RoomRead)
def reactivate_room(
    room_id: Annotated[int, Path(gt=0)],
    unit_of_work: UnitOfWorkDep,
    _: AdminUserDep,
) -> Room:
    return reactivate_room_service(unit_of_work, room_id)
