# =====================================================================
# TASKFLOW API - Archivo principal (app/main.py)
#
# Práctica 1.1 -> endpoints /health, /version y /ping
# Práctica 1.3 -> main.py solo crea la app e incluye los routers
# Práctica 1.4 -> middlewares y handler global de errores, separados
#                 en app/core/middlewares.py
# =====================================================================

from fastapi import FastAPI

from app.routers import tasks, projects

# Función que registra CORS, X-Process-Time y el handler de errores
from app.core.middlewares import registrar_middlewares

app = FastAPI()

# Registramos los routers (Práctica 1.3)
app.include_router(tasks.router)
app.include_router(projects.router)

# Registramos los middlewares (Práctica 1.4)
registrar_middlewares(app)


# =====================================================================
# Endpoints de sistema (Práctica 1.1)
# =====================================================================
@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/version")
def version():
    return {"version": "1.0.0"}


@app.get("/ping")
def ping():
    return {"message": "pong"}


# GET /error-prueba -> SOLO para probar el handler global (Práctica 1.4).
# Provoca un error a propósito para comprobar que el servidor no se rompe.
@app.get("/error-prueba")
def error_prueba():
    raise Exception("Error forzado para probar el handler")