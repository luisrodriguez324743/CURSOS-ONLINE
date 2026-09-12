import uuid
from sqlalchemy import Float, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from src.database.connection import Base

class Evaluacion(Base):
    __tablename__ = "evaluacion"

    id_evaluacion: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    nombre: Mapped[str] = mapped_column(String(150), default="", nullable=False)
    descripcion: Mapped[str] = mapped_column(Text, default="", nullable=False)
    calificacion: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    id_leccion: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("leccion.id_leccion"), nullable=True)
    id_usuario: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("usuario.id_usuario"), nullable=True)