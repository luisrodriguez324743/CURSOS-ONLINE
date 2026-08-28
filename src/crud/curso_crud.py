from src.entities.curso import Curso
from typing import Any
from uuid import UUID

from .base_crud import CRUD


class CursoCRUD(CRUD[Curso]):
    def __init__(self) -> None:
        super().__init__(Curso)

    def crear(self, registro: Curso) -> Curso:
        return super().crear(registro)

    def eliminar(self, identificador: UUID) -> bool:
        return super().eliminar(identificador)

    def actualizar(self, identificador: UUID, cambios: dict[str, Any]) -> Curso | None:
        return super().actualizar(identificador, cambios)

    def obtener(self, identificador: UUID) -> Curso | None:
        return super().obtener(identificador)

    def listar(self) -> list[Curso]:
        return super().listar()
