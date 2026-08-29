from typing import Any
from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4


@dataclass
class Factura:
    id_factura: UUID = field(default_factory=uuid4)
    numero_factura: str = ""
    fecha_emision: datetime = field(default_factory=datetime.now)
    total: float = 0.0
    id_inscripcion: UUID | None = None
    id_usuario: UUID | None = None
    id_curso: UUID | None = None
    detalle_cursos: list[dict[str, Any]] = field(default_factory=list)
    metodo_pago: str = ""
    estado: str = "emitida"

    def __post_init__(self) -> None:
        if self.total < 0:
            raise ValueError("El total de la factura no puede ser negativo.")
        if not self.numero_factura:
            self.numero_factura = f"FAC-{self.id_factura.hex[:8].upper()}"
        if self.estado not in {"emitida", "pagada", "anulada"}:
            raise ValueError("Estado de factura no válido.")

    @classmethod
    def crear_factura(
        cls,
        total: float,
        id_usuario: UUID | None,
        id_curso: UUID | None,
        id_inscripcion: UUID | None = None,
        metodo_pago: str = "efectivo",
    ) -> "Factura":
        factura = cls(
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
        return factura

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
