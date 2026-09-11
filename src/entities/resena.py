import uuid
from datetime import date
from sqlalchemy import Text, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database.connection import Base


class Resena(Base):
    __tablename__ = "resena"

    id_resena: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    calificacion: Mapped[int] = mapped_column(Integer)
    comentario: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Claves Foráneas
    id_usuario: Mapped[uuid.UUID] = mapped_column(ForeignKey("usuario.id_usuario"))
    id_curso: Mapped[uuid.UUID] = mapped_column(ForeignKey("curso.id_curso"))

    # Auditoría
    fecha_creacion: Mapped[date] = mapped_column(default=date.today)
    fecha_edicion: Mapped[date | None] = mapped_column(nullable=True)

    # Relaciones ORM
    usuario: Mapped["Usuario"] = relationship(back_populates="resenas")
    curso: Mapped["Curso"] = relationship()