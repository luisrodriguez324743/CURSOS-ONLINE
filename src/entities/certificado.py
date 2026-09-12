from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column

from src.database.connection import Base


class Certificado(Base):
    __tablename__ = "certificados"

    id_certificado: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True), primary_key=True, default=uuid4
    )
    fecha_emision: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, nullable=False
    )
    codigo: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    id_usuario: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True), ForeignKey("usuario.id_usuario"), nullable=True
    )
    id_curso: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True), ForeignKey("curso.id_curso"), nullable=True
    )
