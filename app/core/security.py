# =====================================================================
# TASKFLOW API - Seguridad (app/core/security.py)
#
# Práctica 1.7 -> autenticación con JWT:
#   - hashear y comprobar contraseñas con passlib[bcrypt]
#   - crear el token JWT con python-jose (sub + exp)
#   - dependencia get_current_user con OAuth2PasswordBearer
# =====================================================================

from datetime import datetime, timedelta, timezone

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.core.database import get_db
from app import models


# ---------------------------------------------------------------------
# CONFIGURACIÓN DEL TOKEN
# ---------------------------------------------------------------------
# SECRET_KEY: clave con la que se FIRMA el token. Si alguien la
# conociera podría fabricar tokens falsos.
SECRET_KEY = "clave-secreta-taskflow"

# Algoritmo de firma: HS256
ALGORITHM = "HS256"

# El token caduca a los 30 minutos
ACCESS_TOKEN_EXPIRE_MINUTES = 30



# ---------------------------------------------------------------------
# CONTRASEÑAS (passlib + bcrypt)
# ---------------------------------------------------------------------
# bcrypt mete un salt aleatorio distinto en cada hash, así que dos
# usuarios con la misma contraseña tienen hashes diferentes
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Convierte la contraseña en un hash (lo que se guarda en la BD)
def hashear_password(password: str) -> str:
    return pwd_context.hash(password)


# Comprueba si la contraseña coincide con el hash guardado
def verificar_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)


# ---------------------------------------------------------------------
# TOKEN JWT (python-jose)
# ---------------------------------------------------------------------
# Crea un token firmado con:
#   sub -> el usuario al que pertenece el token
#   exp -> cuándo caduca (ahora + 30 minutos)
def crear_token(username: str) -> str:
    expira = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    datos = {"sub": username, "exp": expira}
    return jwt.encode(datos, SECRET_KEY, algorithm=ALGORITHM)


# ---------------------------------------------------------------------
# get_current_user
# ---------------------------------------------------------------------
# OAuth2PasswordBearer lee la cabecera "Authorization: Bearer <token>".
# tokenUrl es la ruta del login (Swagger la usa en el botón Authorize).
# Si no viene token, devuelve él solo un 401.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


# Devuelve el usuario dueño del token. Si el token no vale -> 401
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    error_401 = HTTPException(status_code=401, detail="Token no válido o caducado")

    try:
        # jwt.decode comprueba la FIRMA y la CADUCIDAD (exp).
        # Si el token está mal o ha caducado lanza JWTError
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
    except JWTError:
        raise error_401

    # Buscamos el usuario del token en la base de datos
    usuario = db.query(models.User).filter(models.User.username == username).first()
    if usuario is None:
        raise error_401
    return usuario
