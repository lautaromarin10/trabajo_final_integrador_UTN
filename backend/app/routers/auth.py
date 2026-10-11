from datetime import UTC, datetime

from fastapi import APIRouter, HTTPException, status
from sqlmodel import select

from app.core.auth import CurrentUserDep
from app.core.database import SessionDep
from app.core.security import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    create_access_token,
    verify_password,
)
from app.models.person import Person
from app.models.portal_user import PortalUser
from app.schemas.auth import LoginRequest, LoginResponse, RegisterRequest
from app.schemas.portal_user import PortalUserProfile, PortalUserRead
from app.services.portal_user import (
    register_portal_user as register_portal_user_service,
)

router = APIRouter(prefix="/auth", tags=["Autorización"])


@router.post(
    "/register",
    response_model=PortalUserRead,
    status_code=status.HTTP_201_CREATED,
)
def register_user(data: RegisterRequest, session: SessionDep) -> PortalUser:
    return register_portal_user_service(data, session)


@router.get("/me", response_model=PortalUserProfile)
def get_current_user_profile(
    current_user: CurrentUserDep,
    session: SessionDep,
) -> dict:
    person = (
        session.get(Person, current_user.persona_id)
        if current_user.persona_id is not None
        else None
    )
    return {
        **PortalUserRead.model_validate(current_user).model_dump(),
        "persona": person,
    }


@router.post("/login", response_model=LoginResponse)
def login_user(credentials: LoginRequest, session: SessionDep) -> LoginResponse:
    portal_user = session.exec(
        select(PortalUser).where(
            PortalUser.email == credentials.email,
            PortalUser.deleted == False,
        )
    ).first()

    if not portal_user or not verify_password(
        credentials.password, portal_user.password_hash
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = create_access_token(portal_user.email, portal_user.role)
    portal_user.ultimo_ingreso = datetime.now(UTC)
    session.add(portal_user)
    session.commit()

    return LoginResponse(
        access_token=token,
        expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )
