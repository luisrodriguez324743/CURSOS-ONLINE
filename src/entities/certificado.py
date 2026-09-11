from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import DateTime, String
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
    id_usuario: Mapped[UUID | None] = mapped_column(PGUUID(as_uuid=True), nullable=True)
    id_curso: Mapped[UUID | None] = mapped_column(PGUUID(as_uuid=True), nullable=True)

    def __init__(
        self,
        fecha_emision: datetime | None = None,
        codigo: str | None = None,
        id_usuario: UUID | None = None,
        id_curso: UUID | None = None,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self.fecha_emision = fecha_emision or datetime.now()
        self.codigo = codigo or f"CERT-{uuid4().hex[:8].upper()}"
        self.id_usuario = id_usuario
        self.id_curso = id_curso

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

        return cls(id_usuario=id_usuario, id_curso=id_curso)

    def to_dict(self) -> dict[str, object]:
        return {
            "id_certificado": str(self.id_certificado),
            "fecha_emision": self.fecha_emision.isoformat(),
            "codigo": self.codigo,
            "id_usuario": str(self.id_usuario) if self.id_usuario else None,
            "id_curso": str(self.id_curso) if self.id_curso else None,
        }

    def resumen(self) -> str:
        return (
            f"Certificado {self.codigo} | Curso: {self.id_curso} | "
            f"Usuario: {self.id_usuario} | Fecha: {self.fecha_emision.strftime('%d/%m/%Y')}"
        )
