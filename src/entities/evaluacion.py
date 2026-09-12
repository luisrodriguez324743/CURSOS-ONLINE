from uuid import UUID, uuid4

from sqlalchemy import Float, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column

from src.database.connection import Base


class Evaluacion(Base):
    __tablename__ = "evaluacione"

    id_evaluacion: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True), primary_key=True, default=uuid4
    )
    nombre: Mapped[str] = mapped_column(String(150), default="", nullable=False)
    descripcion: Mapped[str] = mapped_column(Text, default="", nullable=False)
    calificacion: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    id_leccion: Mapped[UUID | None] = mapped_column(
        PGUUID(as_uuid=True), ForeignKey("leccion.id_leccion"), nullable=True
    )
    id_usuario: Mapped[UUID | None] = mapped_column(
        PGUUID(as_uuid=True), ForeignKey("usuario.id_usuario"), nullable=True
    )
