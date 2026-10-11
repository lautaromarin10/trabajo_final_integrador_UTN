from enum import Enum


class PortalRole(str, Enum):
    ADMIN = "admin"
    USER = "user"
