# Práctica 1.6 — CRUD completo con la base de datos

**Tag:** `practica-1.6` · Colección de Postman: [`postman/TaskFlow_Practica_1.6.postman_collection.json`](../../../postman/TaskFlow_Practica_1.6.postman_collection.json)

## Qué se hizo

CRUD real (los datos ya se guardan en `taskflow.db`) de tres recursos:

| Recurso | Endpoints |
|---|---|
| tasks | `GET /tasks` (filtros `project_id`, `completed` y paginación `skip`/`limit`), `GET /tasks/{id}`, `POST`, `PUT`, `DELETE` |
| projects | `GET /projects`, `GET /projects/{id}` (con sus tareas), `POST`, `PUT`, `DELETE` |
| categories | `GET /categories`, `GET /categories/{id}` (con sus tareas), `POST`, `PUT`, `DELETE` (router nuevo) |

- **404** si el recurso no existe, y al crear una tarea se comprueba que el proyecto y la categoría existen.
- **409** si se repite el nombre de una categoría.
- Schemas nuevos: `TaskUpdate`, `CategoryCreate`/`CategoryRead`, `ProjectWithTasks`, `CategoryWithTasks`, y `from_attributes=True` para que Pydantic lea los modelos de SQLAlchemy.

## Decisiones al borrar

- **Proyecto → borrado en cascada**: una tarea no tiene sentido sin proyecto (`project_id` es obligatorio).
- **Categoría → bloqueo (409)** si tiene tareas: la categoría es solo una etiqueta y no quiero perder tareas válidas.

## Conceptos

- `db.add()` → `db.commit()` → `db.refresh()` para guardar y recuperar el `id`.
- `query().filter().offset().limit()` para filtros y paginación.
- `Query(ge=..., le=...)` para limitar los parámetros de la URL.

## Archivos

`app/routers/categories.py` (nuevo), `app/routers/tasks.py`, `app/routers/projects.py`, `app/schemas.py`, `app/main.py`, carpeta `postman/`
