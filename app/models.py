# =====================================================================
# TASKFLOW API - Modelos de la base de datos (app/models.py)
#
# Práctica 1.5 -> modelos Task, Project, User y Category con SQLAlchemy.
# Cada clase es una tabla y cada atributo es una columna (ORM).
# Todos los usuarios pueden acceder a todos los proyectos, por eso
# Project no tiene un usuario dueño.
# =====================================================================

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from app.core.database import Base


# Tabla users
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

    # Relación 1-N: un usuario tiene muchas tareas asignadas
    tasks = relationship("Task", back_populates="user")


# Tabla projects
class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String)

    # Relación 1-N: un proyecto tiene muchas tareas.
    # cascade -> si se borra el proyecto, se borran también sus tareas
    tasks = relationship("Task", back_populates="project",
                         cascade="all, delete-orphan")


# Tabla categories
class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

    # Relación 1-N: una categoría tiene muchas tareas
    tasks = relationship("Task", back_populates="category")


# Tabla tasks
class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String)
    completed = Column(Boolean, default=False)

    # Claves foráneas (FK): a qué proyecto, categoría y usuario pertenece
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"))
    user_id = Column(Integer, ForeignKey("users.id"))

    # Relaciones inversas (back_populates conecta con el otro lado)
    project = relationship("Project", back_populates="tasks")
    category = relationship("Category", back_populates="tasks")
    user = relationship("User", back_populates="tasks")