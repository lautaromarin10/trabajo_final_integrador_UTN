# BACKEND

## Requisitos

- Python 3
- pip
- PostgreSQL Accesible desde el backend

## Configuración

Desde la carpeta backend, creá y activa un entorno virtual

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Instalar dependencias

```bash
python -m pip install -r requirements.txt
```

## Como ejecutarlo

Desde la carpeta backend, con el entorno virtual activado

```bash
uvicorn main:app --reload --env-file ../.env
```

### Consideración

- Tener configurado **DATABASE_URL** en .env de la raíz del repositorio.
