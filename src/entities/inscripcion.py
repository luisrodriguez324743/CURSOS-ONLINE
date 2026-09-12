import uuid
from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column
from src.database.connection import Base

from sqlalchemy import DateTime, String
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column

from src.database.connection import Base


class Inscripcion(Base):
    __tablename__ = "inscripciones"

    id_inscripcion: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True), primary_key=True, default=uuid4
    )
    fecha_inscripcion: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, nullable=False
    )
    estado: Mapped[str] = mapped_column(String(20), default="activa", nullable=False)
    id_usuario: Mapped[UUID | None] = mapped_column(PGUUID(as_uuid=True), nullable=True)
    id_curso: Mapped[UUID | None] = mapped_column(PGUUID(as_uuid=True), nullable=True)
