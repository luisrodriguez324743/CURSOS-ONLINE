import uuid
from datetime import datetime
from sqlalchemy import DateTime, Float, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column
from src.database.connection import Base

class Progreso(Base):
    __tablename__ = "progreso"

    id_progreso: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    porcentaje: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    estado: Mapped[str] = mapped_column(String(50), default="En progreso", nullable=False)
    ultima_actualizacion: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False)
    id_usuario: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("usuario.id_usuario"), nullable=True)
    id_curso: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("curso.id_curso"), nullable=True)
    id_leccion: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("leccion.id_leccion"), nullable=True)