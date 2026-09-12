from typing import Any
from uuid import UUID, uuid4

from sqlalchemy import func
from sqlalchemy.exc import IntegrityError

from src.database.connection import get_session
from src.entities.factura import Factura


class FacturaCRUD:
    @staticmethod
    def generar_numero_factura() -> str:
        return f"FAC-{uuid4().hex[:8].upper()}"

    @staticmethod
    def validar_total(total: float) -> None:
        if total < 0:
            raise ValueError("El total de la factura no puede ser negativo.")

    @staticmethod
    def validar_estado(estado: str) -> None:
        if estado not in {"emitida", "pagada", "anulada"}:
            raise ValueError("Estado de factura no válido.")

    @staticmethod
    def generar_comprobante(
        factura: Factura, nombre_curso: str, nombre_usuario: str
    ) -> str:
        return (
            "\n========================================\n"
            f"        COMPROBANTE DE PAGO\n"
            "========================================\n"
            f"Factura: {factura.numero_factura}\n"
            f"Fecha: {factura.fecha_emision.strftime('%d/%m/%Y %H:%M')}\n"
            f"Cliente: {nombre_usuario}\n"
            f"Curso: {nombre_curso}\n"
            f"Método de pago: {factura.metodo_pago}\n"
            f"Total: ${factura.total:.2f}\n"
            f"Estado: {factura.estado}\n"
            "========================================\n"
        )

    @staticmethod
    def to_dict(factura: Factura) -> dict[str, Any]:
        return {
            "id_factura": str(factura.id_factura),
            "numero_factura": factura.numero_factura,
            "fecha_emision": factura.fecha_emision.isoformat(),
            "total": factura.total,
            "id_inscripcion": (
                str(factura.id_inscripcion) if factura.id_inscripcion else None
            ),
            "id_usuario": str(factura.id_usuario) if factura.id_usuario else None,
            "id_curso": str(factura.id_curso) if factura.id_curso else None,
            "detalle_cursos": factura.detalle_cursos,
            "metodo_pago": factura.metodo_pago,
            "estado": factura.estado,
        }

    def crear(self, registro: Factura) -> Factura:
        if registro is None:
            raise ValueError("La factura no puede ser nula.")
        self.validar_total(registro.total)
        if not registro.numero_factura or not registro.numero_factura.strip():
            registro.numero_factura = self.generar_numero_factura()
        if not registro.metodo_pago or not registro.metodo_pago.strip():
            registro.metodo_pago = "efectivo"
        self.validar_estado(registro.estado)

        session = get_session()
        try:
            session.add(registro)
            session.commit()
            session.refresh(registro)
            return registro
        except IntegrityError as exc:
            session.rollback()
            raise ValueError("No se pudo crear la factura.") from exc
        finally:
            session.close()

    def eliminar(self, identificador: UUID) -> bool:
        session = get_session()
        try:
            registro = session.get(Factura, identificador)
            if registro is None:
                return False
            session.delete(registro)
            session.commit()
            return True
        except IntegrityError as exc:
            session.rollback()
            raise ValueError("No se pudo eliminar la factura.") from exc
        finally:
            session.close()

    def actualizar(
        self, identificador: UUID, cambios: dict[str, Any]
    ) -> Factura | None:
        session = get_session()
        try:
            registro = session.get(Factura, identificador)
            if registro is None:
                return None
            for nombre, valor in cambios.items():
                if nombre != "id_factura" and hasattr(registro, nombre):
                    setattr(registro, nombre, valor)
            if registro.total < 0:
                raise ValueError("El total de la factura no puede ser negativo.")
            if registro.metodo_pago is not None and not registro.metodo_pago.strip():
                registro.metodo_pago = "efectivo"
            if registro.estado not in {"emitida", "pagada", "anulada"}:
                raise ValueError("Estado de factura no válido.")
            session.commit()
            session.refresh(registro)
            return registro
        except IntegrityError as exc:
            session.rollback()
            raise ValueError("No se pudo actualizar la factura.") from exc
        finally:
            session.close()

    def obtener(self, identificador: UUID) -> Factura | None:
        session = get_session()
        try:
            return session.get(Factura, identificador)
        finally:
            session.close()

    def listar(self) -> list[Factura]:
        session = get_session()
        try:
            return (
                session.query(Factura)
                .order_by(func.lower(Factura.numero_factura))
                .all()
            )
        finally:
            session.close()
