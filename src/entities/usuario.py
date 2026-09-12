import uuid
from datetime import datetime, date
from typing import TYPE_CHECKING

from sqlalchemy import String, Text, Integer, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database.connection import Base

if TYPE_CHECKING:
    from .resena import Resena
    from .rol import Rol


class Usuario(Base):
    __tablename__ = "usuario"

    id_usuario: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    primer_nombre: Mapped[str] = mapped_column(String(80))
    segundo_nombre: Mapped[str | None] = mapped_column(
        String(80), default="", nullable=True
    )
    primer_apellido: Mapped[str] = mapped_column(String(80))
    segundo_apellido: Mapped[str | None] = mapped_column(
        String(80), default="", nullable=True
    )
    nombre_usuario: Mapped[str] = mapped_column(String(80), unique=True)
    correo: Mapped[str] = mapped_column(String(120), unique=True)
    clave: Mapped[str] = mapped_column(String(255))
    area: Mapped[str | None] = mapped_column(String(100), default="", nullable=True)
    activo: Mapped[bool] = mapped_column(Boolean, default=True)

    # Clave Foránea hacia la tabla 'rol'
    id_rol: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("rol.id_rol"), nullable=True
    )

    # Auditoría (siguiendo el ejemplo del profesor)
    fecha_creacion: Mapped[date] = mapped_column(default=date.today)
    fecha_edicion: Mapped[date | None] = mapped_column(nullable=True)

    # Relaciones ORM
    rol: Mapped["Rol | None"] = relationship(back_populates="usuarios")
    resenas: Mapped[list["Resena"]] = relationship(back_populates="usuario")
