# =====================================================================
# Router de PROYECTOS - app/routers/projects.py
# Práctica 1.3 -> todas las rutas de proyectos
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

# Schemas de proyectos (ya estaban creados en schemas.py)
from app.schemas import ProjectCreate, ProjectRead

# Creamos el router de proyectos:
#   prefix="/projects" -> todas las rutas de este archivo empiezan por /projects
#   tags=["projects"]  -> en Swagger salen agrupadas en "projects"
router = APIRouter(prefix="/projects", tags=["projects"])


# POST /projects -> crear un proyecto (TEMPORAL, todavía no guarda en BD)
# db: Session = Depends(get_db) -> FastAPI le pasa una sesión de BD
@router.post("", response_model=ProjectRead, status_code=201)
def crear_proyecto(project: ProjectCreate, db: Session = Depends(get_db)):
    return ProjectRead(
        id=1,                          # id inventado (todavía sin BD)
        created_at=datetime.now(),     # fecha y hora actual
        **project.model_dump(),        # copiamos los datos que envía el cliente
    )