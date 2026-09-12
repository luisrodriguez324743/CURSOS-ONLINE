from typing import Any
from uuid import UUID

from sqlalchemy import func
from sqlalchemy.exc import IntegrityError

from src.database.connection import get_session
from src.entities.pago import Pago


class PagoCRUD:
    def crear(self, registro: Pago) -> Pago:
        if registro is None:
            raise ValueError("El pago no puede ser nulo.")
        if registro.monto < 0:
            raise ValueError("El monto del pago no puede ser negativo.")

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
