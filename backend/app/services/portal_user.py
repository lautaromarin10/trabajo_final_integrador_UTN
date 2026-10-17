from fastapi import HTTPException

from app.core.roles import PortalRole
from app.core.security import hash_password
from app.core.unit_of_work import UnitOfWork
from app.models.person import Person
from app.models.portal_user import PortalUser
from app.schemas.auth import RegisterRequest
from app.schemas.person import PersonUpdate
from app.schemas.portal_user import (
    PortalUserCreate,
    PortalUserPage,
    PortalUserRead,
    PortalUserUpdate,
)
from app.services.person import _ensure_document_available


def register_portal_user(data: RegisterRequest, unit_of_work: UnitOfWork) -> PortalUser:
    if unit_of_work.portal_users.get_by_email(data.email, include_deleted=True):
        raise HTTPException(
            status_code=409,
            detail="Ya existe una cuenta con ese email",
        )

    person_data = data.model_dump(exclude={"email", "password"})
    _ensure_document_available(
        unit_of_work, person_data["tipo_documento"], person_data["numero_documento"]
    )
    person = Person(**person_data)
    unit_of_work.persons.add(person)
    unit_of_work.persons.flush()

    portal_user = PortalUser(
        persona_id=person.id,
        email=str(data.email),
        password_hash=hash_password(data.password),
        role=PortalRole.USER,
    )
    return unit_of_work.portal_users.add(portal_user)


def create_portal_user(data: PortalUserCreate, unit_of_work: UnitOfWork) -> PortalUser:
    existing = unit_of_work.portal_users.get_by_email(data.email, include_deleted=True)

    if existing:
        detail = (
            "El email pertenece a una cuenta eliminada; debe reactivarse "
            "en lugar de crear otra"
            if existing.deleted
            else "Ya existe una cuenta activa con ese email"
        )
        raise HTTPException(status_code=409, detail=detail)

    portal_user_data = data.model_dump(exclude={"password"})
    portal_user_data["password_hash"] = hash_password(data.password)
    portal_user = PortalUser(**portal_user_data)
    return unit_of_work.portal_users.add(portal_user)


def get_portal_users(
    unit_of_work: UnitOfWork,
    skip: int = 0,
    limit: int = 20,
    email: str | None = None,
    role: PortalRole | None = None,
) -> PortalUserPage:
    total, items = unit_of_work.portal_users.get_page(skip, limit, email, role)
    return PortalUserPage(
        total=total,
        items=[PortalUserRead.model_validate(user) for user in items],
        hasNextPage=skip + len(items) < total,
        hasPrevPage=skip > 0 and total > 0,
    )


def get_portal_user(unit_of_work: UnitOfWork, portal_user_id: int) -> PortalUser:
    portal_user = unit_of_work.portal_users.get_active(portal_user_id)
    if not portal_user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return portal_user


def update_portal_user(
    portal_user_id: int,
    data: PortalUserUpdate,
    unit_of_work: UnitOfWork,
) -> PortalUser:
    portal_user = get_portal_user(unit_of_work, portal_user_id)
    update_data = data.model_dump(exclude_unset=True)
    person_fields = PersonUpdate.model_fields.keys()
    person_data = {
        key: update_data.pop(key) for key in list(update_data) if key in person_fields
    }

    if "password" in update_data:
        password = update_data.pop("password")
        update_data["password_hash"] = hash_password(password)

    if person_data:
        person_id = update_data.get("persona_id", portal_user.persona_id)
        person = unit_of_work.persons.get(person_id) if person_id is not None else None
        if person is None or person.deleted:
            raise HTTPException(
                status_code=409,
                detail="El usuario no tiene una persona activa asociada",
            )

        tipo_documento = person_data.get("tipo_documento", person.tipo_documento)
        numero_documento = person_data.get("numero_documento", person.numero_documento)
        if (
            tipo_documento != person.tipo_documento
            or numero_documento != person.numero_documento
        ):
            _ensure_document_available(
                unit_of_work,
                tipo_documento,
                numero_documento,
                exclude_person_id=person.id,
            )

        unit_of_work.persons.update_fields(person, person_data)
        unit_of_work.persons.add(person)

    unit_of_work.portal_users.update_fields(portal_user, update_data)
    return unit_of_work.portal_users.add(portal_user)


def delete_portal_user(unit_of_work: UnitOfWork, portal_user_id: int) -> PortalUser:
    portal_user = get_portal_user(unit_of_work, portal_user_id)
    return unit_of_work.portal_users.soft_delete(portal_user)


def reactivate_portal_user(unit_of_work: UnitOfWork, portal_user_id: int) -> PortalUser:
    portal_user = unit_of_work.portal_users.get(portal_user_id)
    if portal_user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    if not portal_user.deleted:
        raise HTTPException(status_code=409, detail="El usuario ya está activo")

    return unit_of_work.portal_users.reactivate(portal_user)
