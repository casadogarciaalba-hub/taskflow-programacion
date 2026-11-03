# =====================================================================
# Router de PROYECTOS - app/routers/projects.py
# Práctica 1.3 -> todas las rutas de proyectos viven aquí
# =====================================================================

# datetime: para poner la fecha y hora actual en created_at
from datetime import datetime

# APIRouter: un "mini FastAPI" para agrupar rutas de un mismo recurso
from fastapi import APIRouter

# Schemas de proyectos (ya estaban creados en app/schemas.py)
from app.schemas import ProjectCreate, ProjectRead

# Creamos el router de proyectos:
#   prefix="/projects" -> todas las rutas de este archivo empiezan por /projects
#   tags=["projects"]  -> en Swagger salen agrupadas bajo "projects"
router = APIRouter(prefix="/projects", tags=["projects"])


# POST /projects -> crear un proyecto (TEMPORAL, todavía sin base de datos)
@router.post("", response_model=ProjectRead, status_code=201)
def crear_proyecto(project: ProjectCreate):
    return ProjectRead(
        id=1,                         # id inventado (no hay BD todavía)
        created_at=datetime.now(),    # fecha y hora actual
        **project.model_dump(),       # copia name y description
    )