from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import DateTime, Float, String
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column

from src.database.connection import Base


class Progreso(Base):
    __tablename__ = "progresos"

    id_progreso: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True), primary_key=True, default=uuid4
    )
    porcentaje: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    estado: Mapped[str] = mapped_column(
        String(30), default="En progreso", nullable=False
    )
    ultima_actualizacion: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, onupdate=datetime.now, nullable=False
    )
    id_usuario: Mapped[UUID | None] = mapped_column(PGUUID(as_uuid=True), nullable=True)
    id_curso: Mapped[UUID | None] = mapped_column(PGUUID(as_uuid=True), nullable=True)
    id_leccion: Mapped[UUID | None] = mapped_column(PGUUID(as_uuid=True), nullable=True)
