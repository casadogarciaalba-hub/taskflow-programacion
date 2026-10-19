# =====================================================================
# TASKFLOW API — Archivo principal
# Archivo: app/main.py
#
# Práctica 1.1 -> endpoints /health, /version y /ping
# Práctica 1.2 -> endpoint temporal POST /tasks usando los schemas
# =====================================================================

# FastAPI: framework con el que creamos la API
from fastapi import FastAPI

# datetime: para poner la fecha y hora actual en created_at (Práctica 1.2)
from datetime import datetime

# Importamos los schemas de tareas que hemos definido en app/schemas.py
#   TaskCreate -> lo que ENTRA (lo que envía el cliente)
#   TaskRead   -> lo que SALE (lo que devuelve la API)
from app.schemas import TaskCreate, TaskRead

# Creamos la aplicación. "app" es lo que arranca uvicorn (app.main:app)
app = FastAPI()


# =====================================================================
# ------------------------- PRÁCTICA 1.1 ------------------------------
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


# =====================================================================
# ------------------------- PRÁCTICA 1.2 ------------------------------
# =====================================================================

# POST /tasks -> endpoint TEMPORAL para crear una tarea.
#
# - task: TaskCreate -> FastAPI recibe el JSON del cliente y Pydantic
#   lo valida con el schema TaskCreate. Si el título está vacío o
#   supera 100 caracteres, devuelve automáticamente un error 422
#   indicando qué campo falla y por qué.
#
# - response_model=TaskRead -> la respuesta sigue el schema TaskRead
#   (contrato de salida de la API).
#
# - status_code=201 -> código HTTP 201 "Created" (recurso creado).
#
# Todavía NO hay base de datos, así que no se guarda nada:
# devolvemos una tarea SIMULADA.
@app.post("/tasks", response_model=TaskRead, status_code=201)
def crear_tarea(task: TaskCreate):
    return TaskRead(
        id=1,                     # id inventado (no hay BD todavía)
        completed=False,          # una tarea nueva no está completada
        created_at=datetime.now(),  # fecha y hora actual
        **task.model_dump(),      # copia title, description y project_id
                                  # de lo que envió el cliente
    )

