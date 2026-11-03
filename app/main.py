# =====================================================================
# TASKFLOW API - Archivo principal (app/main.py)
#
# Práctica 1.1 -> endpoints /health, /version y /ping
# Práctica 1.3 -> main.py solo crea la app e incluye los routers
# Práctica 1.4 -> middlewares (CORS y X-Process-Time) y handler global
#                 de errores
# =====================================================================

# time: para medir cuánto tarda cada petición
import time

from fastapi import FastAPI, Request

# CORSMiddleware: middleware de FastAPI para configurar CORS
from fastapi.middleware.cors import CORSMiddleware

# JSONResponse: para devolver nosotros mismos una respuesta JSON
from fastapi.responses import JSONResponse

from app.routers import tasks, projects

app = FastAPI()

# Registramos los routers (Práctica 1.3)
app.include_router(tasks.router)
app.include_router(projects.router)


# =====================================================================
# 1) CORS
# Problema que resuelve: el navegador bloquea las peticiones de un
# frontend que está en otro origen (otro puerto). Aquí permitimos
# SOLO el frontend de http://localhost:5173.
# =====================================================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # origen permitido
    allow_methods=["*"],                      # GET, POST, PUT, DELETE...
    allow_headers=["*"],                      # cualquier cabecera
)


# =====================================================================
# 3) HANDLER GLOBAL DE ERRORES
# Problema que resuelve: si hay un error no controlado, el cliente
# recibe un mensaje genérico con código 500 y NUNCA ve el stacktrace
# (que mostraría información interna del código).
# =====================================================================
@app.exception_handler(Exception)
async def error_global(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"error": "Error interno del servidor"},
    )


# =====================================================================
# 2) MIDDLEWARE PROPIO: X-Process-Time
# Problema que resuelve: saber cuánto tarda la API en responder.
# Se ejecuta en TODAS las peticiones: apunta la hora, deja pasar la
# petición al endpoint (call_next) y al volver calcula los ms.
# =====================================================================
@app.middleware("http")
async def tiempo_respuesta(request: Request, call_next):
    inicio = time.perf_counter()  # hora de inicio

    try:
        # Pasamos la petición al endpoint y esperamos la respuesta
        response = await call_next(request)
    except Exception as exc:
        # Si el endpoint falla, usamos el handler global de errores
        # para que la respuesta 500 también lleve X-Process-Time
        response = await error_global(request, exc)

    # Tiempo que ha tardado, en milisegundos
    ms = (time.perf_counter() - inicio) * 1000

    # Añadimos la cabecera a la respuesta
    response.headers["X-Process-Time"] = f"{ms:.2f}"
    return response


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