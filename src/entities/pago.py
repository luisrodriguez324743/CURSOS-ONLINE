from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import DateTime, Float, String
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column

from src.database.connection import Base


class Pago(Base):
    __tablename__ = "pago"

    id_pago: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True), primary_key=True, default=uuid4
    )
    monto: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    fecha_pago: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, nullable=False
    )
    metodo_pago: Mapped[str] = mapped_column(String(50), default="efectivo")
    estado: Mapped[str] = mapped_column(String(20), default="pagado")
    id_usuario: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), nullable=True)
    id_curso: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), nullable=True)
    id_factura: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), nullable=True)
