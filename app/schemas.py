# =====================================================================
# TASKFLOW API - Schemas (app/schemas.py)
#
# Práctica 1.2 -> schemas de entrada (Create) y salida (Read)
# Práctica 1.6 -> schemas de categorías, TaskUpdate para editar y
#                 schemas de detalle que incluyen las tareas
# =====================================================================

from typing import Optional

# ConfigDict(from_attributes=True) -> permite que Pydantic lea los
# objetos de SQLAlchemy (los modelos) y los convierta a JSON
from pydantic import BaseModel, ConfigDict, Field


# ---------------------------- TAREAS ---------------------------------

# Datos que envía el cliente para CREAR una tarea
class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=100)  # obligatorio, 1-100 caracteres
    description: Optional[str] = None                 # opcional
    project_id: int                                   # proyecto al que pertenece
    category_id: Optional[int] = None                 # categoría (opcional)


# Datos que envía el cliente para EDITAR una tarea (PUT).
# Es lo mismo que TaskCreate + poder marcarla como completada
class TaskUpdate(TaskCreate):
    completed: bool = False


# Datos que DEVUELVE la API
class TaskRead(TaskUpdate):
    model_config = ConfigDict(from_attributes=True)
    id: int


# --------------------------- PROYECTOS -------------------------------

class ProjectCreate(BaseModel):
    name: str
    description: Optional[str] = None


class ProjectRead(ProjectCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int


# GET /projects/{id} -> el proyecto CON sus tareas
class ProjectWithTasks(ProjectRead):
    tasks: list[TaskRead] = []


# -------------------------- CATEGORÍAS -------------------------------

class CategoryCreate(BaseModel):
    name: str = Field(min_length=1, max_length=50)


class CategoryRead(CategoryCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int


# GET /categories/{id} -> la categoría CON sus tareas
class CategoryWithTasks(CategoryRead):
    tasks: list[TaskRead] = []

    