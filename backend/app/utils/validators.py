from typing import Any


# Usar en validadores de schemas para rechazar null en campos opcionales de PATCH
# que pueden omitirse, pero no deben limpiarse explícitamente.
def reject_null_value(value: Any) -> Any:
    if value is None:
        raise ValueError("No se puede enviar null para este campo")
    return value
