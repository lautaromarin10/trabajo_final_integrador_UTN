from typing import Annotated

import jwt
from fastapi import Cookie, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.database import UnitOfWorkDep
from app.core.roles import PortalRole
from app.core.security import decode_access_token
from app.models.portal_user import PortalUser

bearer_scheme = HTTPBearer(auto_error=False)


def get_current_user(
    credentials: Annotated[
        HTTPAuthorizationCredentials | None,
        Depends(bearer_scheme),
    ],
    unit_of_work: UnitOfWorkDep,
    access_token: Annotated[str | None, Cookie()] = None,
) -> PortalUser:
    unauthorized = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Autenticación requerida",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token = credentials.credentials if credentials else access_token
    if token is None:
        raise unauthorized

    try:
        email = decode_access_token(token)
    except jwt.InvalidTokenError:
        raise unauthorized from None

    user = unit_of_work.portal_users.get_by_email(email)
    if user is None:
        raise unauthorized
    return user


def require_admin(user: Annotated[PortalUser, Depends(get_current_user)]) -> PortalUser:
    if user.role != PortalRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Se requiere rol de administrador",
        )
    return user


CurrentUserDep = Annotated[PortalUser, Depends(get_current_user)]
AdminUserDep = Annotated[PortalUser, Depends(require_admin)]
