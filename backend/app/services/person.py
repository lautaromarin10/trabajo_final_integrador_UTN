from datetime import UTC, datetime

from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.sql.elements import ColumnElement
from sqlmodel import Session, col, select

from app.models.person import Person
from app.schemas.person import PersonCreate, PersonPage, PersonRead, PersonUpdate


def _ensure_document_available(
    session: Session,
    tipo_documento: str,
    numero_documento: str,
    exclude_person_id: int | None = None,
) -> None:
    statement = select(Person).where(
        Person.tipo_documento == tipo_documento,
        Person.numero_documento == numero_documento,
    )
    if exclude_person_id is not None:
        statement = statement.where(Person.id != exclude_person_id)

    existing = session.exec(statement).first()
    if existing:
        detail = (
            "La persona ya está eliminada; debe reactivarse en lugar de crear otra"
            if existing.deleted
            else "Ya existe una persona registrada con ese número y tipo de documento"
        )
        raise HTTPException(status_code=409, detail=detail)


def create_person(data: PersonCreate, session: Session) -> Person:
    _ensure_document_available(session, data.tipo_documento, data.numero_documento)

    person = Person(**data.model_dump())

    session.add(person)
    session.commit()
    session.refresh(person)
    return person


def get_persons(
    session: Session,
    skip: int = 0,
    limit: int = 20,
    nombre: str | None = None,
    apellido: str | None = None,
    tipo_documento: str | None = None,
    numero_documento: str | None = None,
) -> PersonPage:
    filters: list[ColumnElement[bool]] = [col(Person.deleted) == False]
    if nombre:
        filters.append(func.lower(col(Person.nombre)).like(f"%{nombre.lower()}%"))
    if apellido:
        filters.append(func.lower(col(Person.apellido)).like(f"%{apellido.lower()}%"))
    if tipo_documento:
        filters.append(col(Person.tipo_documento) == tipo_documento)
    if numero_documento:
        filters.append(col(Person.numero_documento) == numero_documento)

    total = session.exec(select(func.count()).select_from(Person).where(*filters)).one()
    items = session.exec(
        select(Person)
        .where(*filters)
        .order_by(col(Person.id))
        .offset(skip)
        .limit(limit)
    ).all()
    return PersonPage(
        total=total,
        items=[PersonRead.model_validate(person) for person in items],
        hasNextPage=skip + len(items) < total,
        hasPrevPage=skip > 0 and total > 0,
    )


def get_person(
    session: Session,
    person_id: int,
) -> Person:
    person = session.exec(
        select(Person).where(Person.id == person_id).where(Person.deleted == False)
    ).first()

    if not person:
        raise HTTPException(status_code=404, detail="Persona no encontrada")

    return person


def update_person(session: Session, person_id: int, data: PersonUpdate) -> Person:

    person = get_person(session, person_id)
    update_data = data.model_dump(exclude_unset=True)

    tipo_documento = update_data.get("tipo_documento", person.tipo_documento)
    numero_documento = update_data.get("numero_documento", person.numero_documento)
    if (
        tipo_documento != person.tipo_documento
        or numero_documento != person.numero_documento
    ):
        _ensure_document_available(
            session,
            tipo_documento,
            numero_documento,
            exclude_person_id=person_id,
        )

    for key, value in update_data.items():
        setattr(person, key, value)

    person.updated_at = datetime.now(UTC)
    session.add(person)
    session.commit()
    session.refresh(person)
    return person


def delete_person(session: Session, person_id: int) -> Person:

    person = get_person(session, person_id)
    person.deleted = True
    person.deleted_at = datetime.now(UTC)
    person.updated_at = datetime.now(UTC)
    session.add(person)
    session.commit()
    session.refresh(person)
    return person


def reactivate_person(session: Session, person_id: int) -> Person:
    person = session.get(Person, person_id)
    if person is None:
        raise HTTPException(status_code=404, detail="Persona no encontrada")
    if not person.deleted:
        raise HTTPException(status_code=409, detail="La persona ya está activa")

    _ensure_document_available(
        session,
        person.tipo_documento,
        person.numero_documento,
        exclude_person_id=person_id,
    )
    person.deleted = False
    person.deleted_at = None
    person.updated_at = datetime.now(UTC)
    session.add(person)
    session.commit()
    session.refresh(person)
    return person
