# Práctica 1.5 — Modelos SQLAlchemy y conexión a BD

**Tag:** `practica-1.5` · Entrega en PDF: [Practica_1.5_SQLAlchemy_Alba_Casado.pdf](entregas/Practica_1.5_SQLAlchemy_Alba_Casado.pdf)

## Qué se hizo

- `app/core/database.py`: `engine` (SQLite, fichero `taskflow.db`), `SessionLocal`, `Base` y la dependencia `get_db()`, que abre una sesión por petición y la cierra siempre con `try/finally`.
- `app/models.py`: modelos `User`, `Project`, `Category` y `Task`. `Task` tiene FK a `Project` (obligatoria), a `Category` y a `User`.
- `Base.metadata.create_all(bind=engine)` en `main.py` crea las tablas al arrancar.
- `db: Session = Depends(get_db)` en los endpoints.
- `taskflow.db` al `.gitignore`.

## Esquema

```
projects 1 ──── N tasks N ──── 1 categories
                   N
                   │
                   1
                 users
```

- Al borrar un proyecto se borran sus tareas (`cascade="all, delete-orphan"`).
- Todos los usuarios pueden acceder a todos los proyectos, por eso `Project` no tiene dueño.

## Conceptos

- **ORM**: traduce clases de Python a tablas (clase = tabla, atributo = columna, objeto = fila).
- **`relationship` y `back_populates`**: navegar entre objetos (`proyecto.tasks`, `tarea.project`).
- **Pool de conexiones**: `db.close()` no destruye la conexión, la devuelve al pool.

## Problemas en el instituto

- `pip.exe` bloqueado → `python -m pip install ...`
- SQLAlchemy 2.1 trae `.pyd` compilados que también se bloquean → instalar `sqlalchemy<2.1` y poner `os.environ["DISABLE_SQLALCHEMY_CEXT_RUNTIME"] = "1"` antes del import.

## Archivos

`app/core/database.py`, `app/models.py` (nuevos), `app/main.py`, `app/routers/*.py`, `.gitignore`, `requirements.txt`
