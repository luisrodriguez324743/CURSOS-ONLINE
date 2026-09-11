import uuid
from datetime import datetime, date
from sqlalchemy import String, Text, Integer, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database.connection import Base
class Rol(Base):
    __tablename__ = "rol"

    id_rol: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    nombre_rol: Mapped[str] = mapped_column(String(50), unique=True)
    descripcion: Mapped[str | None] = mapped_column(String(255), default=None, nullable=True)

    # Relación uno a muchos con Usuario (opcional pero recomendada en SQLAlchemy)
    usuarios: Mapped[list["Usuario"]] = relationship(back_populates="rol")