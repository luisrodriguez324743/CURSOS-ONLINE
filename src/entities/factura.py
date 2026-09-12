from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import DateTime, Float, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column

from src.database.connection import Base


class Factura(Base):
    __tablename__ = "facturas"

    id_factura: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True), primary_key=True, default=uuid4
    )
    numero_factura: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    fecha_emision: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, nullable=False
    )
    total: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    id_inscripcion: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True), ForeignKey("inscripciones.id_inscripcion"), nullable=True
    )
    id_usuario: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True), ForeignKey("usuario.id_usuario"), nullable=True
    )
    id_curso: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True), ForeignKey("curso.id_curso"), nullable=True
    )
    detalle_cursos: Mapped[str] = mapped_column(String, nullable=True, default="[]")
    metodo_pago: Mapped[str] = mapped_column(String(50), default="efectivo")
    estado: Mapped[str] = mapped_column(String(20), default="emitida")
