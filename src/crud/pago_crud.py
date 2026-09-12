from typing import Any
from uuid import UUID

from sqlalchemy import func
from sqlalchemy.exc import IntegrityError

from src.database.connection import get_session
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
        if not registro.metodo_pago or not registro.metodo_pago.strip():
            registro.metodo_pago = "efectivo"
        if registro.estado not in {"pendiente", "pagado", "cancelado"}:
            raise ValueError("Estado de pago no válido.")

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
            for nombre, valor in cambios.items():
                if nombre != "id_pago" and hasattr(registro, nombre):
                    setattr(registro, nombre, valor)
            if registro.monto < 0:
                raise ValueError("El monto del pago no puede ser negativo.")
            if registro.metodo_pago is not None and not registro.metodo_pago.strip():
                registro.metodo_pago = "efectivo"
            if registro.estado not in {"pendiente", "pagado", "cancelado"}:
                raise ValueError("Estado de pago no válido.")
            session.commit()
            session.refresh(registro)
            return registro
        except IntegrityError as exc:
            session.rollback()
            raise ValueError("No se pudo actualizar el pago.") from exc
        finally:
            session.close()

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
