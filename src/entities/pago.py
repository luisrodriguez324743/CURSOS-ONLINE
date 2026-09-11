from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import DateTime, Float, String
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column

from src.database.connection import Base


class Pago(Base):
    __tablename__ = "pagos"

    id_pago: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True), primary_key=True, default=uuid4
    )
    monto: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    fecha_pago: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, nullable=False
    )
    metodo_pago: Mapped[str] = mapped_column(String(50), default="efectivo")
    estado: Mapped[str] = mapped_column(String(20), default="pagado")
    id_usuario: Mapped[UUID | None] = mapped_column(PGUUID(as_uuid=True), nullable=True)
    id_curso: Mapped[UUID | None] = mapped_column(PGUUID(as_uuid=True), nullable=True)
    id_factura: Mapped[UUID | None] = mapped_column(PGUUID(as_uuid=True), nullable=True)

    def __init__(
        self,
        monto: float = 0.0,
        fecha_pago: datetime | None = None,
        metodo_pago: str = "",
        estado: str = "pagado",
        id_usuario: UUID | None = None,
        id_curso: UUID | None = None,
        id_factura: UUID | None = None,
        **kwargs,
    ) -> None:
        if monto < 0:
            raise ValueError("El monto del pago no puede ser negativo.")
        if not metodo_pago.strip():
            metodo_pago = "efectivo"
        if estado not in {"pendiente", "pagado", "cancelado"}:
            raise ValueError("Estado de pago no válido.")

        super().__init__(**kwargs)
        self.monto = monto
        self.fecha_pago = fecha_pago or datetime.now()
        self.metodo_pago = metodo_pago
        self.estado = estado
        self.id_usuario = id_usuario
        self.id_curso = id_curso
        self.id_factura = id_factura

    @staticmethod
    def validar_tarjeta(numero_tarjeta: str) -> bool:
        tarjeta = numero_tarjeta.replace(" ", "")
        return tarjeta.isdigit() and 13 <= len(tarjeta) <= 19

    @staticmethod
    def validar_pago(
        metodo_pago: str, referencia: str | None = None
    ) -> tuple[bool, str]:
        metodo = metodo_pago.lower().strip()
        if metodo == "tarjeta":
            if referencia is None or not Pago.validar_tarjeta(referencia):
                return (
                    False,
                    "La tarjeta no es válida. Debe tener entre 13 y 19 dígitos.",
                )
            return True, "Pago con tarjeta validado."
        if metodo in {"transferencia", "efectivo"}:
            return True, f"Pago por {metodo} registrado correctamente."
        return False, "Método de pago no válido."

    @classmethod
    def crear_pago(
        cls,
        monto: float,
        metodo_pago: str,
        id_usuario: UUID | None,
        id_curso: UUID | None,
        id_factura: UUID | None = None,
    ) -> "Pago":
        return cls(
            monto=monto,
            metodo_pago=metodo_pago,
            estado="pagado",
            id_usuario=id_usuario,
            id_curso=id_curso,
            id_factura=id_factura,
        )

    def to_dict(self) -> dict[str, object]:
        return {
            "id_pago": str(self.id_pago),
            "monto": self.monto,
            "fecha_pago": self.fecha_pago.isoformat(),
            "metodo_pago": self.metodo_pago,
            "estado": self.estado,
            "id_usuario": str(self.id_usuario) if self.id_usuario else None,
            "id_curso": str(self.id_curso) if self.id_curso else None,
            "id_factura": str(self.id_factura) if self.id_factura else None,
        }

    def resumen(self) -> str:
        return (
            f"Pago #{self.id_pago.hex[:8].upper()} | Monto: ${self.monto:.2f} | "
            f"Método: {self.metodo_pago} | Estado: {self.estado}"
        )

    def __str__(self) -> str:
        return (
            f"Pago(id={self.id_pago}, monto={self.monto}, metodo={self.metodo_pago}, "
            f"estado={self.estado})"
        )
