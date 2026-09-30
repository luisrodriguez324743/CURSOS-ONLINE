from typing import Any
from uuid import UUID

from sqlalchemy import func
from sqlalchemy.exc import IntegrityError

from src.database.connection import get_session
from src.crud.factura_crud import FacturaCRUD
from src.entities.factura import Factura
from src.entities.inscripcion import Inscripcion
from src.entities.pago import Pago


class PagoCRUD:
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
            if referencia is None or not PagoCRUD.validar_tarjeta(referencia):
                return (
                    False,
                    "La tarjeta no es válida. Debe tener entre 13 y 19 dígitos.",
                )
            return True, "Pago con tarjeta validado."
        if metodo in {"transferencia", "efectivo"}:
            return True, f"Pago por {metodo} registrado correctamente."
        return False, "Método de pago no válido."

    @staticmethod
    def resumen(pago: Pago) -> str:
        return (
            f"Pago #{pago.id_pago.hex[:8].upper()} | Monto: ${pago.monto:.2f} | "
            f"Método: {pago.metodo_pago} | Estado: {pago.estado}"
        )

    @classmethod
    def crear_pago(
        cls,
        monto: float,
        metodo_pago: str,
        id_usuario: UUID | None,
        id_curso: UUID | None,
        id_factura: UUID | None = None,
    ) -> Pago:
        return Pago(
            monto=monto,
            metodo_pago=metodo_pago,
            estado="pagado",
            id_usuario=id_usuario,
            id_curso=id_curso,
            id_factura=id_factura,
        )

    def crear(self, registro: Pago) -> Pago:
        if registro is None:
            raise ValueError("El pago no puede ser nulo.")
        if registro.monto < 0:
            raise ValueError("El monto del pago no puede ser negativo.")
        registro.metodo_pago = FacturaCRUD.validar_metodo_pago(
            registro.metodo_pago or "efectivo"
        )
        if registro.estado not in {"pendiente", "pagado", "cancelado"}:
            raise ValueError("Estado de pago no válido.")
        if registro.estado == "pagado":
            raise ValueError(
                "Los pagos confirmados deben registrarse junto con su factura."
            )

        session = get_session()
        try:
            session.add(registro)
            session.commit()
            session.refresh(registro)
            return registro
        except IntegrityError as exc:
            session.rollback()
            raise ValueError("No se pudo crear el pago.") from exc
        finally:
            session.close()

    def crear_con_factura(self, pago: Pago, factura: Factura) -> tuple[Pago, Factura]:
        if pago is None or factura is None:
            raise ValueError("El pago y la factura son obligatorios.")
        if pago.estado != "pagado":
            raise ValueError("Solo los pagos confirmados generan factura.")
        if pago.monto < 0:
            raise ValueError("El monto del pago no puede ser negativo.")
        if (
            pago.id_usuario is None
            or pago.id_curso is None
            or factura.id_usuario != pago.id_usuario
            or factura.id_curso != pago.id_curso
        ):
            raise ValueError(
                "La factura debe corresponder al usuario y curso del pago."
            )
        pago.metodo_pago = FacturaCRUD.validar_metodo_pago(
            pago.metodo_pago or "efectivo"
        )
        if factura.total != pago.monto:
            raise ValueError("El total de la factura debe coincidir con el pago.")
        if factura.estado != "pagada":
            raise ValueError("La factura de un pago confirmado debe estar pagada.")
        if not factura.numero_factura or not factura.numero_factura.strip():
            factura.numero_factura = FacturaCRUD.generar_numero_factura()
        factura.metodo_pago = pago.metodo_pago
        FacturaCRUD.validar_estado(factura.estado)

        session = get_session()
        try:
            inscripcion = (
                session.query(Inscripcion)
                .filter_by(id_usuario=pago.id_usuario, id_curso=pago.id_curso)
                .first()
            )
            if inscripcion is None:
                raise ValueError(
                    "El usuario debe estar inscrito en este curso antes de realizar el pago."
                )
            factura.id_inscripcion = inscripcion.id_inscripcion
            session.add(factura)
            session.flush()
            pago.id_factura = factura.id_factura
            session.add(pago)
            session.commit()
            session.refresh(factura)
            session.refresh(pago)
            return pago, factura
        except IntegrityError as exc:
            session.rollback()
            raise ValueError("No se pudo registrar el pago y su factura.") from exc
        finally:
            session.close()

    def eliminar(self, identificador: UUID) -> bool:
        session = get_session()
        try:
            registro = session.get(Pago, identificador)
            if registro is None:
                return False
            session.delete(registro)
            session.commit()
            return True
        except IntegrityError as exc:
            session.rollback()
            raise ValueError("No se pudo eliminar el pago.") from exc
        finally:
            session.close()

    def actualizar(self, identificador: UUID, cambios: dict[str, Any]) -> Pago | None:
        session = get_session()
        try:
            registro = session.get(Pago, identificador)
            if registro is None:
                return None
            estado_anterior = registro.estado
            campos_pago_confirmado = {
                "monto",
                "metodo_pago",
                "id_usuario",
                "id_curso",
                "id_factura",
            }
            if estado_anterior == "pagado" and campos_pago_confirmado.intersection(
                cambios
            ):
                raise ValueError(
                    "Los datos de un pago confirmado no se pueden modificar."
                )
            for nombre, valor in cambios.items():
                if nombre not in {"id_pago", "id_factura"} and hasattr(
                    registro, nombre
                ):
                    setattr(registro, nombre, valor)
            if registro.monto < 0:
                raise ValueError("El monto del pago no puede ser negativo.")
            registro.metodo_pago = FacturaCRUD.validar_metodo_pago(
                registro.metodo_pago or "efectivo"
            )
            if registro.estado not in {"pendiente", "pagado", "cancelado"}:
                raise ValueError("Estado de pago no válido.")
            if estado_anterior == "pagado" and registro.estado == "pendiente":
                raise ValueError("Un pago confirmado no puede volver a pendiente.")
            if estado_anterior == "cancelado" and registro.estado != "cancelado":
                raise ValueError("Un pago cancelado no se puede reactivar.")
            if estado_anterior != "pagado" and registro.estado == "pagado":
                self._generar_factura_para_pago(session, registro)
            elif estado_anterior == "pagado" and registro.estado == "cancelado":
                factura = session.get(Factura, registro.id_factura)
                if factura is not None:
                    factura.estado = "anulada"
            session.commit()
            session.refresh(registro)
            return registro
        except IntegrityError as exc:
            session.rollback()
            raise ValueError("No se pudo actualizar el pago.") from exc
        finally:
            session.close()

    @staticmethod
    def _generar_factura_para_pago(session, pago: Pago) -> Factura:
        if pago.id_usuario is None or pago.id_curso is None:
            raise ValueError("El pago requiere un usuario y un curso.")
        inscripcion = (
            session.query(Inscripcion)
            .filter_by(id_usuario=pago.id_usuario, id_curso=pago.id_curso)
            .first()
        )
        if inscripcion is None:
            raise ValueError(
                "El usuario debe estar inscrito en este curso antes de confirmar el pago."
            )

        if pago.id_factura is not None:
            factura = session.get(Factura, pago.id_factura)
            if (
                factura is None
                or factura.id_usuario != pago.id_usuario
                or factura.id_curso != pago.id_curso
                or factura.id_inscripcion != inscripcion.id_inscripcion
                or factura.total != pago.monto
                or factura.estado not in {"emitida", "pagada"}
            ):
                raise ValueError(
                    "La factura vinculada no coincide con los datos del pago."
                )
            factura.estado = "pagada"
            factura.metodo_pago = pago.metodo_pago
            return factura

        factura = Factura(
            numero_factura=FacturaCRUD.generar_numero_factura(),
            total=pago.monto,
            id_inscripcion=inscripcion.id_inscripcion,
            id_usuario=pago.id_usuario,
            id_curso=pago.id_curso,
            metodo_pago=pago.metodo_pago,
            estado="pagada",
        )
        session.add(factura)
        session.flush()
        pago.id_factura = factura.id_factura
        return factura

    def obtener(self, identificador: UUID) -> Pago | None:
        session = get_session()
        try:
            return session.get(Pago, identificador)
        finally:
            session.close()

    def listar(self) -> list[Pago]:
        session = get_session()
        try:
            return session.query(Pago).order_by(func.lower(Pago.metodo_pago)).all()
        finally:
            session.close()
