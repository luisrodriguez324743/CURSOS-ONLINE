from typing import Any
from uuid import UUID

from src.entities.progreso import Progreso
from .base_crud import CRUD


class ProgresoCRUD(CRUD[Progreso]):
    """
    CRUD encargado de gestionar el progreso académico
    de los usuarios dentro de los cursos.
    """

    def __init__(self) -> None:
        super().__init__(Progreso)

    def crear(self, registro: Progreso) -> Progreso:
        """Registra un nuevo progreso académico."""
        return super().crear(registro)

    def listar(self) -> list[Progreso]:
        """Obtiene todos los registros de progreso."""
        return super().listar()

    def obtener(self, identificador: UUID) -> Progreso | None:
        """Obtiene un progreso mediante su identificador."""
        return super().obtener(identificador)

    def actualizar(
        self,
        identificador: UUID,
        cambios: dict[str, Any]
    ) -> Progreso | None:
        """Actualiza los datos de un progreso existente."""
        return super().actualizar(identificador, cambios)

    def eliminar(self, identificador: UUID) -> bool:
        """Elimina un progreso mediante su identificador."""
        return super().eliminar(identificador)