# =====================================================================
# Router de AUTENTICACIÓN - app/routers/auth.py
# Práctica 1.7 -> registro y login con JWT
# =====================================================================

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import hashear_password, verificar_password, crear_token
from app import models
from app.schemas import UserCreate, UserRead, Token

router = APIRouter(prefix="/auth", tags=["auth"])


# POST /auth/register -> crear un usuario nuevo
# La contraseña se guarda HASHEADA, nunca en texto plano
@router.post("/register", response_model=UserRead, status_code=201)
def registrar(datos: UserCreate, db: Session = Depends(get_db)):
    # username y email son únicos: si ya existen -> 409
    existe = db.query(models.User).filter(
        (models.User.username == datos.username) | (models.User.email == datos.email)
    ).first()
    if existe:
        raise HTTPException(status_code=409, detail="El usuario o el email ya existen")

    usuario = models.User(
        username=datos.username,
        email=datos.email,
        hashed_password=hashear_password(datos.password),
    )
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    # response_model=UserRead -> la respuesta NO lleva la contraseña
    return usuario


# POST /auth/login -> comprobar credenciales y devolver el JWT
# OAuth2PasswordRequestForm: el usuario y la contraseña llegan como
# formulario, que es lo que usa el botón Authorize de Swagger
@router.post("/login", response_model=Token)
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    usuario = db.query(models.User).filter(models.User.username == form.username).first()

    # Mismo mensaje si el usuario no existe o la contraseña está mal
    if usuario is None or not verificar_password(form.password, usuario.hashed_password):
        raise HTTPException(status_code=401, detail="Usuario o contraseña incorrectos")

    return {"access_token": crear_token(usuario.username), "token_type": "bearer"}
