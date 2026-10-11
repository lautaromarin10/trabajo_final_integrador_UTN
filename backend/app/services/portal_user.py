from datetime import datetime, timezone

from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.sql.elements import ColumnElement
from sqlmodel import Session, col, select

from app.core.roles import PortalRole
from app.core.security import hash_password
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


def register_portal_user(data: RegisterRequest, session: Session) -> PortalUser:
    if session.exec(
        select(PortalUser).where(PortalUser.email == data.email)
    ).first():
        raise HTTPException(
            status_code=409,
            detail="Ya existe una cuenta con ese email",
        )

    person_data = data.model_dump(exclude={"email", "password"})
    _ensure_document_available(
        session, person_data["tipo_documento"], person_data["numero_documento"]
    )
    person = Person(**person_data)
    session.add(person)
    session.flush()

    portal_user = PortalUser(
        persona_id=person.id,
        email=str(data.email),
        password_hash=hash_password(data.password),
        role=PortalRole.USER,
    )
    session.add(portal_user)
    session.commit()
    session.refresh(portal_user)
    return portal_user


def create_portal_user(data: PortalUserCreate, session: Session) -> PortalUser:
    existing = session.exec(
        select(PortalUser).where(PortalUser.email == data.email)
    ).first()

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
    session.add(portal_user)
    session.commit()
    session.refresh(portal_user)
    return portal_user


def get_portal_users(
    session: Session,
    skip: int = 0,
    limit: int = 20,
    email: str | None = None,
    role: PortalRole | None = None,
) -> PortalUserPage:
    filters: list[ColumnElement[bool]] = [col(PortalUser.deleted) == False]
    if email:
        filters.append(
            func.lower(col(PortalUser.email)).like(f"%{email.lower()}%")
        )
    if role:
        filters.append(col(PortalUser.role) == role)

    total = session.exec(
        select(func.count()).select_from(PortalUser).where(*filters)
    ).one()
    items = session.exec(
        select(PortalUser)
        .where(*filters)
        .order_by(col(PortalUser.id))
        .offset(skip)
        .limit(limit)
    ).all()
    return PortalUserPage(
        total=total,
        items=[PortalUserRead.model_validate(user) for user in items],
        hasNextPage=skip + len(items) < total,
        hasPrevPage=skip > 0 and total > 0,
    )


def get_portal_user(session: Session, portal_user_id: int) -> PortalUser:
    portal_user = session.exec(
        select(PortalUser).where(
            PortalUser.id == portal_user_id,
            PortalUser.deleted  == False,
        )
    ).first()
    if not portal_user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return portal_user


def update_portal_user(
    portal_user_id: int,
    data: PortalUserUpdate,
    session: Session,
) -> PortalUser:
    portal_user = get_portal_user(session, portal_user_id)
    update_data = data.model_dump(exclude_unset=True)
    person_fields = PersonUpdate.model_fields.keys()
    person_data = {
        key: update_data.pop(key)
        for key in list(update_data)
        if key in person_fields
    }

    if "password" in update_data:
        password = update_data.pop("password")
        update_data["password_hash"] = hash_password(password)

    if person_data:
        person_id = update_data.get("persona_id", portal_user.persona_id)
        person = session.get(Person, person_id) if person_id is not None else None
        if person is None or person.deleted:
            raise HTTPException(
                status_code=409,
                detail="El usuario no tiene una persona activa asociada",
            )

        tipo_documento = person_data.get("tipo_documento", person.tipo_documento)
        numero_documento = person_data.get(
            "numero_documento", person.numero_documento
        )
        if (
            tipo_documento != person.tipo_documento
            or numero_documento != person.numero_documento
        ):
            _ensure_document_available(
                session,
                tipo_documento,
                numero_documento,
                exclude_person_id=person.id,
            )

        for key, value in person_data.items():
            setattr(person, key, value)
        person.updated_at = datetime.now(timezone.utc)
        session.add(person)

    for key, value in update_data.items():
        setattr(portal_user, key, value)

    portal_user.updated_at = datetime.now(timezone.utc)
    session.add(portal_user)
    session.commit()
    session.refresh(portal_user)
    return portal_user


def delete_portal_user(session: Session, portal_user_id: int) -> PortalUser:
    portal_user = get_portal_user(session, portal_user_id)
    portal_user.deleted = True
    portal_user.deleted_at = datetime.now(timezone.utc)
    portal_user.updated_at = datetime.now(timezone.utc)
    session.add(portal_user)
    session.commit()
    session.refresh(portal_user)
    return portal_user


def reactivate_portal_user(session: Session, portal_user_id: int) -> PortalUser:
    portal_user = session.get(PortalUser, portal_user_id)
    if portal_user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    if not portal_user.deleted:
        raise HTTPException(status_code=409, detail="El usuario ya está activo")

    portal_user.deleted = False
    portal_user.deleted_at = None
    portal_user.updated_at = datetime.now(timezone.utc)
    session.add(portal_user)
    session.commit()
    session.refresh(portal_user)
    return portal_user
