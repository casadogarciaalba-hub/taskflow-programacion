# =====================================================================
# Router de TAREAS - app/routers/tasks.py
# Práctica 1.3 -> todas las rutas de tareas viven aquí
# =====================================================================

# datetime: para poner la fecha y hora actual en created_at
from datetime import datetime

# APIRouter: un "mini FastAPI" para agrupar rutas de un mismo recurso
from fastapi import APIRouter

# Schemas de tareas (los mismos de la Práctica 1.2)
from app.schemas import TaskCreate, TaskRead

# Creamos el router de tareas:
#   prefix="/tasks" -> todas las rutas de este archivo empiezan por /tasks
#   tags=["tasks"]  -> en Swagger salen agrupadas bajo "tasks"
router = APIRouter(prefix="/tasks", tags=["tasks"])


# POST /tasks -> crear una tarea (TEMPORAL, todavía sin base de datos)
# Este endpoint estaba antes en main.py y lo hemos MOVIDO aquí.
# Como el router ya tiene prefix="/tasks", aquí la ruta va vacía ("")
@router.post("", response_model=TaskRead, status_code=201)
def crear_tarea(task: TaskCreate):
    return TaskRead(
        id=1,                       # id inventado (no hay BD todavía)
        completed=False,            # una tarea nueva no está completada
        created_at=datetime.now(),  # fecha y hora actual
        **task.model_dump(),        # copia title, description y project_id
    )
