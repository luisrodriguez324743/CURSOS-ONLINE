from datetime import datetime
from typing import Any
from uuid import UUID, uuid4

from sqlalchemy import DateTime, Float, String
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
    id_inscripcion: Mapped[UUID | None] = mapped_column(
        PGUUID(as_uuid=True), nullable=True
    )
    id_usuario: Mapped[UUID | None] = mapped_column(PGUUID(as_uuid=True), nullable=True)
    id_curso: Mapped[UUID | None] = mapped_column(PGUUID(as_uuid=True), nullable=True)
    detalle_cursos: Mapped[str] = mapped_column(String, nullable=True, default="[]")
    metodo_pago: Mapped[str] = mapped_column(String(50), default="efectivo")
    estado: Mapped[str] = mapped_column(String(20), default="emitida")

    def __init__(
        self,
        total: float = 0.0,
        numero_factura: str | None = None,
        fecha_emision: datetime | None = None,
        id_inscripcion: UUID | None = None,
        id_usuario: UUID | None = None,
        id_curso: UUID | None = None,
        detalle_cursos: list[dict[str, Any]] | None = None,
        metodo_pago: str = "efectivo",
        estado: str = "emitida",
        **kwargs,
    ) -> None:
        if total < 0:
            raise ValueError("El total de la factura no puede ser negativo.")
        if not numero_factura:
            numero_factura = f"FAC-{uuid4().hex[:8].upper()}"
        if not metodo_pago.strip():
            metodo_pago = "efectivo"
        if estado not in {"emitida", "pagada", "anulada"}:
            raise ValueError("Estado de factura no válido.")

        super().__init__(**kwargs)
        self.numero_factura = numero_factura
        self.fecha_emision = fecha_emision or datetime.now()
        self.total = total
        self.id_inscripcion = id_inscripcion
        self.id_usuario = id_usuario
        self.id_curso = id_curso
        self.detalle_cursos = str(detalle_cursos or [])
        self.metodo_pago = metodo_pago
        self.estado = estado

    @classmethod
    def crear_factura(
        cls,
        total: float,
        id_usuario: UUID | None,
        id_curso: UUID | None,
        id_inscripcion: UUID | None = None,
        metodo_pago: str = "efectivo",
    ) -> "Factura":
        return cls(
            total=total,
            id_inscripcion=id_inscripcion,
            id_usuario=id_usuario,
            id_curso=id_curso,
            metodo_pago=metodo_pago,
            detalle_cursos=[
                {
                    "id_curso": str(id_curso),
                    "descripcion": "Compra de curso",
                    "total": total,
                }
            ],
        )

    def generar_comprobante(self, nombre_curso: str, nombre_usuario: str) -> str:
        return (
            "\n========================================\n"
            f"        COMPROBANTE DE PAGO\n"
            "========================================\n"
            f"Factura: {self.numero_factura}\n"
            f"Fecha: {self.fecha_emision.strftime('%d/%m/%Y %H:%M')}\n"
            f"Cliente: {nombre_usuario}\n"
            f"Curso: {nombre_curso}\n"
            f"Método de pago: {self.metodo_pago}\n"
            f"Total: ${self.total:.2f}\n"
            f"Estado: {self.estado}\n"
            "========================================\n"
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "id_factura": str(self.id_factura),
            "numero_factura": self.numero_factura,
            "fecha_emision": self.fecha_emision.isoformat(),
            "total": self.total,
            "id_inscripcion": str(self.id_inscripcion) if self.id_inscripcion else None,
            "id_usuario": str(self.id_usuario) if self.id_usuario else None,
            "id_curso": str(self.id_curso) if self.id_curso else None,
            "detalle_cursos": self.detalle_cursos,
            "metodo_pago": self.metodo_pago,
            "estado": self.estado,
        }

    def __str__(self) -> str:
        return (
            f"Factura({self.numero_factura}, total={self.total}, metodo={self.metodo_pago}, "
            f"estado={self.estado})"
        )
