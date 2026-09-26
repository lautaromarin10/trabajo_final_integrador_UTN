```mermaid
erDiagram
    HOTEL ||--o{ HABITACION : tiene
    TIPO_HABITACION ||--o{ HABITACION : define

    HOTEL ||--o{ RESERVA : gestiona
    CLIENTE ||--o{ RESERVA : realiza
    USUARIO_PORTAL o|--o{ RESERVA : crea
    RESERVA ||--o{ HISTORIAL_ESTADO_RESERVA : registra

    RESERVA ||--o{ RESERVA_HUESPED : incluye
    HUESPED ||--o{ RESERVA_HUESPED : participa
    HABITACION ||--o{ RESERVA_HUESPED : ocupa

    PERSONA ||--o| CLIENTE : es
    PERSONA ||--o| HUESPED : es
    PERSONA ||--o| USUARIO_PORTAL : es

    ROL ||--o{ USUARIO_PORTAL : asigna
    ORIGEN_CLIENTE ||--o{ CLIENTE : define

    HOTEL {
        int id PK
        string nombre
        string descripcion
        string telefono
        string email
    }

    TIPO_HABITACION {
        int id PK
        string nombre
        string descripcion
        int capacidad_adultos
        int capacidad_ninos
        int cantidad_camas
        float tamanio_m2
    }

    HABITACION {
        int id PK
        int hotel_id FK
        int tipo_habitacion_id FK
        string numero
        string descripcion
        int piso
        string estado_habitacion
        string estado_limpieza
    }

    PERSONA {
        int id PK
        string nombre
        string apellido
        string tipo_documento
        string numero_documento
        date fecha_nacimiento
        string nacionalidad
        string observaciones
    }

    CLIENTE {
        int id PK
        int persona_id FK
        string email
        string telefono
        string direccion
        string ciudad
        string origen_cliente
    }

    ORIGEN_CLIENTE {
        int id PK
        string nombre
    }

    ROL {
        int id PK
        string nombre
    }

    USUARIO_PORTAL {
        int id PK
        int persona_id FK
        int rol_id FK
        string email
        string password_hash
        datetime ultimo_ingreso
    }

    RESERVA {
        int id PK
        int hotel_id FK
        int cliente_id FK
        int usuario_creador_id FK
        string codigo
        datetime fecha_reserva
        date check_in
        date check_out
        int cantidad_adultos
        int cantidad_ninos
        string estado
        string origen
        string observaciones
    }

    HISTORIAL_ESTADO_RESERVA {
        int id PK
        int reserva_id FK
        string estado_anterior
        string estado_nuevo
        datetime fecha_cambio
        string motivo
    }

    HUESPED {
        int id PK
        int persona_id FK
    }

    RESERVA_HUESPED {
        int id PK
        int reserva_id FK
        int huesped_id FK
        int habitacion_id FK
    }
```

## Consideración

- Todas las tablas van a contar con las siguientes columnas base:
  - datetime created_at
  - datetime updated_at
  - boolean delete
  - datetime deleted_at

- Todos los registros deben ser marcados como eliminados con soft delete.
