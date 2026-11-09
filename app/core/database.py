# =====================================================================
# TASKFLOW API - Conexión a la base de datos (app/core/database.py)
#
# Práctica 1.5 -> engine (SQLite), SessionLocal y dependencia get_db()
# =====================================================================

import os

# Los ordenadores del instituto bloquean las extensiones compiladas
# (.pyd) de SQLAlchemy, así que le decimos que use su versión en
# Python puro. Tiene que ir ANTES de importar sqlalchemy.
os.environ["DISABLE_SQLALCHEMY_CEXT_RUNTIME"] = "1"

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# URL de la base de datos: un fichero SQLite llamado taskflow.db
DATABASE_URL = "sqlite:///./taskflow.db"

# engine: la conexión con la base de datos.
# check_same_thread=False -> SQLite por defecto solo deja usar la
# conexión en el hilo que la creó, pero FastAPI atiende las peticiones
# en varios hilos, así que hay que desactivarlo.
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)

# SessionLocal: "fábrica" de sesiones. Cada petición pide una sesión nueva.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base: clase de la que heredan todos los modelos (tablas)
Base = declarative_base()


# get_db(): dependencia que da una sesión por petición.
# Con yield le pasamos la sesión al endpoint, y el finally se asegura
# de que la sesión se cierra SIEMPRE, aunque haya un error.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()