# =====================================================================
# Router de CATEGORÍAS - app/routers/categories.py
# Práctica 1.6 -> CRUD completo de categorías
# =====================================================================

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app import models
from app.schemas import CategoryCreate, CategoryRead, CategoryWithTasks

router = APIRouter(prefix="/categories", tags=["categories"])


# Busca una categoría por id. Si no existe -> 404
def buscar_categoria(category_id: int, db: Session):
    categoria = db.get(models.Category, category_id)
    if categoria is None:
        raise HTTPException(status_code=404, detail=f"La categoría {category_id} no existe")
    return categoria


# El nombre de la categoría es único (unique=True en models.py).
# Lo comprobamos antes para dar un error claro en vez de un error 500.
def comprobar_nombre(nombre: str, db: Session, category_id: int = None):
    existe = db.query(models.Category).filter(models.Category.name == nombre).first()
    if existe and existe.id != category_id:
        raise HTTPException(status_code=409, detail=f"Ya existe una categoría llamada '{nombre}'")


# GET /categories -> lista de categorías
@router.get("", response_model=list[CategoryRead])
def listar_categorias(db: Session = Depends(get_db)):
    return db.query(models.Category).all()


# GET /categories/{id} -> detalle de la categoría CON sus tareas
@router.get("/{category_id}", response_model=CategoryWithTasks)
def obtener_categoria(category_id: int, db: Session = Depends(get_db)):
    return buscar_categoria(category_id, db)


# POST /categories -> crear una categoría
@router.post("", response_model=CategoryRead, status_code=201)
def crear_categoria(category: CategoryCreate, db: Session = Depends(get_db)):
    comprobar_nombre(category.name, db)
    categoria = models.Category(**category.model_dump())
    db.add(categoria)
    db.commit()
    db.refresh(categoria)
    return categoria


# PUT /categories/{id} -> editar una categoría
@router.put("/{category_id}", response_model=CategoryRead)
def editar_categoria(category_id: int, category: CategoryCreate, db: Session = Depends(get_db)):
    categoria = buscar_categoria(category_id, db)
    comprobar_nombre(category.name, db, category_id)
    categoria.name = category.name
    db.commit()
    db.refresh(categoria)
    return categoria


# DELETE /categories/{id} -> eliminar una categoría
# Decisión: BLOQUEO. La categoría es solo una etiqueta; si la borráramos
# en cascada perderíamos tareas que siguen siendo válidas. Por eso, si
# tiene tareas, no se deja borrar y se devuelve 409 con un mensaje claro.
@router.delete("/{category_id}")
def eliminar_categoria(category_id: int, db: Session = Depends(get_db)):
    categoria = buscar_categoria(category_id, db)
    if categoria.tasks:
        raise HTTPException(
            status_code=409,
            detail=f"No se puede eliminar la categoría {category_id}: tiene "
                   f"{len(categoria.tasks)} tareas. Cámbialas de categoría o bórralas primero",
        )
    db.delete(categoria)
    db.commit()
    return {"message": f"Categoría {category_id} eliminada"}
