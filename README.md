# TaskFlow API — Programación de aplicaciones web

**Alumna:** Alba Casado García · 2º DAW
**Profesor:** Luis Vicente Viñas

Backend de **TaskFlow**, una API REST con **FastAPI** para gestionar proyectos, tareas y categorías. El proyecto va creciendo práctica a práctica y cada práctica tiene su **tag** en Git.

## Índice del curso

### 1ª evaluación

- [**Tema 1 — API REST con FastAPI (backend)**](docs/1-evaluacion/tema-1-api-rest-fastapi/README.md): prácticas 1.1 a 1.7

## Estructura del backend

    app/
    ├── main.py            crea la app e incluye routers y middlewares
    ├── models.py          tablas de la BD (SQLAlchemy)
    ├── schemas.py         datos que entran y salen (Pydantic)
    ├── core/
    │   ├── middlewares.py CORS, X-Process-Time, errores
    │   ├── database.py    conexión a SQLite y get_db()
    │   └── security.py    contraseñas, JWT y get_current_user
    └── routers/
        ├── auth.py        registro y login
        ├── tasks.py
        ├── projects.py
        └── categories.py

## Cómo arrancar

    python -m venv venv
    venv\Scripts\activate
    python -m pip install -r requirements.txt
    python -m uvicorn app.main:app --reload

Swagger: http://127.0.0.1:8000/docs
