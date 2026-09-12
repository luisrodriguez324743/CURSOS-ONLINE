import uuid
from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column
from src.database.connection import Base

class Inscripcion(Base):
    __tablename__ = "inscripcion"

    id_inscripcion: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    fecha_inscripcion: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False)
    estado: Mapped[str] = mapped_column(String(50), default="activa", nullable=False)
    id_usuario: Mapped[uuid.UUID] = mapped_column(ForeignKey("usuario.id_usuario"), nullable=False)
    id_curso: Mapped[uuid.UUID] = mapped_column(ForeignKey("curso.id_curso"), nullable=False)