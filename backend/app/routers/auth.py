import os
from datetime import UTC, datetime

from fastapi import APIRouter, HTTPException, Response, status

from app.core.auth import CurrentUserDep
from app.core.database import UnitOfWorkDep
from app.core.security import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    create_access_token,
    verify_password,
)
from app.models.portal_user import PortalUser
from app.schemas.auth import LoginRequest, LoginResponse, RegisterRequest
from app.schemas.portal_user import PortalUserProfile, PortalUserRead
from app.services.portal_user import (
    register_portal_user as register_portal_user_service,
)

router = APIRouter(prefix="/auth", tags=["Autorización"])
ACCESS_TOKEN_COOKIE = "access_token"
COOKIE_SECURE = os.getenv("PRODUCTION", "false").strip().lower() == "true"


@router.post(
    "/register",
    response_model=PortalUserRead,
    status_code=status.HTTP_201_CREATED,
)
def register_user(data: RegisterRequest, unit_of_work: UnitOfWorkDep) -> PortalUser:
    return register_portal_user_service(data, unit_of_work)


@router.get("/me", response_model=PortalUserProfile)
def get_current_user_profile(
    current_user: CurrentUserDep,
    unit_of_work: UnitOfWorkDep,
) -> dict:
    person = (
        unit_of_work.persons.get(current_user.persona_id)
        if current_user.persona_id is not None
        else None
    )
    return {
        **PortalUserRead.model_validate(current_user).model_dump(),
        "persona": person,
    }


@router.post("/login", response_model=LoginResponse)
def login_user(
    credentials: LoginRequest,
    response: Response,
    unit_of_work: UnitOfWorkDep,
) -> LoginResponse:
    portal_user = unit_of_work.portal_users.get_by_email(credentials.email)

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
    unit_of_work.portal_users.add(portal_user)

    response.set_cookie(
        key=ACCESS_TOKEN_COOKIE,
        value=token,
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        httponly=True,
        secure=COOKIE_SECURE,
        samesite="lax",
        path="/",
    )
    return LoginResponse(
        expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout_user() -> Response:
    response = Response(status_code=status.HTTP_204_NO_CONTENT)
    response.delete_cookie(
        key=ACCESS_TOKEN_COOKIE,
        httponly=True,
        secure=COOKIE_SECURE,
        samesite="lax",
        path="/",
    )
    return response
