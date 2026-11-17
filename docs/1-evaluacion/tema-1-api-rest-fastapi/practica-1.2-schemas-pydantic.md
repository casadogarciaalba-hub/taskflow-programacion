# Práctica 1.2 — Schemas con Pydantic

**Tag:** `practica-1.2`

## Qué se hizo

- Crear `app/schemas.py` con los schemas de tareas y proyectos:
  - `TaskCreate`: lo que **envía** el cliente para crear una tarea (`title` obligatorio de 1 a 100 caracteres, `description` opcional, `project_id`).
  - `TaskRead`: lo que **devuelve** la API (lo anterior más `id`, `completed`, `created_at`).
  - `ProjectCreate` / `ProjectRead`, con la misma idea.
- Endpoint temporal `POST /tasks` en `main.py` que valida con `TaskCreate` y devuelve una tarea simulada (todavía no hay base de datos).

## Conceptos

- **Pydantic** valida los datos automáticamente: si el título está vacío o es demasiado largo, FastAPI devuelve **422** diciendo qué campo falla.
- **Separar Create y Read**: lo que entra no es lo mismo que lo que sale (el cliente no manda el `id`, lo pone la API).
- **`response_model`**: el contrato de salida; FastAPI filtra la respuesta según ese schema.
- **`status_code=201`**: "Created", el código correcto cuando se crea algo.

## Archivos

`app/schemas.py` (nuevo), `app/main.py`
