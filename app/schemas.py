# =====================================================================
# PRÁCTICA 1.2 — MODELADO CON PYDANTIC
# Archivo: app/schemas.py
#
# ¿Qué es un SCHEMA?
#   Es el CONTRATO de la API: define qué datos ENTRAN (lo que envía
#   el cliente) y qué datos SALEN (lo que devuelve la API).
#   Pydantic comprueba automáticamente que los datos cumplen ese
#   contrato. Si no lo cumplen, FastAPI devuelve un error 422.
#
# Schema vs modelo de base de datos:
#   - Schema (este archivo) -> define los datos que viajan por la API.
#   - Modelo de BD (más adelante) -> define cómo se guardan en la tabla.
#
# Por ahora NO incluimos usuarios, como indica el enunciado.
# =====================================================================

# datetime: tipo de dato para fechas y horas (lo usamos en created_at)
from datetime import datetime

# Optional: indica que un campo puede venir vacío (None)
from typing import Optional

# BaseModel: clase base de Pydantic de la que heredan todos los schemas
# Field: permite añadir restricciones a un campo (longitud mínima, máxima...)
from pydantic import BaseModel, Field


# =====================================================================
# ---------------------------- TAREAS ---------------------------------
# =====================================================================

# TaskCreate -> schema de ENTRADA
# Son los datos que el cliente envía al crear una tarea (POST /tasks)
class TaskCreate(BaseModel):
    """Datos que envía el cliente para crear una tarea (ENTRADA)."""

    # title: texto obligatorio.
    # Field(min_length=1) -> no puede estar vacío ("" da error 422)
    # Field(max_length=100) -> máximo 100 caracteres
    title: str = Field(min_length=1, max_length=100)

    # description: texto OPCIONAL.
    # Si el cliente no la envía, vale None (vacío)
    description: Optional[str] = None

    # project_id: número entero obligatorio.
    # Indica a qué proyecto pertenece la tarea
    project_id: int


# TaskRead -> schema de SALIDA
# Son los datos que la API devuelve al cliente.
# Hereda de TaskCreate, así que ya tiene title, description y project_id,
# y además añade los campos que genera el servidor (no los envía el cliente)
class TaskRead(TaskCreate):
    """Datos que devuelve la API (SALIDA)."""

    # id: identificador único de la tarea (lo genera el servidor)
    id: int

    # completed: si la tarea está hecha o no.
    # Por defecto False (una tarea nueva no está completada)
    completed: bool = False

    # created_at: fecha y hora en que se creó la tarea
    created_at: datetime


# =====================================================================
# --------------------------- PROYECTOS -------------------------------
# =====================================================================

# ProjectCreate -> schema de ENTRADA
# Son los datos que el cliente envía al crear un proyecto
class ProjectCreate(BaseModel):
    """Datos que envía el cliente para crear un proyecto (ENTRADA)."""

    # name: nombre del proyecto, texto obligatorio
    name: str

    # description: descripción del proyecto, texto OPCIONAL
    description: Optional[str] = None


# ProjectRead -> schema de SALIDA
# Hereda de ProjectCreate (name y description)
# y añade los campos que genera el servidor
class ProjectRead(ProjectCreate):
    """Datos que devuelve la API (SALIDA)."""

    # id: identificador único del proyecto
    id: int

    # created_at: fecha y hora de creación del proyecto
    created_at: datetime