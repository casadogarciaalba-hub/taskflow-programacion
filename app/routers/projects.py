# =====================================================================
# Router de PROYECTOS - app/routers/projects.py
# Práctica 1.3 -> todas las rutas de proyectos
# Práctica 1.5 -> sesión de BD con Depends(get_db)
# Práctica 1.6 -> CRUD completo contra la base de datos
# Práctica 1.7 -> POST, PUT y DELETE necesitan token (get_current_user)
# =====================================================================

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app import models
from app.schemas import ProjectCreate, ProjectRead, ProjectWithTasks

router = APIRouter(prefix="/projects", tags=["projects"])


# Busca un proyecto por id. Si no existe -> 404
def buscar_proyecto(project_id: int, db: Session):
    proyecto = db.get(models.Project, project_id)
    if proyecto is None:
        raise HTTPException(status_code=404, detail=f"El proyecto {project_id} no existe")
    return proyecto


# GET /projects -> lista de proyectos
@router.get("", response_model=list[ProjectRead])
def listar_proyectos(db: Session = Depends(get_db)):
    return db.query(models.Project).all()


# GET /projects/{id} -> detalle del proyecto CON sus tareas
# (las tareas salen gracias a la relación "tasks" del modelo)
@router.get("/{project_id}", response_model=ProjectWithTasks)
def obtener_proyecto(project_id: int, db: Session = Depends(get_db)):
    return buscar_proyecto(project_id, db)


# POST /projects -> crear un proyecto (necesita token)
@router.post("", response_model=ProjectRead, status_code=201)
def crear_proyecto(
    project: ProjectCreate,
    db: Session = Depends(get_db),
    usuario: models.User = Depends(get_current_user),  # 1.7: exige token
):
    proyecto = models.Project(**project.model_dump())
    db.add(proyecto)
    db.commit()
    db.refresh(proyecto)
    return proyecto


# PUT /projects/{id} -> editar un proyecto (necesita token)
@router.put("/{project_id}", response_model=ProjectRead)
def editar_proyecto(
    project_id: int,
    project: ProjectCreate,
    db: Session = Depends(get_db),
    usuario: models.User = Depends(get_current_user),  # 1.7: exige token
):
    proyecto = buscar_proyecto(project_id, db)
    for campo, valor in project.model_dump().items():
        setattr(proyecto, campo, valor)
    db.commit()
    db.refresh(proyecto)
    return proyecto


# DELETE /projects/{id} -> eliminar un proyecto (necesita token)
# Decisión: BORRADO EN CASCADA. Una tarea no puede existir sin proyecto
# (project_id es obligatorio), así que al borrar el proyecto se borran
# también sus tareas. Lo hace el cascade="all, delete-orphan" de models.py
@router.delete("/{project_id}")
def eliminar_proyecto(
    project_id: int,
    db: Session = Depends(get_db),
    usuario: models.User = Depends(get_current_user),  # 1.7: exige token
):
    proyecto = buscar_proyecto(project_id, db)
    num_tareas = len(proyecto.tasks)
    db.delete(proyecto)
    db.commit()
    return {"message": f"Proyecto {project_id} eliminado junto con sus {num_tareas} tareas"}
