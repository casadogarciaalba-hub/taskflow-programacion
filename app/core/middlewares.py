# =====================================================================
# TASKFLOW API - Middlewares (app/core/middlewares.py)
#
# Práctica 1.4 -> CORS, middleware X-Process-Time y handler global
# de errores. Los sacamos de main.py para tener el código separado
# por responsabilidades (main.py solo crea la app).
# =====================================================================

# time: para medir cuánto tarda cada petición
import time

from fastapi import FastAPI, Request

# CORSMiddleware: middleware de FastAPI para configurar CORS
from fastapi.middleware.cors import CORSMiddleware

# JSONResponse: para devolver nosotros mismos una respuesta JSON
from fastapi.responses import JSONResponse


def registrar_middlewares(app: FastAPI):
    """Registra en la app el CORS, el handler de errores y X-Process-Time."""

    # =================================================================
    # 1) CORS
    # Problema que resuelve: el navegador bloquea las peticiones de un
    # frontend que está en otro origen (otro puerto). Aquí permitimos
    # SOLO el frontend de http://localhost:5173.
    # =================================================================
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173"],  # origen permitido
        allow_methods=["*"],                      # GET, POST, PUT, DELETE...
        allow_headers=["*"],                      # cualquier cabecera
    )

    # =================================================================
    # 3) HANDLER GLOBAL DE ERRORES
    # Problema que resuelve: si hay un error no controlado, el cliente
    # recibe un mensaje genérico con código 500 y NUNCA ve el stacktrace
    # (que mostraría información interna del código).
    # =================================================================
    @app.exception_handler(Exception)
    async def error_global(request: Request, exc: Exception):
        return JSONResponse(
            status_code=500,
            content={"error": "Error interno del servidor"},
        )

    # =================================================================
    # 2) MIDDLEWARE PROPIO: X-Process-Time
    # Problema que resuelve: saber cuánto tarda la API en responder.
    # Se ejecuta en TODAS las peticiones: apunta la hora, deja pasar la
    # petición al endpoint (call_next) y al volver calcula los ms.
    # =================================================================
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