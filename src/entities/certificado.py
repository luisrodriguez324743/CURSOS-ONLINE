from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4


@dataclass
class Certificado:
    id_certificado: UUID = field(default_factory=uuid4)
    fecha_emision: datetime = field(default_factory=datetime.now)
    codigo: str = ""
    id_usuario: UUID | None = None
    id_curso: UUID | None = None

    def __post_init__(self) -> None:
        if not self.codigo:
            self.codigo = f"CERT-{self.id_certificado.hex[:8].upper()}"

    @staticmethod
    def puede_emitirse(
        pagos: list,
        facturas: list,
        progresos: list,
        id_usuario: UUID,
        id_curso: UUID,
    ) -> tuple[bool, str]:
        pago = next(
            (
                registro
                for registro in pagos
                if registro.id_usuario == id_usuario and registro.id_curso == id_curso
            ),
            None,
        )
        factura = next(
            (
                registro
                for registro in facturas
                if registro.id_usuario == id_usuario and registro.id_curso == id_curso
            ),
            None,
        )
        progreso = next(
            (
                registro
                for registro in progresos
                if registro.id_usuario == id_usuario and registro.id_curso == id_curso
            ),
            None,
        )

        if pago is None:
            return False, "No existe un pago registrado para este curso."
        if pago.estado != "pagado":
            return False, "El pago aún no está confirmado."
        if factura is None:
            return False, "No existe una factura asociada al curso."
        if factura.estado != "pagada":
            return False, "La factura aún no está pagada."
        if progreso is None:
            return False, "No existe progreso registrado para este curso."
        if progreso.porcentaje < 100:
            return False, "El progreso aún no llega al 100% para emitir el certificado."

        return True, "Certificado disponible."

    @classmethod
    def emitir_si_aplica(
        cls,
        pagos: list,
        facturas: list,
        progresos: list,
        id_usuario: UUID,
        id_curso: UUID,
    ) -> "Certificado | None":
        ok, mensaje = cls.puede_emitirse(
            pagos, facturas, progresos, id_usuario, id_curso
        )
        if not ok:
            print(mensaje)
            return None

        certificado = cls(id_usuario=id_usuario, id_curso=id_curso)
        return certificado

    def resumen(self) -> str:
        return (
            f"Certificado {self.codigo} | Curso: {self.id_curso} | "
            f"Usuario: {self.id_usuario} | Fecha: {self.fecha_emision.strftime('%d/%m/%Y')}"
        )
