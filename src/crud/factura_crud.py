from typing import Any
from uuid import UUID

from sqlalchemy import func
from sqlalchemy.exc import IntegrityError

from database.connection import get_session
from entities.factura import Factura


class FacturaCRUD:
    def crear(self, registro: Factura) -> Factura:
        if registro is None:
            raise ValueError("La factura no puede ser nula.")
        if registro.total < 0:
            raise ValueError("El total de la factura no puede ser negativo.")

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

    def actualizar(self, identificador: UUID, cambios: dict[str, Any]) -> Factura | None:
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
            return session.query(Factura).order_by(func.lower(Factura.numero_factura)).all()
        finally:
            session.close()
