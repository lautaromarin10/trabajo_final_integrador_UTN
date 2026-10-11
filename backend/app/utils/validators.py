import re
from typing import Annotated, Any

from pydantic import AfterValidator, Field


def validate_password_strength(value: str) -> str:
    if not re.search(r"[A-Z]", value) or not re.search(r"[^A-Za-z0-9\s]", value):
        raise ValueError(
            "La contraseña debe incluir al menos una mayúscula y un símbolo"
        )
    return value


Password = Annotated[
    str,
    Field(
        min_length=6,
        max_length=128,
        description="Mínimo 6 caracteres, una mayúscula y un símbolo",
    ),
    AfterValidator(validate_password_strength),
]

# Usar en validadores de schemas para rechazar null en campos opcionales de PATCH
# que pueden omitirse, pero no deben limpiarse explícitamente.
def reject_null_value(value: Any) -> Any:
    if value is None:
        raise ValueError("No se puede enviar null para este campo")
    return value
