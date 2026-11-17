# Práctica 1.1 — Estructura inicial con FastAPI

**Tag:** `practica-1.1`

## Qué se hizo

- Crear el proyecto con su entorno virtual (`venv`) y `requirements.txt`.
- Crear la carpeta `app/` con `main.py`, que es donde se crea la aplicación (`app = FastAPI()`).
- Primeros endpoints de sistema:
  - `GET /health` → `{"status": "ok"}`
  - `GET /version` → `{"version": "1.0.0"}`
  - `GET /ping` → `{"message": "pong"}`
- Arrancar con `uvicorn app.main:app --reload` y probar en Swagger (`/docs`).
- `.gitignore` para no subir `venv/` ni `__pycache__/`.

## Conceptos

- **FastAPI**: framework de Python para hacer APIs REST. Genera la documentación de Swagger automáticamente.
- **Uvicorn**: el servidor que ejecuta la aplicación. `app.main:app` significa "el objeto `app` del archivo `app/main.py`".
- **--reload**: reinicia el servidor solo cada vez que guardo un cambio.
- **Entorno virtual**: carpeta con las librerías del proyecto, separadas de las del sistema.

## Archivos

`app/__init__.py`, `app/main.py`, `requirements.txt`, `.gitignore`, `README.md`
