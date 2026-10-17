# Responsabilidades de las capas

Cada capa separa responsabilidades, reglas de negocio, persistencia y HTTP.

## Routers

- Define rutas, métodos, parámetros y códigos de respuesta
- Convierte las llamadas HTTP validas en una llamada a service
- Declara autenticación y permisos generales del endpoint
- No consulta ni modifica las entidades directamente ni controla transacciones

## Services

- Coordina las operaciones entre los repositories
- Aplica validación y reglas de negocio
- Recibe UnitOfWork y usa sus repositorios para leer o cambiar datos
- No hace rollback, commit o close.

## Repositories

- Encapsula el acceso a los datos con SQLModel
- Comparte la sesión recibida del UnitOfWork
- Con Add y otros métodos prepara los cambios pero no confirma la transacción
- No decide permisos ni regla de negocios

## Unit of Work (`app/core/unit_of_work.py`)

- Crea una sessión por request y construye los repositories que comparten dicha sessión
- Se asegura de mantener la atomicidad de las operaciones mediante rollback o commit
- No contiene consultas ni reglas de negocio
- Se tiene que inyectar en los routers mediante UnitOfWorkDep

## Flujo esperado

```text
Request → Router → Servicio → Repositorios → Base de datos
                    ↕             ↕
                 Unit of Work (misma sesión y transacción)
```

Las lecturas también usan el `UnitOfWork` del request, para que autenticación y servicio trabajen con la misma sesión cuando ambas intervienen en una operación.
