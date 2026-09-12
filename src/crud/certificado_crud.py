from typing import Any
from uuid import UUID

from sqlalchemy import func
from sqlalchemy.exc import IntegrityError

from src.database.connection import get_session
from src.entities.certificado import Certificado


class CertificadoCRUD:
    def crear(self, registro: Certificado) -> Certificado:
        if registro is None:
            raise ValueError("El certificado no puede ser nulo.")
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
