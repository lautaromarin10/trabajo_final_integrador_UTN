from typing import Annotated

from fastapi import APIRouter, Path, Query, Response, status

from app.core.auth import AdminUserDep, CurrentUserDep
from app.core.database import UnitOfWorkDep
from app.models.room_type import RoomType
from app.schemas.room_type import (
    RoomTypeCreate,
    RoomTypePage,
    RoomTypeRead,
    RoomTypeUpdate,
)
from app.services.room_type import (
    create_room_type as create_room_type_service,
)
from app.services.room_type import (
    delete_room_type as delete_room_type_service,
)
from app.services.room_type import (
    get_room_type as get_room_type_service,
)
from app.services.room_type import (
    get_room_types as get_room_types_service,
)
from app.services.room_type import (
    reactivate_room_type as reactivate_room_type_service,
)
from app.services.room_type import (
    update_room_type as update_room_type_service,
)

router = APIRouter(
    prefix="/room-type",
    tags=["Tipo de habitación"],
)


@router.post("/", response_model=RoomTypeRead, status_code=status.HTTP_201_CREATED)
def create_room_type(
    room_type: RoomTypeCreate,
    unit_of_work: UnitOfWorkDep,
    _: AdminUserDep,
) -> RoomType:
    return create_room_type_service(room_type, unit_of_work)


@router.get("/", response_model=RoomTypePage)
def get_room_types(
    unit_of_work: UnitOfWorkDep,
    _: CurrentUserDep,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    nombre: str | None = Query(None, min_length=1),
    descripcion: str | None = Query(None, min_length=1),
    capacidad_adultos: int | None = Query(None, ge=1),
    capacidad_ninos: int | None = Query(None, ge=0),
    cantidad_camas: int | None = Query(None, ge=1),
    tamanio_m2: float | None = Query(None, gt=0),
    precio: float | None = Query(None, gt=0),
) -> RoomTypePage:
    return get_room_types_service(
        unit_of_work,
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


@router.get("/{room_type_id}", response_model=RoomTypeRead)
def get_room_type(
    room_type_id: Annotated[int, Path(gt=0)],
    unit_of_work: UnitOfWorkDep,
    _: CurrentUserDep,
) -> RoomType:
    return get_room_type_service(unit_of_work, room_type_id)


@router.patch("/{room_type_id}", response_model=RoomTypeRead)
def update_room_type(
    room_type: RoomTypeUpdate,
    room_type_id: Annotated[int, Path(gt=0)],
    unit_of_work: UnitOfWorkDep,
    _: AdminUserDep,
) -> RoomType:
    return update_room_type_service(unit_of_work, room_type_id, room_type)


@router.delete("/{room_type_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_room_type(
    room_type_id: Annotated[int, Path(gt=0)],
    unit_of_work: UnitOfWorkDep,
    _: AdminUserDep,
) -> Response:
    delete_room_type_service(unit_of_work, room_type_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/{room_type_id}/reactivate", response_model=RoomTypeRead)
def reactivate_room_type(
    room_type_id: Annotated[int, Path(gt=0)],
    unit_of_work: UnitOfWorkDep,
    _: AdminUserDep,
) -> RoomType:
    return reactivate_room_type_service(unit_of_work, room_type_id)
