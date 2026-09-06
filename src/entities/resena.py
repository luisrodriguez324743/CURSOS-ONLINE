import uuid
from datetime import datetime, date
from sqlalchemy import String, Text, Integer, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.connection import Base

class Resena(Base):
    __tablename__ = "resena"

    id_resena: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    calificacion: Mapped[int] = mapped_column(Integer)  # Ej: 1 a 5
    comentario: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Clave foránea al Usuario que escribe la reseña
    id_usuario: Mapped[uuid.UUID] = mapped_column(ForeignKey("usuario.id_usuario"))

    # Clave foránea al Curso que recibe la reseña (Entidad de tus compañeros)
   # id_curso: Mapped[uuid.UUID] = mapped_column(ForeignKey("curso.id_curso"))

    # Auditoría
    fecha_creacion: Mapped[date] = mapped_column(default=date.today)
    fecha_edicion: Mapped[date | None] = mapped_column(nullable=True)

    # Relación con Usuario
    usuario: Mapped["Usuario"] = relationship(back_populates="resenas")