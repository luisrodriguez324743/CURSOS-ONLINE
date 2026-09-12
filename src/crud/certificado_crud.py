from typing import Any
from uuid import UUID, uuid4

from sqlalchemy import func
from sqlalchemy.exc import IntegrityError

from src.database.connection import get_session
from src.entities.certificado import Certificado


class CertificadoCRUD:
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
                if registro.id_usuario == id_usuario
                and registro.id_curso == id_curso
                and registro.id_leccion is None
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
        mostrar_mensaje: bool = True,
    ) -> Certificado | None:
        ok, mensaje = cls.puede_emitirse(
            pagos, facturas, progresos, id_usuario, id_curso
        )
        if not ok and mostrar_mensaje:
            print(mensaje)
        if not ok:
            return None
        return Certificado(id_usuario=id_usuario, id_curso=id_curso)

    @staticmethod
    def resumen(certificado: Certificado) -> str:
        return (
            f"Certificado {certificado.codigo} | Curso: {certificado.id_curso} | "
            f"Usuario: {certificado.id_usuario} | Fecha: {certificado.fecha_emision.strftime('%d/%m/%Y')}"
        )

    def crear(self, registro: Certificado) -> Certificado:
        if registro is None:
            raise ValueError("El certificado no puede ser nulo.")
        if registro.id_certificado is None:
            registro.id_certificado = uuid4()
        if not registro.codigo:
            registro.codigo = f"CERT-{registro.id_certificado.hex[:8].upper()}"

        session = get_session()
        try:
            session.add(registro)
            session.commit()
            session.refresh(registro)
            return registro
        except IntegrityError as exc:
            session.rollback()
            raise ValueError("No se pudo crear el certificado.") from exc
        finally:
            session.close()

    def obtener_por_usuario_curso(
        self, id_usuario: UUID, id_curso: UUID
    ) -> Certificado | None:
        session = get_session()
        try:
            return (
                session.query(Certificado)
                .filter_by(id_usuario=id_usuario, id_curso=id_curso)
                .first()
            )
        finally:
            session.close()

    def eliminar(self, identificador: UUID) -> bool:
        session = get_session()
        try:
            registro = session.get(Certificado, identificador)
            if registro is None:
                return False
            session.delete(registro)
            session.commit()
            return True
        except IntegrityError as exc:
            session.rollback()
            raise ValueError("No se pudo eliminar el certificado.") from exc
        finally:
            session.close()

    def actualizar(
        self, identificador: UUID, cambios: dict[str, Any]
    ) -> Certificado | None:
        session = get_session()
        try:
            registro = session.get(Certificado, identificador)
            if registro is None:
                return None
            for nombre, valor in cambios.items():
                if nombre != "id_certificado" and hasattr(registro, nombre):
                    setattr(registro, nombre, valor)
            if not registro.codigo:
                registro.codigo = f"CERT-{registro.id_certificado.hex[:8].upper()}"
            session.commit()
            session.refresh(registro)
            return registro
        except IntegrityError as exc:
            session.rollback()
            raise ValueError("No se pudo actualizar el certificado.") from exc
        finally:
            session.close()

    def obtener(self, identificador: UUID) -> Certificado | None:
        session = get_session()
        try:
            return session.get(Certificado, identificador)
        finally:
            session.close()

    def listar(self) -> list[Certificado]:
        session = get_session()
        try:
            return (
                session.query(Certificado)
                .order_by(func.lower(Certificado.codigo))
                .all()
            )
        finally:
            session.close()
