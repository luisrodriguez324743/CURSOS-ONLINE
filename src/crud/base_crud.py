from typing import Any, Generic, TypeVar
from uuid import UUID

from src.database.connection import get_session

Entidad = TypeVar("Entidad")


class CRUD(Generic[Entidad]):
    def __init__(self, entidad: type[Entidad]) -> None:
        self.entidad = entidad

    def crear(self, registro: Entidad) -> Entidad:
        session = get_session()
        try:
            session.add(registro)
            session.commit()
            session.refresh(registro)
            return registro
        finally:
            session.close()

    def listar(self) -> list[Entidad]:
        session = get_session()
        try:
            return session.query(self.entidad).all()
        finally:
            session.close()

    def obtener(self, identificador: UUID) -> Entidad | None:
        session = get_session()
        try:
            return session.get(self.entidad, identificador)
        finally:
            session.close()

    def actualizar(
        self, identificador: UUID, cambios: dict[str, Any]
    ) -> Entidad | None:
        session = get_session()
        try:
            registro = session.get(self.entidad, identificador)
            if registro is None:
                return None
            for nombre, valor in cambios.items():
                if nombre != self._nombre_id() and hasattr(registro, nombre):
                    setattr(registro, nombre, valor)
            session.commit()
            session.refresh(registro)
            return registro
        finally:
            session.close()

    def eliminar(self, identificador: UUID) -> bool:
        session = get_session()
        try:
            registro = session.get(self.entidad, identificador)
            if registro is None:
                return False
            session.delete(registro)
            session.commit()
            return True
        finally:
            session.close()

    def _nombre_id(self) -> str:
        mapper = self.entidad.__mapper__
        return mapper.primary_key[0].name
