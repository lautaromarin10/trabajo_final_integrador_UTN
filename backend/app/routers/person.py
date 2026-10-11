from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query, Response, status

from app.core.auth import require_admin
from app.core.database import SessionDep
from app.models.person import Person
from app.schemas.person import PersonCreate, PersonPage, PersonRead, PersonUpdate
from app.services.person import (
    create_person as create_person_service,
)
from app.services.person import (
    delete_person as delete_person_service,
)
from app.services.person import (
    get_person as get_person_service,
)
from app.services.person import (
    get_persons as get_persons_service,
)
from app.services.person import (
    reactivate_person as reactivate_person_service,
)
from app.services.person import (
    update_person as update_person_service,
)

router = APIRouter(
    prefix="/person",
    tags=["Persona"],
    dependencies=[Depends(require_admin)],
)


@router.post("/", response_model=PersonRead, status_code=status.HTTP_201_CREATED)
def create_person(person: PersonCreate, session: SessionDep) -> Person:
    return create_person_service(person, session)


@router.get("/", response_model=PersonPage)
def get_persons(
    session: SessionDep,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    nombre: str | None = Query(None, min_length=1, max_length=100),
    apellido: str | None = Query(None, min_length=1, max_length=100),
    tipo_documento: str | None = Query(None, min_length=1, max_length=30),
    numero_documento: str | None = Query(None, min_length=1, max_length=50),
) -> PersonPage:
    return get_persons_service(
        session,
        skip,
        limit,
        nombre,
        apellido,
        tipo_documento,
        numero_documento,
    )


@router.get("/{person_id}", response_model=PersonRead)
def get_person(
    person_id: Annotated[int, Path(gt=0)],
    session: SessionDep,
) -> Person:
    return get_person_service(session, person_id)


@router.patch("/{person_id}", response_model=PersonRead)
def update_person(
    person: PersonUpdate,
    person_id: Annotated[int, Path(gt=0)],
    session: SessionDep,
) -> Person:
    return update_person_service(session, person_id, person)


@router.delete("/{person_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_person(
    person_id: Annotated[int, Path(gt=0)],
    session: SessionDep,
) -> Response:
    delete_person_service(session, person_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/{person_id}/reactivate", response_model=PersonRead)
def reactivate_person(
    person_id: Annotated[int, Path(gt=0)],
    session: SessionDep,
) -> Person:
    return reactivate_person_service(session, person_id)
