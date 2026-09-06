from typing import Any
from uuid import UUID

from src.entities.inscripcion import Inscripcion
from .base_crud import CRUD


class InscripcionCRUD(CRUD[Inscripcion]):
    """
    CRUD encargado de gestionar las inscripciones de los usuarios
    en los cursos disponibles.
    """

    def __init__(self) -> None:
        super().__init__(Inscripcion)

    def crear(self, registro: Inscripcion) -> Inscripcion:
        """Registra una nueva inscripción."""
        return super().crear(registro)

    def listar(self) -> list[Inscripcion]:
        """Obtiene todas las inscripciones registradas."""
        return super().listar()

    def obtener(self, identificador: UUID) -> Inscripcion | None:
        """Obtiene una inscripción mediante su identificador."""
        return super().obtener(identificador)

    def actualizar(
        self,
        identificador: UUID,
        cambios: dict[str, Any]
    ) -> Inscripcion | None:
        """Actualiza los datos de una inscripción existente."""
        return super().actualizar(identificador, cambios)

    def eliminar(self, identificador: UUID) -> bool:
        """Elimina una inscripción mediante su identificador."""
        return super().eliminar(identificador)