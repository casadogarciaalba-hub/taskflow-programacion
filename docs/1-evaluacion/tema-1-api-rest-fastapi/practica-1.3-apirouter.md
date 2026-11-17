# Práctica 1.3 — Organización con APIRouter

**Tag:** `practica-1.3` · Entrega en PDF: [Practica_1.3_APIRouter_Alba_Casado.pdf](entregas/Practica_1.3_APIRouter_Alba_Casado.pdf)

## Qué se hizo

- Crear la carpeta `app/routers/` con un archivo por recurso:
  - `tasks.py` → `router = APIRouter(prefix="/tasks", tags=["tasks"])`
  - `projects.py` → `router = APIRouter(prefix="/projects", tags=["projects"])`
- Mover el `POST /tasks` de `main.py` a su router.
- En `main.py` solo queda crear la app e incluir los routers con `app.include_router(...)`.

## Conceptos

- **APIRouter** es como un "mini FastAPI" para agrupar las rutas de un mismo recurso.
- **prefix**: todas las rutas del archivo empiezan por él, así que dentro se escribe `""` o `"/{id}"`.
- **tags**: agrupan los endpoints en Swagger.
- **Separación de responsabilidades**: cada archivo se encarga de una cosa y el código es más fácil de mantener.

## Problema en el instituto

`uvicorn.exe` está bloqueado por la directiva de Control de aplicaciones de Windows. Solución: `python -m uvicorn app.main:app --reload`.

## Archivos

`app/routers/__init__.py`, `app/routers/tasks.py`, `app/routers/projects.py` (nuevos), `app/main.py`
