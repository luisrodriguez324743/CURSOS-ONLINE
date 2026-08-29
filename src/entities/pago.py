from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4


@dataclass
class Pago:
    id_pago: UUID = field(default_factory=uuid4)
    monto: float = 0.0
    fecha_pago: datetime = field(default_factory=datetime.now)
    metodo_pago: str = ""
    estado: str = "pagado"
    id_usuario: UUID | None = None
    id_curso: UUID | None = None
    id_factura: UUID | None = None

    def __post_init__(self) -> None:
        if self.monto < 0:
            raise ValueError("El monto del pago no puede ser negativo.")
        if not self.metodo_pago.strip():
            self.metodo_pago = "efectivo"
        if self.estado not in {"pendiente", "pagado", "cancelado"}:
            raise ValueError("Estado de pago no válido.")

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
    ) -> "Pago":
        return cls(
            monto=monto,
            metodo_pago=metodo_pago,
            estado="pagado",
            id_usuario=id_usuario,
            id_curso=id_curso,
        )

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
