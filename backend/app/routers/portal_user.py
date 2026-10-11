from typing import Annotated

from fastapi import APIRouter, HTTPException, Path, Query, Response, status

from app.core.auth import AdminUserDep, CurrentUserDep
from app.core.database import SessionDep
from app.core.roles import PortalRole
from app.models.portal_user import PortalUser
from app.schemas.portal_user import (
    PortalUserCreate,
    PortalUserPage,
    PortalUserRead,
    PortalUserUpdate,
)
from app.services.portal_user import (
    create_portal_user as create_portal_user_service,
    delete_portal_user as delete_portal_user_service,
    get_portal_user as get_portal_user_service,
    get_portal_users as get_portal_users_service,
    reactivate_portal_user as reactivate_portal_user_service,
    update_portal_user as update_portal_user_service,
)


router = APIRouter(
    prefix="/portal-user",
    tags=["Usuario Portal"],
)


@router.post(
    "/",
    response_model=PortalUserRead,
    status_code=status.HTTP_201_CREATED,
)
def create_portal_user(
    portal_user: PortalUserCreate,
    session: SessionDep,
    _: AdminUserDep,
) -> PortalUser:
    return create_portal_user_service(portal_user, session)


@router.get("/", response_model=PortalUserPage)
def get_users_portals(
    session: SessionDep,
    _: AdminUserDep,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    email: str | None = Query(None, min_length=1, max_length=255),
    role: PortalRole | None = None,
) -> PortalUserPage:
    return get_portal_users_service(session, skip, limit, email, role)


@router.get("/{portal_user_id}", response_model=PortalUserRead)
def get_user_portal(
    portal_user_id: Annotated[int, Path(gt=0)],
    session: SessionDep,
    _: AdminUserDep,
) -> PortalUser:
    return get_portal_user_service(session, portal_user_id)


@router.patch("/{portal_user_id}", response_model=PortalUserRead)
def update_user_portal(
    portal_user: PortalUserUpdate,
    portal_user_id: Annotated[int, Path(gt=0)],
    session: SessionDep,
    current_user: CurrentUserDep,
) -> PortalUser:
    if current_user.role != PortalRole.ADMIN:
        if current_user.id != portal_user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Solo podés modificar tus propios datos personales",
            )
        if portal_user.model_fields_set & {"persona_id", "role", "password"}:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tenés permiso para modificar campos administrativos",
            )
    return update_portal_user_service(portal_user_id, portal_user, session)


@router.delete("/{portal_user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_portal(
    portal_user_id: Annotated[int, Path(gt=0)],
    session: SessionDep,
    _: AdminUserDep,
) -> Response:
    delete_portal_user_service(session, portal_user_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/{portal_user_id}/reactivate", response_model=PortalUserRead)
def reactivate_user_portal(
    portal_user_id: Annotated[int, Path(gt=0)],
    session: SessionDep,
    _: AdminUserDep,
) -> PortalUser:
    return reactivate_portal_user_service(session, portal_user_id)
