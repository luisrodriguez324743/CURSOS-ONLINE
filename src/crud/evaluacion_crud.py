from typing import Any
from uuid import UUID

from src.entities.evaluacion import Evaluacion
from .base_crud import CRUD


class EvaluacionCRUD(CRUD[Evaluacion]):
    """
    CRUD encargado de gestionar las evaluaciones
    realizadas por los usuarios.
    """

    def __init__(self) -> None:
        super().__init__(Evaluacion)

    def crear(self, registro: Evaluacion) -> Evaluacion:
        """Registra una nueva evaluación."""
        return super().crear(registro)

    def listar(self) -> list[Evaluacion]:
        """Obtiene todas las evaluaciones registradas."""
        return super().listar()

    def obtener(self, identificador: UUID) -> Evaluacion | None:
        """Obtiene una evaluación mediante su identificador."""
        return super().obtener(identificador)

    def actualizar(
        self,
        identificador: UUID,
        cambios: dict[str, Any]
    ) -> Evaluacion | None:
        """Actualiza los datos de una evaluación existente."""
        return super().actualizar(identificador, cambios)

    def eliminar(self, identificador: UUID) -> bool:
        """Elimina una evaluación mediante su identificador."""
        return super().eliminar(identificador)