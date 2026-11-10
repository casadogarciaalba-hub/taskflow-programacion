# =====================================================================
# Router de TAREAS - app/routers/tasks.py
# Práctica 1.3 -> todas las rutas de tareas
# Práctica 1.5 -> sesión de BD con Depends(get_db)
# Práctica 1.6 -> CRUD completo contra la base de datos
# =====================================================================

from typing import Optional

# HTTPException: para devolver errores (404...)
# Query: para poner límites a los parámetros de la URL
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app import models
from app.schemas import TaskCreate, TaskUpdate, TaskRead

router = APIRouter(prefix="/tasks", tags=["tasks"])


# Busca una tarea por id. Si no existe -> 404
def buscar_tarea(task_id: int, db: Session):
    tarea = db.get(models.Task, task_id)
    if tarea is None:
        raise HTTPException(status_code=404, detail=f"La tarea {task_id} no existe")
    return tarea


# Comprueba que el proyecto (y la categoría, si viene) existen.
# Así no se pueden crear tareas que apunten a algo que no existe.
def comprobar_relaciones(datos: TaskCreate, db: Session):
    if db.get(models.Project, datos.project_id) is None:
        raise HTTPException(status_code=404, detail=f"El proyecto {datos.project_id} no existe")
    if datos.category_id is not None and db.get(models.Category, datos.category_id) is None:
        raise HTTPException(status_code=404, detail=f"La categoría {datos.category_id} no existe")


# GET /tasks -> lista de tareas
#   Filtros (opcionales): project_id y completed
#   Paginación: skip (cuántas se salta) y limit (cuántas devuelve)
@router.get("", response_model=list[TaskRead])
def listar_tareas(
    project_id: Optional[int] = None,
    completed: Optional[bool] = None,
    skip: int = Query(0, ge=0),           # no puede ser negativo
    limit: int = Query(10, ge=1, le=100), # entre 1 y 100
    db: Session = Depends(get_db),
):
    consulta = db.query(models.Task)
    if project_id is not None:
        consulta = consulta.filter(models.Task.project_id == project_id)
    if completed is not None:
        consulta = consulta.filter(models.Task.completed == completed)
    return consulta.offset(skip).limit(limit).all()


# GET /tasks/{id} -> detalle de una tarea
@router.get("/{task_id}", response_model=TaskRead)
def obtener_tarea(task_id: int, db: Session = Depends(get_db)):
    return buscar_tarea(task_id, db)


# POST /tasks -> crear una tarea (ahora SÍ se guarda en la BD)
@router.post("", response_model=TaskRead, status_code=201)
def crear_tarea(task: TaskCreate, db: Session = Depends(get_db)):
    comprobar_relaciones(task, db)
    tarea = models.Task(**task.model_dump())  # creamos el objeto con los datos
    db.add(tarea)       # lo añadimos a la sesión
    db.commit()         # lo guardamos en la BD
    db.refresh(tarea)   # recargamos para tener el id que ha puesto la BD
    return tarea


# PUT /tasks/{id} -> editar una tarea
@router.put("/{task_id}", response_model=TaskRead)
def editar_tarea(task_id: int, task: TaskUpdate, db: Session = Depends(get_db)):
    tarea = buscar_tarea(task_id, db)
    comprobar_relaciones(task, db)
    # Cambiamos cada campo por el nuevo valor
    for campo, valor in task.model_dump().items():
        setattr(tarea, campo, valor)
    db.commit()
    db.refresh(tarea)
    return tarea


# DELETE /tasks/{id} -> eliminar una tarea
@router.delete("/{task_id}")
def eliminar_tarea(task_id: int, db: Session = Depends(get_db)):
    tarea = buscar_tarea(task_id, db)
    db.delete(tarea)
    db.commit()
    return {"message": f"Tarea {task_id} eliminada"}
