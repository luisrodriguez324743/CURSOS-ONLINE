from typing import Any
from uuid import UUID
from src.entities.progreso import Progreso
from .base_crud import CRUD

class ProgresoCRUD(CRUD[Progreso]):
    """
    CRUD encargado de gestionar el progreso académico de los usuarios.
    """
    def __init__(self) -> None:
        super().__init__(Progreso)

    def crear(self, registro: Progreso) -> Progreso:
        return super().crear(registro)

    def listar(self) -> list[Progreso]:
        return super().listar()

    def obtener(self, identificador: UUID) -> Progreso | None:
        return super().obtener(identificador)

    def actualizar(self, identificador: UUID, cambios: dict[str, Any]) -> Progreso | None:
        return super().actualizar(identificador, cambios)

    def eliminar(self, identificador: UUID) -> bool:
        return super().eliminar(identificador)