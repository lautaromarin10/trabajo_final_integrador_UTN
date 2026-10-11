import os
from datetime import datetime, timedelta, timezone

import bcrypt
import jwt

from app.core.roles import PortalRole


ACCESS_TOKEN_EXPIRE_MINUTES = 30
JWT_ALGORITHM = "HS256"


def create_access_token(subject: str, role: PortalRole) -> str:
    secret_key = os.getenv("JWT_SECRET_KEY")
    if not secret_key:
        raise RuntimeError("La variable JWT_SECRET_KEY es requerida")

    expires_at = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )
    return jwt.encode(
        {"sub": subject, "role": role.value, "exp": expires_at},
        secret_key,
        algorithm=JWT_ALGORITHM,
    )


def decode_access_token(token: str) -> str:
    secret_key = os.getenv("JWT_SECRET_KEY")
    if not secret_key:
        raise RuntimeError("La variable JWT_SECRET_KEY es requerida")

    payload = jwt.decode(token, secret_key, algorithms=[JWT_ALGORITHM])
    subject = payload.get("sub")
    if not isinstance(subject, str) or not subject:
        raise jwt.InvalidTokenError("El token no contiene un sujeto válido")
    return subject


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(password: str, password_hash: str) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8"))
