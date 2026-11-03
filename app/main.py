# =====================================================================
# TASKFLOW API - Archivo principal (app/main.py)
#
# Práctica 1.1 -> endpoints /health, /version y /ping
# Práctica 1.3 -> main.py SOLO crea la app e incluye los routers.
#                 Las rutas de negocio (tareas y proyectos) están
#                 ahora en app/routers/
# =====================================================================

# FastAPI: framework con el que creamos la API
from fastapi import FastAPI

# Importamos los routers que hemos creado en app/routers/
from app.routers import tasks, projects

# Creamos la aplicación. "app" es lo que arranca uvicorn (app.main:app)
app = FastAPI()

# Registramos los routers en la app.
# Así FastAPI añade sus rutas (/tasks y /projects) a la API.
app.include_router(tasks.router)
app.include_router(projects.router)


# =====================================================================
# Endpoints de sistema (Práctica 1.1)
# No son rutas de negocio, solo comprueban que la API funciona,
# por eso se quedan en main.py
# =====================================================================

# GET /health -> comprueba que la API está funcionando
@app.get("/health")
def health():
    return {"status": "ok"}


# GET /version -> devuelve la versión de la API
@app.get("/version")
def version():
    return {"version": "1.0.0"}


# GET /ping -> prueba rápida de conexión, responde "pong"
@app.get("/ping")
def ping():
    return {"message": "pong"}
