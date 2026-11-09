# =====================================================================
# Router de TAREAS - app/routers/tasks.py
# Práctica 1.3 -> todas las rutas de tareas
# Práctica 1.5 -> los endpoints reciben la sesión de BD con Depends(get_db)
# =====================================================================

# datetime: para poner la fecha y hora actual
from datetime import datetime

# APIRouter: un "mini FastAPI" para agrupar rutas
# Depends: para inyectar dependencias (la sesión de la base de datos)
from fastapi import APIRouter, Depends

# Session: tipo de la sesión de SQLAlchemy
from sqlalchemy.orm import Session

# get_db: dependencia que da una sesión por petición (Práctica 1.5)
from app.core.database import get_db

# Schemas de tareas (los mismos de la Práctica 1.1)
from app.schemas import TaskCreate, TaskRead

# Creamos el router de tareas:
#   prefix="/tasks" -> todas las rutas de este archivo empiezan por /tasks
#   tags=["tasks"]  -> en Swagger salen agrupadas en "tasks"
router = APIRouter(prefix="/tasks", tags=["tasks"])


# POST /tasks -> crear una tarea (TEMPORAL, todavía no guarda en BD)
# Este endpoint estaba antes en main.py y lo movimos aquí en la 1.3.
# Como el router ya tiene prefix="/tasks", la ruta es "".
# db: Session = Depends(get_db) -> FastAPI le pasa una sesión de BD
@router.post("", response_model=TaskRead, status_code=201)
def crear_tarea(task: TaskCreate, db: Session = Depends(get_db)):
    return TaskRead(
        id=1,                         # id inventado (todavía sin BD)
        completed=False,              # una tarea nueva empieza sin completar
        created_at=datetime.now(),    # fecha y hora actual
        **task.model_dump(),          # copiamos los datos que envía el cliente
    )