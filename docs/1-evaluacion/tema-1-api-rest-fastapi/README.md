# Tema 1 — API REST con FastAPI (backend)

**1ª evaluación** · Todas las prácticas de este tema van construyendo el mismo backend, **TaskFlow API**, paso a paso. Cada práctica tiene su **tag** en Git para poder ver el código tal y como quedó.

| Práctica | Qué se hizo | Tag | Documentación |
|---|---|---|---|
| 1.1 | Estructura inicial y primeros endpoints | `practica-1.1` | [ver](practica-1.1-estructura-inicial.md) |
| 1.2 | Schemas con Pydantic | `practica-1.2` | [ver](practica-1.2-schemas-pydantic.md) |
| 1.3 | Organización con APIRouter | `practica-1.3` | [ver](practica-1.3-apirouter.md) |
| 1.4 | Middleware, CORS y errores | `practica-1.4` | [ver](practica-1.4-middleware.md) |
| 1.5 | Modelos SQLAlchemy y conexión a BD | `practica-1.5` | [ver](practica-1.5-sqlalchemy.md) |
| 1.6 | CRUD completo | `practica-1.6` | [ver](practica-1.6-crud.md) |
| 1.7 | Autenticación JWT | `practica-1.7` | [ver](practica-1.7-autenticacion-jwt.md) |

Los PDF entregados están en la carpeta [`entregas`](entregas/).

## Cómo ver el código de una práctica concreta

En GitHub: botón de la rama (`main`) → pestaña **Tags** → elegir la práctica.

## Evolución del backend

    1.1  main.py con /health, /version y /ping
    1.2  + schemas.py (Pydantic valida lo que entra y lo que sale)
    1.3  + routers/ (tasks y projects separados de main.py)
    1.4  + core/middlewares.py (CORS, X-Process-Time, errores)
    1.5  + core/database.py y models.py (SQLite con SQLAlchemy)
    1.6  + CRUD real y router de categories
    1.7  + core/security.py y routers/auth.py (login con JWT)
