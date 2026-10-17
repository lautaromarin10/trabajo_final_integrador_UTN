from fastapi import HTTPException

from app.core.unit_of_work import UnitOfWork
from app.models.person import Person
from app.schemas.person import PersonCreate, PersonPage, PersonRead, PersonUpdate


def _ensure_document_available(
    unit_of_work: UnitOfWork,
    tipo_documento: str,
    numero_documento: str,
    exclude_person_id: int | None = None,
) -> None:
    existing = unit_of_work.persons.get_by_document(
        tipo_documento, numero_documento, exclude_person_id
    )
    if existing:
        detail = (
            "La persona ya está eliminada; debe reactivarse en lugar de crear otra"
            if existing.deleted
            else "Ya existe una persona registrada con ese número y tipo de documento"
        )
        raise HTTPException(status_code=409, detail=detail)


def create_person(data: PersonCreate, unit_of_work: UnitOfWork) -> Person:
    _ensure_document_available(unit_of_work, data.tipo_documento, data.numero_documento)

    person = Person(**data.model_dump())
    return unit_of_work.persons.add(person)


def get_persons(
    unit_of_work: UnitOfWork,
    skip: int = 0,
    limit: int = 20,
    nombre: str | None = None,
    apellido: str | None = None,
    tipo_documento: str | None = None,
    numero_documento: str | None = None,
) -> PersonPage:
    total, items = unit_of_work.persons.get_page(
        skip, limit, nombre, apellido, tipo_documento, numero_documento
    )
    return PersonPage(
        total=total,
        items=[PersonRead.model_validate(person) for person in items],
        hasNextPage=skip + len(items) < total,
        hasPrevPage=skip > 0 and total > 0,
    )


def get_person(
    unit_of_work: UnitOfWork,
    person_id: int,
) -> Person:
    person = unit_of_work.persons.get_active(person_id)
    if not person:
        raise HTTPException(status_code=404, detail="Persona no encontrada")

    return person


def update_person(
    unit_of_work: UnitOfWork, person_id: int, data: PersonUpdate
) -> Person:

    person = get_person(unit_of_work, person_id)
    update_data = data.model_dump(exclude_unset=True)

    tipo_documento = update_data.get("tipo_documento", person.tipo_documento)
    numero_documento = update_data.get("numero_documento", person.numero_documento)
    if (
        tipo_documento != person.tipo_documento
        or numero_documento != person.numero_documento
    ):
        _ensure_document_available(
            unit_of_work,
            tipo_documento,
            numero_documento,
            exclude_person_id=person_id,
        )

    unit_of_work.persons.update_fields(person, update_data)
    return unit_of_work.persons.add(person)


def delete_person(unit_of_work: UnitOfWork, person_id: int) -> Person:

    person = get_person(unit_of_work, person_id)
    return unit_of_work.persons.soft_delete(person)


def reactivate_person(unit_of_work: UnitOfWork, person_id: int) -> Person:
    person = unit_of_work.persons.get(person_id)
    if person is None:
        raise HTTPException(status_code=404, detail="Persona no encontrada")
    if not person.deleted:
        raise HTTPException(status_code=409, detail="La persona ya está activa")

    _ensure_document_available(
        unit_of_work,
        person.tipo_documento,
        person.numero_documento,
        exclude_person_id=person_id,
    )
    return unit_of_work.persons.reactivate(person)
