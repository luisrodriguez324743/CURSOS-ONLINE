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
        return super().crear(registro)

    def listar(self) -> list[Inscripcion]:
        return super().listar()

    def obtener(self, identificador: UUID) -> Inscripcion | None:
        return super().obtener(identificador)

    def actualizar(self, identificador: UUID, cambios: dict[str, Any]) -> Inscripcion | None:
        return super().actualizar(identificador, cambios)

    def eliminar(self, identificador: UUID) -> bool:
        return super().eliminar(identificador)