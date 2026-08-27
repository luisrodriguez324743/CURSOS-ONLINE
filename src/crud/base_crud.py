from dataclasses import fields
from typing import Any, Generic, TypeVar
from uuid import UUID

Entidad = TypeVar("Entidad")


class CRUD(Generic[Entidad]):
    def __init__(self, entidad: type[Entidad]) -> None:
        self.entidad = entidad
        self.registros: dict[UUID, Entidad] = {}
        self._campo_id = fields(entidad)[0].name

    def crear(self, registro: Entidad) -> Entidad:
        identificador = getattr(registro, self._campo_id)
        self.registros[identificador] = registro
        return registro

    def listar(self) -> list[Entidad]:
        return list(self.registros.values())

    def obtener(self, identificador: UUID) -> Entidad | None:
        return self.registros.get(identificador)

    def actualizar(
        self, identificador: UUID, cambios: dict[str, Any]
    ) -> Entidad | None:
        registro = self.obtener(identificador)
        if registro is None:
            return None

        nombres = {campo.name for campo in fields(self.entidad)}
        for nombre, valor in cambios.items():
            if nombre in nombres and nombre != self._campo_id:
                setattr(registro, nombre, valor)
        return registro

    def eliminar(self, identificador: UUID) -> bool:
        return self.registros.pop(identificador, None) is not None
